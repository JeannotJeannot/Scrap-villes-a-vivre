"""Read website and parse its content."""
from abc import ABC, abstractmethod
from itertools import batched
from typing import ClassVar, Self

import bs4


class SectionParser(ABC):
    _section: bs4.element.Tag

    def __init__(self: Self, section: bs4.element.Tag) -> None:
        self._section = section

    @abstractmethod
    def get_all_informations(self: Self) -> bs4.element.ResultSet:
        pass

    @abstractmethod
    def link_number_with_description(self: Self) -> list[str]:
        pass

    @abstractmethod
    def parse(self: Self) -> list[str]:
        pass


class SectionParserEconomie(SectionParser):
    def get_all_informations(self: Self) -> bs4.element.ResultSet:
        def _filter(tag: bs4.element.Tag) -> bool:
            classes_raw = tag.get("class")
            classes: list = list(classes_raw) if classes_raw else []
            return tag.name == "p" and ("source" not in classes)

        if result := self._section.find_all(_filter):
            return result
        msg = "No information found !"
        raise ValueError(msg)

    def link_number_with_description(self: Self) -> list[str]:
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
        return self.link_number_with_description()


class GetSectionParser:

    _parsers: ClassVar[dict[str, type[SectionParser]]]= {
            "economie": SectionParserEconomie,
        }

    @classmethod
    def get_handled_parsers(cls:"GetSectionParser") -> list[str]:
        return list(cls._parsers.keys())

    @classmethod
    def get_parser(cls:"GetSectionParser", section_name: str) -> SectionParser:
        return cls._parsers[section_name]
