import requests
import re
from bs4 import BeautifulSoup
BASE_URL = "http://www.berkshirehathaway.com"

class Berkshirehathaway:
    """
    Berkshirehathaway is a financial company located on USA, from the investor Warren Buffet. It provides investment letters on it's website. This model helps download that letters.

    >>> bh = Berkshirehathaway()
    >>> bh.get_letters_url()
    'http://www.berkshirehathaway.com/letters/letters.html'
    >>> bh.get_all_letters_url()
    ['http://www.berkshirehathaway.com/letters/letters.html']
    """
    def __init__(self):
        self.dest_dir = "letters/berkshirehathaway/"

    def get_letters_url(self):
        return "{}/letters/letters.html".format(BASE_URL)

    def get_all_letters_url(self):
        return [self.get_letters_url()]

    def extract_pdf(self, html):
        """
        Not all letters are PDF, some are in HTML. TODO
        """
        soup = BeautifulSoup(html, "html.parser")     
        links = soup.find_all('a', href=re.compile(r'(\.pdf)'))
        return [
                (
                    l.getText(),
                    "{}/letters/{}".format(BASE_URL, l['href']),
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
