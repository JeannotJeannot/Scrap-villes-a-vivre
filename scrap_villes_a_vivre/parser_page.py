"""Define the parser for the webpage."""

import logging
from typing import Self

import bs4
from bs4 import BeautifulSoup

from scrap_villes_a_vivre.page_request import get_page
from scrap_villes_a_vivre.parsers_sections import GetSectionParser, SectionParser


class PageParser:
    """Base class for all page parsers."""

    page: BeautifulSoup

    def __init__(self: Self, page: BeautifulSoup) -> None:
        """Initiate PageParser.

        It needs page as an beautifulsoup to extract informations from.
        """
        self.page = page

    def get_all_sections(self: Self) -> bs4.element.ResultSet:
        """Return all sections usefull in the web page."""
        if result := self.page.find_all(name="section"):
            return result
        message: str = "No section found !"
        raise ValueError(message)

    def get_informations(self: Self) -> list[str]:
        """Return informations about one page."""
        sections: bs4.element.ResultSet = self.get_all_sections()
        informations: list[str] = []
        for section in sections:
            message: str = f"Handling {section['id']}"
            logging.warning(message)
            parser: type[SectionParser] = GetSectionParser.get_parser(section["id"])
            informations.extend(parser(section).parse())

        return informations


def get_informations_from_url(page_url: str) -> list[str]:
    """Return informations about one url."""
    page_souped: BeautifulSoup = get_page(page_url)
    return PageParser(page_souped).get_informations()
