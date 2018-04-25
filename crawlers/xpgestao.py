import requests
import re
from bs4 import BeautifulSoup

BASE_URL = "http://www.xpgestao.com.br"
BASE_JSON = "http://www.xpgestao.com.br/api/relatorios?_=1524613313318"

class XPGestao:
    """
    XPGestao is a financial company located on Brazil. It provides investment letters on it's website. This model helps download that letters.

    >>> xp = XPGestao()
    """
    def __init__(self):
        self.dest_dir = "letters/xpgestao/"

    def __str__(self):
        return "XP Gestão"

    """
    Return all pdf links for the investment letters
    """
    def crawl(self):
        r = requests.get(BASE_JSON)
        if r.status_code != 200:
            return []

        json_request = r.json()
        return [
                (
                    "{}".format(letter['Title']).replace("/", "-"),
                    "{}{}".format(BASE_URL, letter['Url']),
                    self.dest_dir
                )
                for letter in json_request['Return']['Documents']
            ]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
