import requests
from itertools import batched
from bs4 import BeautifulSoup
import bs4
from abc import ABC, abstractmethod
from typing import Self

WEBSITE: str = "https://www.villesavivre.fr/"
town: str = "versailles-78646"
url: str = WEBSITE + town

page_raw: bytes = requests.get(url).content
page_complete: BeautifulSoup = BeautifulSoup(page_raw, "html.parser")


def get_all_sections(page_complete: BeautifulSoup) -> bs4.element.ResultSet:
    if result := page_complete.find_all(
        name="section", class_="city-content", recursive=True
    ):
        return result
    raise ValueError("No section found !")


class SectionParser(ABC):
    _section: bs4.element.Tag

    def __init__(self: Self, section: bs4.element.Tag):
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
        raise ValueError("No information found !")

    def link_number_with_description(self: Self) -> list[str]:
        zipped: list[tuple[bs4.element.Tag, bs4.element.Tag]] = list(
            batched(self.get_all_informations(), 2)
        )
        results: list[str] = []
        for number, description in zipped:
            results.append(
                " ".join((number.string.strip(), description.string.strip()))
            )
        return results

    def parse(self: Self) -> list[str]:
        return self.link_number_with_description()


def get_parser(section_name: str) -> SectionParser:
    parsers: dict[str, SectionParser] = {
        "economie": SectionParserEconomie,
    }
    return parsers[section_name]


sections: bs4.element.ResultSet = get_all_sections(page_complete)
informations: list[str] = []
for section in sections:
    print(section["id"])
    if section["id"] not in [
        "presentation",
        "labels",
        "compare",
        "population",
        "climat",
        "immobilier",
        "politique",
        "cityhall",
        "near-by",
    ]:
        parser: SectionParser = get_parser(section["id"])
        informations.extend(parser(section).parse())
