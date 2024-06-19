"""Define the parser for the webpage."""

from typing import TYPE_CHECKING, ClassVar, Self

from bs4.element import ResultSet, Tag

from scrap_villes_a_vivre.page_request import get_page

if TYPE_CHECKING:
    from bs4 import BeautifulSoup


class FullPageParser:
    """Parser for balises only."""

    _page: Tag
    _info_balise: ClassVar[set[str]] = {
        "demo-content",
        "bar",
        "dynamic-content",
        "text-content",
        "second-circle-content",
        "card-content",
        "city-crime",
    }

    def __init__(self: Self, page: Tag) -> None:
        """Initiate SectionParser.

        It needs section as an beautifulsoup.tag to extract informations from.
        """
        self._page = page

    def _filter(self: Self, tag: Tag) -> bool:
        """Filter the information for each tag in the economie section."""
        classes_raw: list[str] | str | None = tag.get("class")
        classes: list[str] = list(classes_raw) if classes_raw is not None else []
        return (
            tag.name == "div" and bool(self._info_balise.intersection(classes))
        ) or tag.name == "tr"

    def _get_all_informations(self: Self) -> ResultSet:
        """Return all usefull informations in the section.

        Returned informations are not formated.
        """
        if result := self._page.find_all(self._filter):
            return result
        message = "No information found !"
        raise ValueError(message)

    def parse(self: Self) -> list[str]:
        """Parse section and return the list of formatted information."""
        return [
            " ".join((info.text.replace("\u202f", "").strip().replace(" %", "%")).split())
            for info in self._get_all_informations()
        ]


def get_informations_from_url(page_url: str) -> list[str]:
    """Return informations about one url."""
    page_souped: BeautifulSoup = get_page(page_url)
    return FullPageParser(page_souped).parse()
