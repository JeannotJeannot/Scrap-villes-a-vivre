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


def get_informations_from_list(informations: list[str], information_regex: str) -> str:
    """Return bac+5 for results."""
    r: re.Pattern = re.compile(information_regex)
    for data in informations:
        match: re.Match
        if match := r.match(data):
            return str(match.group("result"))

    return "Not found!"


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
        "Prix médian au m2 d'une maison": r"^(?P<result>\d+) € -?\d+(,\d+)?% Prix médian m2 d'une maison$",
        "Evolution du prix médian au m2 d'une maison": r"^\d+ € (?P<result>-?\d+(,\d+)?%) Prix médian m2 d'une maison$",
        "Cambriolages": r"^Cambriolages (?P<result>\d+) \d+$",
        "Vols automobiles": r"^Vols automobiles (?P<result>\d+) \d+$",
        "Vols de particulier": r"^Vols de particulier (?P<result>\d+) \d+$",
        "Violences physiques": r"^Violences physiques (?P<result>\d+) \d+$",
        "Violences sexuelles": r"^Violences sexuelles (?P<result>\d+) \d+$",
        "Médecin": r"^Médecin (?P<result>.*)$",
        "Dentiste": r"^Dentiste (?P<result>.*)$",
        "Infirmier": r"^Infirmier (?P<result>.*)$",
        "Pharmacie": r"^Pharmacie (?P<result>.*)$",
        "Urgences": r"^Urgences (?P<result>.*)$",
        "Crèche": r"^Crèche (?P<result>.*)$",
        "Ecole maternelle": r"^Ecole maternelle (?P<result>.*)$",
        "Ecole élementaire": r"^Ecole élementaire (?P<result>.*)$",
        "Collège": r"^Collège (?P<result>.*)$",
        "Lycée": r"^Lycée (?P<result>.*)$",
        "Hypermarché": r"^Hypermarché (?P<result>.*)$",
        "Supermarché": r"^Supermarché (?P<result>.*)$",
        "Epicerie": r"^Epicerie (?P<result>.*)$",
        "Station service": r"^Station service (?P<result>.*)$",
        "Bureau de Poste": r"^Bureau de Poste (?P<result>.*)$",
        "Hôtel": r"^Hôtel (?P<result>.*)$",
        "Restaurant": r"^Restaurant (?P<result>.*)$",
        "Boulangerie": r"^Boulangerie (?P<result>.*)$",
        "Cinéma": r"^Cinéma (?P<result>.*)$",
        "Bibliothèque": r"^Bibliothèque (?P<result>.*)$",
        "Aeroport": r"^Aeroport (?P<result>.*)$",
        "Gare SNCF": r"^Gare SNCF (?P<result>.*)$",
        "Voisin 1": r"^(?P<result>.* à \d+(,\d+)? km)$",
        "Logements vacants": r"^(?P<result>\d+(,\d+)?%) Logements vacants$",
        "Résidences principales": r"^(?P<result>\d+(,\d+)?%) Résidences principales$",
        "Résidences secondaires": r"^(?P<result>\d+(,\d+)?%) Résidences secondaires$",
        "Propriétaires": r"^(?P<result>\d+(,\d+)?%) Propriétaires$",
        "1 pièce": r"^(?P<result>\d+(,\d+)?%) 1 pièce$",
        "2 pièces": r"^(?P<result>\d+(,\d+)?%) 2 pièces$",
        "3 pièces": r"^(?P<result>\d+(,\d+)?%) 3 pièces$",
        "4 pièces": r"^(?P<result>\d+(,\d+)?%) 4 pièces$",
        "5 pièces et plus": r"^ 5 pièces et plus$",
        "Crimes et délits": r"^(?P<result>\d+) crimes et délits pour 100 000 habitants.$",
        "Nom": r"^.*\. Le code postal de (?P<result>.+) est \d+\.$",
        "Code postal": r"^.*\. Le code postal de .+ est (?P<result>\d+)\.$",
        "Evolution du nombre d'habitants": r"^(?P<result>-?\d+(,\d+)?%) Entre 2016 et 2021$",
        "Part de maisons": r"^(?P<result>\d+(,\d+)?%) Maisons$",
        "Part d'appartements": r"^(?P<result>\d+(,\d+)?%) Appartements$",
    }
    logging.warning(informations_formatted)
    for name, regex in informations_regex.items():
        logging.warning(
            name
            + "        "
            + get_informations_from_list(informations_formatted, regex),
        )
