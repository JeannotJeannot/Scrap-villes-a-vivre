"""Define the parser for the webpage."""

from typing import TYPE_CHECKING

from scrap_villes_a_vivre.page_request import get_page
from scrap_villes_a_vivre.parsers_sections import FullPageParser

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


def get_informations_from_url(page_url: str) -> list[str]:
    """Return informations about one url."""
    page_souped: BeautifulSoup = get_page(page_url)
    return FullPageParser(page_souped).parse()
