"""
Sample script to test OpenEO CWL integration
All that it does is read 1 or multiple STAC
Collections, confirms that the STAC is valid,
confirms that it has been read correctly and
rewrites the STAC with some custom appended
metadata to show that the STAC has been written
by this script.

Author: Juraj Zvolensky @jzvolensky
"""

import json
import pystac
import os
import sys
import logging
import requests
from typing import List, Union

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def read_stac(stac_urls: List[str]) -> List[Union[pystac.Catalog, pystac.Collection]]:
    stac_objects = []
    for stac_url in stac_urls:
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
                    stac_objects.append(stac_object)
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
    return stac_objects


def print_stac_info(stac_objects: List[Union[pystac.Catalog, pystac.Collection]]):
    for stac_object in stac_objects:
        logger.info(f"STAC ID: {stac_object.id}")
        logger.info(f"STAC Description: {stac_object.description}")


def rewrite_stac(
    stac_objects: List[Union[pystac.Catalog, pystac.Collection]], output_path: str
):
    new_catalog = pystac.Catalog(
        id="combined-catalog", description="Combined STAC Catalog"
    )
    for stac_object in stac_objects:
        new_catalog.add_child(stac_object)

    # custom metadata here and save new catalog
    new_catalog.extra_fields["custom_metadata"] = (
        "Metadata appended by read_write_stac.py"
    )

    new_catalog.normalize_and_save(
        output_path, catalog_type=pystac.CatalogType.SELF_CONTAINED
    )
    logger.info(f"New catalog written to {output_path}")


def main():
    logger.debug(f"Script arguments: {sys.argv}")
    logger.debug(f"Number of arguments: {len(sys.argv)}")

    if len(sys.argv) < 2:
        logger.error("Please provide at least one STAC URL")
        sys.exit(1)

    stac_urls_str = sys.argv[1]
    logger.debug(f"Raw STAC URLs string: {stac_urls_str}")
    logger.debug(f"Type of raw STAC URLs string: {type(stac_urls_str)}")

    try:
        stac_urls = json.loads(stac_urls_str)
        logger.debug(f"Parsed STAC URLs: {stac_urls}")
        logger.debug(f"Type of parsed STAC URLs: {type(stac_urls)}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse STAC URLs JSON: {e}")
        sys.exit(1)

    stac_objects = read_stac(stac_urls)
    print_stac_info(stac_objects)
    rewrite_stac(stac_objects, "output_catalog")


if __name__ == "__main__":
    main()