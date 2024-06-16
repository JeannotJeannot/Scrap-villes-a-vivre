"""Read website and parse its content."""

import bs4
import requests
from bs4 import BeautifulSoup

from .parsers_sections import GetSectionParser, SectionParser

WEBSITE: str = "https://www.villesavivre.fr/"
town: str = "versailles-78646"
url: str = WEBSITE + town

page_raw: bytes = requests.get(url, timeout=100).content
page_analysed: BeautifulSoup = BeautifulSoup(page_raw, "html.parser")


def get_all_sections(page_analysed: BeautifulSoup) -> bs4.element.ResultSet:
    """Return all sections usefull in the web page."""
    if result := page_analysed.find_all(name="section", class_="city-content"):
        return result
    msg = "No section found !"
    raise ValueError(msg)


sections: bs4.element.ResultSet = get_all_sections(page_analysed)
informations: list[str] = []
for section in sections:
    if section["id"] in GetSectionParser.get_handled_parsers():
        parser: type[SectionParser] = GetSectionParser.get_parser(section["id"])
        informations.extend(parser(section).parse())
