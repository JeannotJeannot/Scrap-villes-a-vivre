"""Define parsers for each sections of the website."""

import logging
from abc import ABC, abstractmethod
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


class SectionParserTables(SectionParser):
    """Parser for tables only."""

    def _get_all_informations(self: Self) -> ResultSet:
        """Return all usefull informations in the section.

        Returned informations are not formated.
        """
        if result := self._section.find_all(name="tr"):
            return result
        message = "No information found !"
        raise ValueError(message)

    def parse(self: Self) -> list[str]:
        """Parse section and return the list of formatted information."""
        return [
            " ".join((info.text.strip()).split())
            for info in self._get_all_informations()
        ]

class SectionParserServices(SectionParserTables):
    """Parser for Services only."""
class SectionParserBalises(SectionParser):
    """Parser for balises only."""

    _info_balise: ClassVar[set[str]]

    def _filter(self: Self, tag: Tag) -> bool:
        """Filter the information for each tag in the economie section."""
        classes: list[str] = tag.get("class") if tag.get("class") else []
        return tag.name == "div" and (self._info_balise.intersection(classes))

    def _get_all_informations(self: Self) -> ResultSet:
        """Return all usefull informations in the section.

        Returned informations are not formated.
        """
        if result := self._section.find_all(self._filter):
            return result
        message = "No information found !"
        raise ValueError(message)

    def parse(self: Self) -> list[str]:
        """Parse section and return the list of formatted information."""
        return [
            " ".join((info.text.strip()).split())
            for info in self._get_all_informations()
        ]


class SectionParserPopulation(SectionParserBalises):
    """Parser for population section."""

    _info_balise: ClassVar[set[str]] = {"demo-content"}


class SectionParserPresentation(SectionParserBalises):
    """Parser for Presentation section."""

    _info_balise: ClassVar[set[str]] = {"dynamic-content"}


class SectionParserEconomie(SectionParserBalises):
    """Parser for Economie section."""

    _info_balise: ClassVar[set[str]] = {"text-content"}


class SectionParserImmobilier(SectionParserBalises):
    """Parser for Economie section."""

    _info_balise: ClassVar[set[str]] = {"second-circle-content", "card-content"}


class SectionParserSecurite(SectionParserBalises):
    """Parser for Economie section."""

    _info_balise: ClassVar[set[str]] = {"city-crime"}


class GetSectionParser:
    """Handle the choosing of the section parser."""

    _parsers: ClassVar[dict[str, type[SectionParser]]] = {
        "economie": SectionParserEconomie,
        "population": SectionParserPopulation,
        "presentation": SectionParserPresentation,
        "immobilier": SectionParserImmobilier,
        "securite": SectionParserSecurite,
        "services":  SectionParserServices,
        "climat": SectionParserDummy,
        "labels": SectionParserDummy,
        "politique": SectionParserDummy,
        "cityhall": SectionParserDummy,
        "compare": SectionParserDummy,
        "reviews": SectionParserDummy,
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
