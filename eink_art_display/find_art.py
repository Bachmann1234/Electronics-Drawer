import random
from dataclasses import dataclass
import requests


@dataclass
class Art:
    artist_name: str
    art_url: str
    image_url: str


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
            artist_name=object_dict["artistDisplayName"],
            art_url=object_dict["objectURL"],
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
    print(Metropolitan().grab_art())


if __name__ == "__main__":
    main()
