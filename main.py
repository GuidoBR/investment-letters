import os
import time
import requests
import json

from crawlers.dynamo import Dynamo
from crawlers.berkshirehathaway import Berkshirehathaway
from crawlers.arx import Arx
from crawlers.tropico import Tropico
from crawlers.xpgestao import XPGestao

from collections import namedtuple

Letter = namedtuple('Letter', ['filename', 'url', 'directory'])

def get_all_letters():
    # pt = Dynamo("pt")
    # en = Dynamo("en")
    # bh = Berkshirehathaway()
    # arx = Arx()
    # tropico = Tropico()
    xp = XPGestao()
    letters = xp.crawl()

    # letters = pt.crawl()
    # letters.extend(en.crawl())
    # letters.extend(bh.crawl())
    # letters.extend(arx.crawl())
    # letters.extend(tropico.crawl())
    # letters.extend(xp.crawl())
    return letters

def get_xp_gestao():
    xp = XPGestao()
    letters = xp.crawl()
    return json.dumps({'xp_gestao': letters})


if __name__ == "__main__":
    print(get_xp_gestao())
