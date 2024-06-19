"""Define parsers for each sections of the website."""

from typing import ClassVar, Self

from bs4.element import ResultSet, Tag


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
            " ".join((info.text.strip()).split())
            for info in self._get_all_informations()
        ]
