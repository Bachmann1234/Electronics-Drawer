import random
import os
import argparse
import time
import json
from datetime import datetime
from io import BytesIO
from dataclasses import dataclass, asdict
import requests
from PIL import Image, ImageFont, ImageDraw
from requests.models import HTTPBasicAuth
from font_source_serif_pro import SourceSerifProSemibold
import hitherdither

# Hitherdither is not on pypi
# python3 -m pip install git+https://www.github.com/hbldh/hitherdither
DOG_URL = "https://pbs.twimg.com/media/EUUsJsKXYAUC8vg?format=png&name=900x900"
MAX_ATTEMPTS = 5
HISTORY_DIR = os.environ.get("ART_HISTORY_DIR", os.path.expanduser("~/art_history"))
HISTORY_KEEP = int(os.environ.get("ART_HISTORY_KEEP", "50"))

try:
    from inky.auto import auto as Inky

    has_inky = True
except ImportError:
    print("Could not import inky")
    has_inky = False


@dataclass
class Art:
    artist: str
    title: str
    image_url: str
    # Where to find the piece again, for the history
    page_url: str = ""


class UrlSource:
    def __init__(self, url):
        self.url = url

    def grab_art(self) -> Art:
        return Art(
            "Matt Bachmann" if self.url == DOG_URL else "Unknown",
            "Dog" if self.url == DOG_URL else "Unknown",
            self.url,
            self.url,
        )


class Reddit:
    CLIENT_ID = os.environ["REDDIT_CLIENT_ID"]
    CLIENT_SECRET = os.environ["REDDIT_CLIENT_SECRET"]
    REDDIT_USER_AGENT = os.environ["REDDIT_USER_AGENT"]
    HOST = "https://www.reddit.com"
    OAUTH_HOST = "https://oauth.reddit.com"

    def _get_access_token(self) -> str:
        response = requests.post(
            f"{self.HOST}/api/v1/access_token",
            auth=HTTPBasicAuth(self.CLIENT_ID, self.CLIENT_SECRET),
            data={
                "grant_type": "client_credentials",
            },
            headers={"User-agent": self.REDDIT_USER_AGENT},
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def _grab_random_piece(self, access_token: str) -> dict:
        pieces = []
        after = ""
        for _ in range(10):
            response = requests.get(
                f"{self.OAUTH_HOST}/r/art/hot?raw_json=1&g=US&limit=100{f'&after={after}' if after else ''}",
                headers={
                    "Authorization": f"bearer {access_token}",
                    "User-agent": self.REDDIT_USER_AGENT,
                },
            )
            response.raise_for_status()
            response_data = response.json()["data"]
            after = response_data["after"]
            pieces += response_data["children"]

        piece = random.choice(pieces)
        return piece["data"]

    def grab_art(self) -> Art:
        access_token = self._get_access_token()
        piece = self._grab_random_piece(access_token)
        return Art(
            piece["author"],
            piece["title"].split(",")[0],
            piece["url"],
            f"{self.HOST}{piece['permalink']}",
        )


class Deviantart:
    CLIENT_ID = os.environ["DEVIANT_ART_CLIENT_ID"]
    CLIENT_SECRET = os.environ["DEVIANT_ART_CLIENT_SECRET"]
    HOST = "https://www.deviantart.com"

    def _get_access_token(self) -> str:
        response = requests.post(
            f"{self.HOST}/oauth2/token",
            data={
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
                "grant_type": "client_credentials",
            },
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def _grab_random_piece(self, access_token: str) -> dict:
        offset = 0
        results = []
        for _ in range(10):
            pieces_response = requests.get(
                f"https://www.deviantart.com/api/v1/oauth2/browse/dailydeviations?&limit=120&offset={offset}&access_token={access_token}"
            )
            pieces_response.raise_for_status()
            results_json = pieces_response.json()
            results += results_json["results"]
            # has_more is sometimes true with no next_offset on the last page
            if not results_json["has_more"] or results_json.get("next_offset") is None:
                break
            offset = results_json["next_offset"]
        return random.choice(results)

    def grab_art(self) -> Art:
        access_token = self._get_access_token()
        piece = self._grab_random_piece(access_token)
        # content is the full image (around 1000px), thumbs top out at 300px
        # wide which looks soft on the 600px colour panel
        image = piece.get("content") or piece.get("preview")
        if not image and piece.get("thumbs"):
            image = max(piece["thumbs"], key=lambda t: t["width"])
        if not image:
            raise ValueError(f"No image for {piece.get('url')}, probably literature")
        return Art(
            piece["author"]["username"],
            piece["title"],
            image["src"],
            piece.get("url", ""),
        )


class Metropolitan:
    def _grab_random_object_id(self) -> int:
        object_ids_response = requests.get(
            "https://collectionapi.metmuseum.org/public/collection/v1/objects"
        )
        object_ids_response.raise_for_status()
        return random.choice(object_ids_response.json()["objectIDs"])

    def _grab_art(self) -> Art:
        object_id = self._grab_random_object_id()
        object_response = requests.get(
            f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
        )
        object_response.raise_for_status()
        object_dict = object_response.json()
        return Art(
            artist=object_dict["artistDisplayName"],
            title=object_dict["title"],
            image_url=object_dict["primaryImage"],
            page_url=object_dict.get("objectURL", ""),
        )

    def grab_art(self) -> Art:
        art = self._grab_art()
        for _ in range(10):
            if art.image_url:
                break
            art = self._grab_art()
        if not art.image_url:
            """
            So many pieces provided by this api are restricted such that they 'cant'
            be downloaded. In theory you can scrape them from the page but out of
            respect I wont

            I give up after a few tries so I dont end up in an infinate loop after some
            bug
            """
            raise ValueError("After a few times I never got an image with a url")
        return art


def load_image(image_url: str, width: int, height: int) -> Image:
    response = requests.get(image_url, timeout=60)
    response.raise_for_status()
    # Raises if the url was not an image (e.g. a reddit gallery or link post)
    img = Image.open(BytesIO(response.content))
    # Let the jpeg decoder downscale huge images, resizing them is slow on a pi zero
    img.draft("RGB", (width, height))
    img.load()
    return img


def convert_image(img: Image, w_cropped, h_new) -> Image:
    w, h = img.size
    w_new = int((float(w) / h) * h_new)
    img = img.resize((w_new, h_new), resample=Image.LANCZOS)
    x0 = (w_new - w_cropped) / 2
    x1 = x0 + w_cropped
    y0 = 0
    y1 = h_new
    img = img.crop((x0, y0, x1, y1))
    return img


def add_footer(
    img: Image,
    art_selection: Art,
    art_source_name: str,
    width,
    height,
    background_fill,
    text_fill,
) -> Image:
    draw = ImageDraw.Draw(img)
    font_size = 12
    author_font = ImageFont.truetype(SourceSerifProSemibold, font_size)
    draw.rectangle(
        [(0, height - 15), (width, height)],
        fill=background_fill,
    )
    draw.multiline_text(
        (5, height - 15),
        f"'{art_selection.title.strip() or 'untitled'}' by {art_selection.artist.strip() or 'unknown'} ({art_source_name})",
        fill=text_fill,
        font=author_font,
        align="left",
    )
    return img


def is_color(inky_board) -> bool:
    # the inkyWHAT does not have _palette_blend
    return hasattr(inky_board, "_palette_blend")


def clean(inky_board) -> None:
    """Flush the panel to reduce ghosting.

    The colour panel needs this before every image. Twice, once does not seem
    to clear it well. The wHAT only needs it now and then (cron runs it nightly).
    """
    if is_color(inky_board):
        colours = [inky_board.CLEAN] * 2
    else:
        colours = [inky_board.RED, inky_board.BLACK, inky_board.WHITE] * 3
    for colour in colours:
        inky_board.set_border(colour)
        inky_board.buf.fill(colour)
        inky_board.show()
        time.sleep(1)


def save_history(img: Image, art_selection: Art, art_source_name: str) -> None:
    """Keep the last HISTORY_KEEP images shown, so a piece I liked can be found again.

    history.log gets a line per image and is never pruned, so the links outlive the images.
    """
    os.makedirs(HISTORY_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    img.save(os.path.join(HISTORY_DIR, f"{stamp}.png"))
    details = {"source": art_source_name, **asdict(art_selection)}
    with open(os.path.join(HISTORY_DIR, f"{stamp}.json"), "w") as f:
        json.dump(details, f, indent=2)
    with open(os.path.join(HISTORY_DIR, "history.log"), "a") as f:
        f.write(
            f"{stamp}\t{art_source_name}\t{art_selection.title}\t{art_selection.artist}"
            f"\t{art_selection.page_url or art_selection.image_url}\n"
        )
    stamps = sorted(n[:-4] for n in os.listdir(HISTORY_DIR) if n.endswith(".png"))
    for old in stamps[:-HISTORY_KEEP]:
        for ext in (".png", ".json"):
            try:
                os.remove(os.path.join(HISTORY_DIR, old + ext))
            except FileNotFoundError:
                pass


def draw_image(inky_board, img: Image, art_selection: Art, art_source_name: str) -> None:
    img = convert_image(img, inky_board.width, inky_board.height)
    img = add_footer(
        img,
        art_selection,
        art_source_name,
        inky_board.width,
        inky_board.height,
        (255, 255, 255, 255),
        (0, 0, 0, 0),
    )
    img = img.convert("RGB")
    # The history keeps the undithered image, it looks more like the art
    history_img = img
    if is_color(inky_board):
        palette = hitherdither.palette.Palette(
            inky_board._palette_blend(0.5, dtype="uint24")
        )
        img = hitherdither.ordered.bayer.bayer_dithering(
            img, palette, [64, 64, 64], order=8
        )
        # Only clear once the new image is ready, so a failure never leaves it blank
        clean(inky_board)
        inky_board.set_image(img, saturation=0.5)
    else:
        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette((255, 255, 255, 0, 0, 0, 255, 0, 0) + (0, 0, 0) * 252)
        img = img.convert("RGB").quantize(palette=pal_img)
        inky_board.set_image(img)

    inky_board.show()
    try:
        save_history(history_img, art_selection, art_source_name)
    except OSError as e:
        print(f"Could not save history: {e!r}")


def main():
    parser = argparse.ArgumentParser(
        description="Tell me the source you want me to grab from"
    )
    parser.add_argument(
        "--source",
        choices=["metro", "deviant", "reddit", "url"],
        help="Where should I grab the art from",
    )
    parser.add_argument(
        "--url", help="Specific url when using the url source", default=DOG_URL
    )
    parser.add_argument(
        "--clean", action="store_true", help="Just clean the panel, no art"
    )
    parsed_args = parser.parse_args()
    inky_board = Inky() if has_inky else None
    if parsed_args.clean:
        clean(inky_board)
        return
    sources = {
        "metro": Metropolitan(),
        "deviant": Deviantart(),
        "reddit": Reddit(),
        "url": UrlSource(parsed_args.url),
    }
    # Only picked when asked for. The met has a lot that does not look great on the displays
    not_random = {"url", "metro"}
    width, height = (inky_board.width, inky_board.height) if has_inky else (600, 448)
    # Some picks are not images or fail to download, try a few before giving up
    for attempt in range(1, MAX_ATTEMPTS + 1):
        art_source = sources[
            parsed_args.source
            if parsed_args.source
            else random.choice([k for k in sources if k not in not_random])
        ]
        art_source_name = art_source.__class__.__name__
        try:
            art_selection = art_source.grab_art()
            print(f"{art_source_name} - {art_selection.title} by {art_selection.artist}")
            print(art_selection.image_url)
            image = load_image(art_selection.image_url, width, height)
            break
        except Exception as e:
            print(f"Attempt {attempt} failed: {e!r}")
            if attempt == MAX_ATTEMPTS:
                raise
    if has_inky:
        draw_image(inky_board, image, art_selection, art_source_name)


if __name__ == "__main__":
    main()
