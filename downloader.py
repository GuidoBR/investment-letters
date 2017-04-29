import os
import time
import requests

from crawlers.dynamo import Dynamo
from crawlers.berkshirehathaway import Berkshirehathaway
from crawlers.arx import Arx

import aiohttp
import aiofiles
import asyncio
import async_timeout

from collections import namedtuple

Letter = namedtuple('Letter', ['filename', 'url', 'directory'])

async def download_letter(session, letter):
    with async_timeout.timeout(10):
        async with session.get(letter.url) as response:
            filename = '{}.pdf'.format(letter.filename)
            path = os.path.join(letter.directory, filename)
            print('Downloading {}'.format(filename))
            async with aiofiles.open(path, 'wb') as f_handle:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    await f_handle.write(chunk)
            return await response.release()

async def main(loop):
    t0 = time.time()

    pt = Dynamo("pt")
    en = Dynamo("en")
    bh = Berkshirehathaway()
    arx = Arx()

    letters = pt.crawl()
    letters.extend(en.crawl())
    letters.extend(bh.crawl())
    # letters.extend(arx.crawl())

    async with aiohttp.ClientSession(loop=loop) as session:
        for l in letters:
            letter = Letter(filename=l[0], url=l[1], directory=l[2])
            await download_letter(session, letter)

    elapsed = time.time() - t0
    msg = '\n{} letters downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
