"""Read website and parse its content."""

import logging
import re
from dataclasses import dataclass
from typing import Self

from scrap_villes_a_vivre.parser_page import get_informations_from_url

WEBSITE: str = "https://www.villesavivre.fr/"


@dataclass
class TownInformations:
    """Informations about a particular town."""

    url_suffix: str

    @property
    def url(self: Self) -> str:
        """Return url for this town."""
        return WEBSITE + self.url_suffix


def get_informations_from_list(informations: list[str], information_regex:str) -> str:
    """Return bac+5 for results."""
    r: re.Pattern = re.compile(information_regex)
    for data in informations:
        match: re.Match
        if match := r.match(data):
            return str(match.group("result"))

    error_message: str = "Not found!"
    raise ValueError(error_message)


if __name__ == "__main__":
    versailles: TownInformations = TownInformations("versailles-78646")
    informations_formatted = get_informations_from_url(versailles.url)
    informations_regex: dict[str, str] = {
        "Population 0-14 ans": r"^(?P<result>\d+(,\d+)?%) Population 0-14 ans$",
        "Population 15-29 ans": r"^(?P<result>\d+(,\d+)?%) Population 15-29 ans$",
        "Population 30-44 ans": r"^(?P<result>\d+(,\d+)?%) Population 30-44 ans$",
        "Population 45-59 ans": r"^(?P<result>\d+(,\d+)?%) Population 45-59 ans$",
        "Population 60-74 ans": r"^(?P<result>\d+(,\d+)?%) Population 60-74 ans$",
        "Population 75-89 ans": r"^(?P<result>\d+(,\d+)?%) Population 75-89 ans$",
        "Population 90 ans et +": r"^(?P<result>\d+(,\d+)?%) Population 90 ans et \+$",
        "Sans diplôme": r"^(?P<result>\d+(,\d+)?%) Sans diplôme$",
        "Brevet des collèges": r"^(?P<result>\d+(,\d+)?%) Brevet des collèges$",
        "CAP / BEP": r"^(?P<result>\d+(,\d+)?%) CAP / BEP$",
        "Baccalauréat, brevet professionnel": r"^(?P<result>\d+(,\d+)?%) Baccalauréat, brevet professionnel$",
        "Bac +2 à Bac +4": r"^(?P<result>\d+(,\d+)?%) Bac \+2 à Bac \+4$",
        "Bac +3 ou Bac +4": r"^(?P<result>\d+(,\d+)?%) Bac \+3 ou Bac \+4$",
        "Bac +5 et plus": r"^(?P<result>\d+(,\d+)?%) Bac \+5 et plus$",
        "Couverture en très haut débit": r"^(?P<result>\d+(,\d+)?%) couverture en très haut débit \(fibre\)$",
        "Taux de chômage": r"^(?P<result>\d+(,\d+)?%) Taux de chômage$",
        "Revenu médian": r"^(?P<result>\d+(,\d+)?) € Revenu médian$",
        "Taux de création d'entreprises": r"^(?P<result>\d+(,\d+)?%) Taux de création d'entreprises$",
        "Prix médian au m2 d'un appartement": r"^(?P<result>\d+) € -?\d+(,\d+)?% Prix médian m2 d'un appartement$",
        "Evolution du prix médian au m2 d'un appartement": r"^\d+ € (?P<result>-?\d+(,\d+)?%) Prix médian m2 d'un appartement$",
    }
    logging.warning(informations_formatted)
    for name, regex in informations_regex.items():
        logging.warning(name +"        " +get_informations_from_list(informations_formatted, regex))
