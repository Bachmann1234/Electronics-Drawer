import random
import os
import argparse
from dataclasses import dataclass
import requests


@dataclass
class Art:
    artist: str
    title: str
    image_url: str


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
        popular_pieces_response = requests.get(
            f"https://www.deviantart.com/api/v1/oauth2/browse/popular?&limit=120&access_token={access_token}"
        )
        popular_pieces_response.raise_for_status()
        return random.choice(popular_pieces_response.json()["results"])

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


def main():
    parser = argparse.ArgumentParser(
        description="Tell me the source you want me to grab from"
    )
    parser.add_argument(
        "--source",
        choices=["metro", "deviant"],
        help="Where should I grab the art from",
    )
    parsed_args = parser.parse_args()
    sources = {"metro": Metropolitan(), "deviant": Deviantart()}
    art_source = sources[
        parsed_args.source
        if parsed_args.source
        else random.choice(list(sources.keys()))
    ]
    art_seletion = art_source.grab_art()
    print(art_seletion.image_url)


if __name__ == "__main__":
    main()
