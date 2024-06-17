"""Read page from website."""

import requests
from bs4 import BeautifulSoup


def get_page(page_url: str) -> BeautifulSoup:
    """Return parsed page."""
    page_raw: bytes = requests.get(page_url, timeout=100).content
    return BeautifulSoup(page_raw, "html.parser")
