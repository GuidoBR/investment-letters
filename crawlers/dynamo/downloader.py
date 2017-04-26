import os
import time
import dynamo
import requests

BASE_URL = "http://www.dynamo.com.br/"
DEST_DIR = "letters/dynamo/pt/"

def save_letter(pdf, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(pdf)


def get_letter(link):
    url = '{}/{}'.format(BASE_URL, link)
    resp = requests.get(url)
    return resp.content


def download_many(letters):
    for letter in letters:
        print("Downloading {} ...".format(letter[0]))
        pdf = get_letter(letter[1])
        save_letter(pdf, '{}.pdf'.format(letter[0]))
    return len(pt_letters)

def main():
    t0 = time.time()
    letters = dynamo.get_pt_letters_links()
    count = download_many(letters)
    elapsed = time.time() - t0
    msg = '\n{} letters downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == "__main__":
    main()
