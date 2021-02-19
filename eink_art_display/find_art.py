import random
import os
import argparse
from dataclasses import dataclass
import requests
from PIL import Image, ImageFont, ImageDraw
from requests.models import HTTPBasicAuth
from font_source_serif_pro import SourceSerifProSemibold
import hitherdither

try:
    from inky.inky_uc8159 import Inky

    has_inky = True
except ImportError:
    print("Could not import inky")
    has_inky = False


@dataclass
class Art:
    artist: str
    title: str
    image_url: str


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
        return Art(piece["author"], piece["title"].split(",")[0], piece["url"])


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
            popular_pieces_response = requests.get(
                f"https://www.deviantart.com/api/v1/oauth2/browse/popular?&limit=120&offset={offset}&access_token={access_token}"
            )
            popular_pieces_response.raise_for_status()
            results_json = popular_pieces_response.json()
            results += results_json["results"]
            if not results_json["has_more"]:
                break
            offset = results_json["next_offset"]
        return random.choice(results)

    def grab_art(self) -> Art:
        access_token = self._get_access_token()
        piece = self._grab_random_piece(access_token)
        return Art(
            piece["author"]["username"], piece["title"], piece["thumbs"][-1]["src"]
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


def load_image(image_url: str) -> Image:
    return Image.open(requests.get(image_url, stream=True).raw)


def convert_image(img: Image, palette) -> Image:
    w, h = img.size
    h_new = 448
    w_new = int((float(w) / h) * h_new)
    w_cropped = 600
    img = img.resize((w_new, h_new), resample=Image.LANCZOS)
    x0 = (w_new - w_cropped) / 2
    x1 = x0 + w_cropped
    y0 = 0
    y1 = h_new
    img = img.crop((x0, y0, x1, y1))
    return img


def add_footer(
    img: Image, art_selection: Art, art_source_name: str, width, height
) -> Image:
    draw = ImageDraw.Draw(img)
    font_size = 12
    author_font = ImageFont.truetype(SourceSerifProSemibold, font_size)
    draw.rectangle(
        [(0, height - 15), (width, height)],
        fill=(255, 255, 255, 255),
    )
    draw.multiline_text(
        (5, height - 15),
        f"'{art_selection.title.strip() or 'untitled'}' by {art_selection.artist.strip() or 'unknown'} ({art_source_name})",
        fill=(0, 0, 0, 0),
        font=author_font,
        align="left",
    )
    return img


def draw_image(img: Image, art_selection: Art, art_source_name: str) -> None:
    inky_board = Inky()
    palette = hitherdither.palette.Palette(
        inky_board._palette_blend(0.5, dtype="uint24")
    )
    img = convert_image(img, palette)
    img = add_footer(
        img, art_selection, art_source_name, inky_board.width, inky_board.height
    )
    img = img.convert("RGB")
    img = hitherdither.ordered.bayer.bayer_dithering(
        img, palette, [64, 64, 64], order=8
    )
    inky_board.set_image(img, saturation=0.5)
    inky_board.show()


def main():
    parser = argparse.ArgumentParser(
        description="Tell me the source you want me to grab from"
    )
    parser.add_argument(
        "--source",
        choices=["metro", "deviant", "reddit"],
        help="Where should I grab the art from",
    )
    parsed_args = parser.parse_args()
    sources = {"metro": Metropolitan(), "deviant": Deviantart(), "reddit": Reddit()}
    art_source = sources[
        parsed_args.source
        if parsed_args.source
        else random.choice(list(sources.keys()))
    ]
    art_selection = art_source.grab_art()
    # Stub selection so I can take a picture of this without
    # using someone elses art
    # art_selection = Art(
    #     "Matt Bachmann",
    #     "Dog",
    #     "https://pbs.twimg.com/media/EUUsJsKXYAUC8vg?format=png&name=900x900",
    # )
    art_source_name = art_source.__class__.__name__
    print(f"{art_source_name} - {art_selection.title} by {art_selection.artist}")
    print(art_selection.image_url)
    if has_inky:
        image = load_image(art_selection.image_url)
        draw_image(image, art_selection, art_source_name)


if __name__ == "__main__":
    main()
