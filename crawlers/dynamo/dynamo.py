import requests
import re
from bs4 import BeautifulSoup

BASE_URL = "http://www.dynamo.com.br"

class Dynamo:
    """
    Dynamo is a financial company located on Brazil. It provides investment letters on it's website. This model helps download that letters.

    >>> pt = Dynamo("pt")
    >>> pt.get_letters_url()
    'http://www.dynamo.com.br/pt/cartas-dynamo'
    >>> pt.get_all_letters_url()
    ['http://www.dynamo.com.br/pt/cartas-dynamo?page=1', 'http://www.dynamo.com.br/pt/cartas-dynamo?page=2', 'http://www.dynamo.com.br/pt/cartas-dynamo?page=3', 'http://www.dynamo.com.br/pt/cartas-dynamo?page=4']

    >>> en = Dynamo("en")
    >>> en.get_letters_url()
    'http://www.dynamo.com.br/en/cartas-dynamo'
    >>> en.get_all_letters_url()
    ['http://www.dynamo.com.br/en/cartas-dynamo?page=1', 'http://www.dynamo.com.br/en/cartas-dynamo?page=2', 'http://www.dynamo.com.br/en/cartas-dynamo?page=3', 'http://www.dynamo.com.br/en/cartas-dynamo?page=4']
    """
    def __init__(self, lang):
        self.language = lang
        self.dest_dir = "letters/dynamo/{}/".format(lang)

    def __str__(self):
        return "Dyanmo"

    def get_letters_url(self):
        return "{}/{}/cartas-dynamo".format(BASE_URL, self.language)

    def get_all_letters_url(self):
        return ["{}?page={}".format(self.get_letters_url(), i) for i in range(1, 5)]

    def extract_pdf(self, html):
        soup = BeautifulSoup(html, "html.parser")     
        links = soup.find_all('a', href=re.compile(r'(\.pdf)'))
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
