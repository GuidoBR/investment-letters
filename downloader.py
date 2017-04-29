import os
import time
from crawlers.dynamo import Dynamo
from crawlers.berkshirehathaway import Berkshirehathaway
from crawlers.arx import Arx
import requests

def save_letter(pdf, filename, dest_dir):
    path = os.path.join(dest_dir, filename)
    with open(path, 'wb') as fp:
        fp.write(pdf)


def get_letter(link):
    resp = requests.get(link)
    return resp.content


def download_many(letters):
    for letter in letters:
        print("Downloading {} ...".format(letter[0]))
        try:
            pdf = get_letter(letter[1])
            save_letter(pdf, '{}.pdf'.format(letter[0]), letter[2])
        except:
            print("Failed to download letter {}".format(letter[0]))
    return len(letters)

def main():
    t0 = time.time()

    pt = Dynamo("pt")
    en = Dynamo("en")
    bh = Berkshirehathaway()
    arx = Arx()

    print("Starting Dyanmo PT")
    letters = pt.crawl()
    print("Starting Dyanmo EN")
    letters.extend(en.crawl())
    print("Starting Berkshirehathway")
    letters.extend(bh.crawl())
    print("Starting ARX")
    letters.extend(arx.crawl())

    count = download_many(letters)

    elapsed = time.time() - t0
    msg = '\n{} letters downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == "__main__":
    main()
