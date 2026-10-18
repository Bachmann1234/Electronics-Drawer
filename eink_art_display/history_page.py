"""Writes index.html in the history directory so the history can be browsed.

find_art.py calls this after each image. Run it directly to rebuild the page:
python3 history_page.py [history_dir]

Serve the directory with: python3 -m http.server 8080 --directory ~/art_history
"""
import html
import json
import os
import socket
import sys
from datetime import datetime

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} history</title>
<style>
:root {{ --bg: #f6f4ef; --card: #fff; --text: #222; --muted: #6b6b6b; --line: #e2ded5; --link: #2a5db0; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #17171a; --card: #222226; --text: #eee; --muted: #a0a0a8; --line: #33333a; --link: #8ab4f8; }}
}}
body {{ margin: 0; padding: 16px; background: var(--bg); color: var(--text);
  font: 15px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
header {{ max-width: 1200px; margin: 0 auto 16px; display: flex; flex-wrap: wrap;
  align-items: baseline; gap: 4px 16px; }}
h1 {{ font-size: 20px; margin: 0; }}
header span {{ color: var(--muted); }}
a {{ color: var(--link); }}
main {{ max-width: 1200px; margin: 0 auto; display: grid; gap: 16px;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); }}
figure {{ margin: 0; background: var(--card); border: 1px solid var(--line);
  border-radius: 8px; overflow: hidden; }}
figure img {{ display: block; width: 100%; height: auto; }}
figcaption {{ padding: 8px 10px 10px; }}
.title {{ font-weight: 600; overflow-wrap: anywhere; }}
.meta {{ color: var(--muted); font-size: 13px; }}
</style>
</head>
<body>
<header>
<h1>{name}</h1>
<span>Last {count} images shown, newest first. Updated {updated}.</span>
<a href="history.log">Everything ever shown</a>
</header>
<main>
{cards}
</main>
</body>
</html>
"""

CARD = """<figure>
<a href="{image}"><img src="{image}" alt="{title}" loading="lazy"></a>
<figcaption>
<div class="title">{link}</div>
<div>{artist}</div>
<div class="meta">{source} &middot; {shown}</div>
</figcaption>
</figure>"""


def _card(stamp: str, details: dict) -> str:
    title = html.escape(details.get("title", "").strip() or "Untitled")
    url = details.get("page_url") or details.get("image_url")
    link = f'<a href="{html.escape(url)}">{title}</a>' if url else title
    try:
        shown = datetime.strptime(stamp, "%Y%m%d-%H%M%S").strftime("%a %b %-d, %-I:%M %p")
    except ValueError:
        shown = stamp
    return CARD.format(
        image=html.escape(f"{stamp}.png"),
        title=title,
        link=link,
        artist=html.escape(details.get("artist", "").strip() or "Unknown artist"),
        source=html.escape(details.get("source", "")),
        shown=shown,
    )


def write_history_page(history_dir: str) -> None:
    stamps = sorted(
        (n[:-5] for n in os.listdir(history_dir) if n.endswith(".json")), reverse=True
    )
    cards = []
    for stamp in stamps:
        if not os.path.exists(os.path.join(history_dir, f"{stamp}.png")):
            continue
        try:
            with open(os.path.join(history_dir, f"{stamp}.json")) as f:
                details = json.load(f)
        except (OSError, ValueError):
            continue
        cards.append(_card(stamp, details))
    page = PAGE.format(
        name=html.escape(socket.gethostname()),
        count=len(cards),
        updated=datetime.now().strftime("%a %b %-d, %-I:%M %p"),
        cards="\n".join(cards),
    )
    # Write then rename so the server never hands out a half written page
    tmp = os.path.join(history_dir, ".index.html.tmp")
    with open(tmp, "w") as f:
        f.write(page)
    os.replace(tmp, os.path.join(history_dir, "index.html"))


if __name__ == "__main__":
    write_history_page(
        sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser("~/art_history")
    )
