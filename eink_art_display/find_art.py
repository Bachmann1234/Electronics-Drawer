import random
from dataclasses import dataclass
import requests


@dataclass
class Art:
    artist_name: str
    artist_url: str
    image_url: str


class Metropolitan:
    def _grab_random_object_id(self) -> int:
        object_ids_response = requests.get(
            "https://collectionapi.metmuseum.org/public/collection/v1/objects"
        )
        object_ids_response.raise_for_status()
        return random.choice(object_ids_response.json()["objectIDs"])

    def grab_art(self) -> Art:
        object_id = self._grab_random_object_id()
        object_response = requests.get(
            f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
        )
        object_response.raise_for_status()
        object_dict = object_response.json()
        return Art(
            artist_name=object_dict["artistDisplayName"],
            artist_url=object_dict["artistWikidata_URL"],
            image_url=object_dict["primaryImage"],
        )


def main():
    print(Metropolitan().grab_art().image_url)


if __name__ == "__main__":
    main()
