import requests
import re
from bs4 import BeautifulSoup

URL_PT = "https://www.arxinvestimentos.com.br/InvestmentFunds/DownloadFilePDF/"
REPORTS_URL = "https://www.arxinvestimentos.com.br/InvestmentFunds/ManagementReports"

def get_reports_url():
    result = requests.get(REPORTS_URL)
    return result.content

def get_last_page_number(html):
    soup = BeautifulSoup(html, "html.parser")
    last_link = soup.find_all('a', href=re.compile("DownloadFilePDF"))[0]["href"]
    return int(last_link.split("/")[-1])

def get_pt_letters_links():
    links = []
    latest = get_last_page_number(get_reports_url())
    for i in range(1, latest):
        links.append('{}{}'.format(URL_PT, i))

    return links
