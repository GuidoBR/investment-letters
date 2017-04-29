import requests
import re
from bs4 import BeautifulSoup

BASE_URL = "https://www.arxinvestimentos.com.br"

class Arx:
    """
    ARX is a financial company located on Brazil. It provides investment letters on it's website. This model helps download that letters.

    >>> arx = Arx()
    >>> arx.get_letters_url()
    'https://www.arxinvestimentos.com.br/InvestmentFunds/ManagementReports'
    >>> arx.get_all_letters_url()
    ['https://www.arxinvestimentos.com.br/InvestmentFunds/ManagementReports']
    """
    def __init__(self):
        self.dest_dir = "letters/arx/"

    def get_letters_url(self):
        return "{}/InvestmentFunds/ManagementReports".format(BASE_URL)

    def get_all_letters_url(self):
        return [self.get_letters_url()]

    def extract_pdf(self, html):
        soup = BeautifulSoup(html, "html.parser")     
        links = soup.find_all('a', href=re.compile(r'(PDF)'))
        return [
                (
                    l.getText(),
                    "{}{}".format(BASE_URL, l['href']),
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
