"""Define parsers for each sections of the website."""

import logging
from abc import ABC, abstractmethod
from itertools import batched
from typing import ClassVar, Self

from bs4.element import ResultSet, Tag


class SectionParser(ABC):
    """Base class for all section parsers."""

    _section: Tag

    def __init__(self: Self, section: Tag) -> None:
        """Initiate SectionParser.

        It needs section as an beautifulsoup.tag to extract informations from.
        """
        self._section = section

    @abstractmethod
    def parse(self: Self) -> list[str]:
        """Parse section and return the list of formatted information."""


class SectionParserDummy(SectionParser):
    """Parser for useless section. It parses nothing."""

    def parse(self: Self) -> list[str]:
        """Parse section and return the list of formatted information."""
        return []


class SectionParserEconomie(SectionParser):
    """Parser for the economie section."""

    def get_all_informations(self: Self) -> ResultSet:
        """Return all usefull informations in the section.

        Returned informations are not formated.
        """

        def _filter(tag: Tag) -> bool:
            """Filter the information for each tag in the economie section."""
            classes_raw = tag.get("class")
            classes: list = list(classes_raw) if classes_raw else []
            return tag.name == "p" and ("source" not in classes)

        if result := self._section.find_all(_filter):
            return result
        message = "No information found !"
        raise ValueError(message)

    def link_number_with_description(self: Self) -> list[str]:
        """Link number with description."""
        zipped: list[tuple[Tag, Tag]] = list(
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
        "climat": SectionParserDummy,
        "labels": SectionParserDummy,
        "politique": SectionParserDummy,
        "cityhall": SectionParserDummy,
        "compare": SectionParserDummy,
    }

    @classmethod
    def get_handled_parsers(cls: type["GetSectionParser"]) -> list[str]:
        """Return the list of handle sections."""
        return list(cls._parsers.keys())

    @classmethod
    def get_parser(
        cls: type["GetSectionParser"],
        section_name: str,
    ) -> type[SectionParser]:
        """Return needed parser for selected section."""
        if section_name not in cls._parsers:
            message: str = f"Parser for {section_name} is not defined."
            logging.warning(message)
            return SectionParserDummy
        return cls._parsers[section_name]
