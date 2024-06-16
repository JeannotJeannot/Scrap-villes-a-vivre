"""Define parsers for each sections of the website."""

from abc import ABC, abstractmethod
from itertools import batched
from typing import ClassVar, Self

import bs4


class SectionParser(ABC):
    """Base class for all section parsers."""

    _section: bs4.element.Tag

    def __init__(self: Self, section: bs4.element.Tag) -> None:
        """Initiate SectionParser.

        It needs section as an beautifulsoup.tag to extract informations from.
        """
        self._section = section

    @abstractmethod
    def get_all_informations(self: Self) -> bs4.element.ResultSet:
        """Return all usefull informations in the section.

        Returned informations are not formated.
        """

    @abstractmethod
    def link_number_with_description(self: Self) -> list[str]:
        """Format informations."""

    @abstractmethod
    def parse(self: Self) -> list[str]:
        """Parse section and return the list of formatted information."""

class SectionParserEconomie(SectionParser):
    """Parser for the economie section."""

    def get_all_informations(self: Self) -> bs4.element.ResultSet:
        """Do the same as super."""

        def _filter(tag: bs4.element.Tag) -> bool:
            """Filter the information for each tag in the economie section."""
            classes_raw = tag.get("class")
            classes: list = list(classes_raw) if classes_raw else []
            return tag.name == "p" and ("source" not in classes)

        if result := self._section.find_all(_filter):
            return result
        msg = "No information found !"
        raise ValueError(msg)

    def link_number_with_description(self: Self) -> list[str]:
        """Do the same as super."""
        zipped: list[tuple[bs4.element.Tag, bs4.element.Tag]] = list(
            batched(self.get_all_informations(), 2),
        )
        results: list[str] = []
        for number, description in zipped:
            results.append(
                f"{number.string.strip()} {description.string.strip()}",
            )
        return results

    def parse(self: Self) -> list[str]:
        """Do the same as super."""
        return self.link_number_with_description()


class GetSectionParser:
    """Handle the choosing of the section parser."""

    _parsers: ClassVar[dict[str, type[SectionParser]]] = {
        "economie": SectionParserEconomie,
    }

    @classmethod
    def get_handled_parsers(cls: type["GetSectionParser"]) -> list[str]:
        """Return the list of handle sections."""
        return list(cls._parsers.keys())

    @classmethod
    def get_parser(
        cls: type["GetSectionParser"], section_name: str,
    ) -> type[SectionParser]:
        """Return needed parser for selected section."""
        return cls._parsers[section_name]
