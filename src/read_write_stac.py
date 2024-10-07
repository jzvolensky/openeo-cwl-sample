import json
import pystac
import os
import sys
import logging
import requests
from typing import Union

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def read_stac(stac_url: str) -> Union[pystac.Catalog, pystac.Collection]:
    response = requests.get(stac_url)
    if response.status_code == 200:
        try:
            if "application/json" in response.headers.get("Content-Type", ""):
                stac_dict = response.json()
                if stac_dict.get("type") == "Collection":
                    stac_object = pystac.Collection.from_dict(stac_dict)
                else:
                    stac_object = pystac.Catalog.from_dict(stac_dict)
                logger.info(f"Read STAC from {stac_url}")
                return stac_object
            else:
                logger.error(
                    f"Unexpected content type: {response.headers.get('Content-Type')}"
                )
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from {stac_url}: {e}")
            logger.debug(f"Response content: {response.text}")
    else:
        logger.error(
            f"Failed to fetch STAC from {stac_url}, status code: {response.status_code}"
        )
    return None


def print_stac_info(stac_object: Union[pystac.Catalog, pystac.Collection]):
    if stac_object:
        logger.info(f"STAC ID: {stac_object.id}")
        logger.info(f"STAC Description: {stac_object.description}")


def rewrite_stac(stac_object: Union[pystac.Catalog, pystac.Collection], output_path: str):
    if isinstance(stac_object, pystac.Collection):
        new_collection = stac_object
    else:
        new_collection = pystac.Collection(
            id="combined-collection",
            description="Combined STAC Collection",
            extent=stac_object.extent
        )
        new_collection.add_child(stac_object)

    # custom metadata here and save new collection
    new_collection.extra_fields["custom_metadata"] = (
        "Metadata appended by read_write_stac.py"
    )

    new_collection.normalize_and_save(
        output_path, catalog_type=pystac.CatalogType.SELF_CONTAINED
    )
    logger.info(f"New collection written to {output_path}")


def main():
    logger.debug(f"Script arguments: {sys.argv}")
    logger.debug(f"Number of arguments: {len(sys.argv)}")

    if len(sys.argv) < 2:
        logger.error("Please provide a STAC URL")
        sys.exit(1)

    stac_url = sys.argv[1]
    logger.debug(f"STAC URL: {stac_url}")

    stac_object = read_stac(stac_url)
    print_stac_info(stac_object)
    rewrite_stac(stac_object, "output_collection")


if __name__ == "__main__":
    main()