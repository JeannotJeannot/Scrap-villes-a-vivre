import requests
from bs4 import BeautifulSoup

WEBSITE: str = "https://www.villesavivre.fr/"

town: str = "versailles-78646"

URL: str  = WEBSITE + town

r = requests.get(URL)

soup = BeautifulSoup(r.content, 'html.parser')

a = soup.find_all(name="div", attrs={"data-v-656b94af": ""}, recursive=True)

for i in range(50):
    print(a[i])