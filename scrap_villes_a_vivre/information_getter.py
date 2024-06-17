"""Get all informations for a page."""

import logging

import bs4
import requests
from bs4 import BeautifulSoup

from scrap_villes_a_vivre.parsers_sections import GetSectionParser, SectionParser


def get_page(page_url: str) -> BeautifulSoup:
    """Return parsed page."""
    page_raw: bytes = requests.get(page_url, timeout=100).content
    return BeautifulSoup(page_raw, "html.parser")


def get_all_sections(page: BeautifulSoup) -> bs4.element.ResultSet:
    """Return all sections usefull in the web page."""
    if result := page.find_all(name="section", class_="city-content"):
        return result
    message: str = "No section found !"
    raise ValueError(message)


def get_informations_from_page(page: BeautifulSoup) -> list[str]:
    """Return informations about one page."""
    sections: bs4.element.ResultSet = get_all_sections(page)
    informations: list[str] = []
    for section in sections:
        if section["id"] in GetSectionParser.get_handled_parsers():
            message: str = f"Handling {section['id']}"
            logging.warning(message)
            parser: type[SectionParser] = GetSectionParser.get_parser(section["id"])
            informations.extend(parser(section).parse())
        else:
            message: str = f"KO {section['id']}"
            logging.warning(message)
    return informations


def get_informations_from_url(page_url: str) -> list[str]:
    """Return informations about one url."""
    page_souped: BeautifulSoup = get_page(page_url)
    return get_informations_from_page(page_souped)
