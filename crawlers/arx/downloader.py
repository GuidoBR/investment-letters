import os
import time
import arx
from urllib.request import urlopen

DEST_DIR = "letters/arx/pt/"

def save_letter(pdf, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(pdf)


def get_letter(url):
    resp = urlopen(url)
    return resp.read()


def download_many(letters):
    for letter in letters:
        letter_num = letter.split("/")[-1]
        print("Downloading {} ...".format(letter_num))
        try:
            pdf = get_letter(letter)
            save_letter(pdf, '{}.pdf'.format(letter_num))
        except:
            print("Failed to download letter {}".format(letter_num))
    return len(letters)

def main():
    t0 = time.time()
    letters = arx.get_pt_letters_links()
    count = download_many(letters)
    elapsed = time.time() - t0
    msg = '\n{} letters downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == "__main__":
    main()
