"""Define the parser for the webpage."""

from abc import ABC, abstractmethod
from typing import Self

from bs4 import BeautifulSoup
from bs4.element import ResultSet


class PageParser(ABC):
    """Base class for all page parsers."""

    _page: BeautifulSoup

    def __init__(self: Self, page: BeautifulSoup) -> None:
        """Initiate PageParser.

        It needs page as an beautifulsoup to extract informations from.
        """
        self._page = page

    @abstractmethod
    def get_all_informations(self: Self) -> ResultSet:
        """Return all usefull informations in the section.

        Returned informations are not formated.
        """
