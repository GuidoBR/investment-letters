import requests
import re
from bs4 import BeautifulSoup

BASE_URL = "http://www.tropicoinvest.com/"

class Tropico:
    """
    Tropico is a financial company located on Brazil. It provides investment letters on it's website. This model helps download that letters.

    >>> tropico = Tropico()
    >>> tropico.get_letters_url()
    'http://www.tropicoinvest.com/downloads-infos/'
    >>> tropico.get_all_letters_url()
    ['http://www.tropicoinvest.com/downloads-infos/']
    """
    def __init__(self):
        self.dest_dir = "letters/tropico/"

    def __str__(self):
        return "Tropico"

    def get_letters_url(self):
        return "{}downloads-infos/".format(BASE_URL)

    def get_all_letters_url(self):
        return ["{}downloads-infos/".format(BASE_URL)]

    def extract_pdf(self, html):
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all('a', href=re.compile(r'(\.pdf)'))
        return [
                (
                    l['href'].rsplit('/', 1)[-1].rsplit('.pdf')[0],
                    "{}".format(l['href']),
                    self.dest_dir
                ) for l in links]

    """
    Return all pdf links for the investment letters
    """
    def crawl(self):
        links = []
        for url in self.get_all_letters_url():
            r = requests.get(url)
            if r.status_code != 200:
                return links
            links.extend(self.extract_pdf(r.text))
        return links

if __name__ == "__main__":
    import doctest
    doctest.testmod()
