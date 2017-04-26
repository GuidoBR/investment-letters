import requests
import re
import os
import time
from bs4 import BeautifulSoup

url_pt = "http://www.dynamo.com.br/pt/cartas-dynamo"
BASE_URL = "http://www.dynamo.com.br/"
DEST_DIR = "letters/dynamo/pt/"

def get_all_pdfs_links(html):
    soup = BeautifulSoup(html, "html.parser")     
    links = soup.find_all('a', href=re.compile(r'(\.pdf)'))
    return [(l.getText(), l['href']) for l in links]

def get_last_page_number(html):
    return 4 # TODO

def get_pt_letters_links():
    links = []
    latest = get_last_page_number('TODO')
    for i in range(1, latest):
        r = requests.get('{}?page={}'.format(url_pt, i))
        if r.status_code != 200:
           return links

        links.extend(get_all_pdfs_links(r.text))

    return links

def save_letter(pdf, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(pdf)


def get_letter(link):
    url = '{}/{}'.format(BASE_URL, link)
    resp = requests.get(url)
    return resp.content

def download_many():
    pt_letters = get_pt_letters_links()
    for letter in pt_letters:
        print("Downloading {} ...".format(letter[0]))
        pdf = get_letter(letter[1])
        save_letter(pdf, '{}.pdf'.format(letter[0]))
    return len(pt_letters)

def main():
    t0 = time.time()
    count = download_many()
    elapsed = time.time() - t0
    msg = '\n{} letters downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == "__main__":
    main()
