import requests
import re
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
