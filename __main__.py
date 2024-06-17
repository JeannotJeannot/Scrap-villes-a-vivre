"""Read website and parse its content."""

import logging

from scrap_villes_a_vivre.parser_page import get_informations_from_url

if __name__ == "__main__":
    WEBSITE: str = "https://www.villesavivre.fr/"
    town: str = "versailles-78646"
    url: str = WEBSITE + town
    informations_formatted = get_informations_from_url(url)

    logging.warning(informations_formatted)
