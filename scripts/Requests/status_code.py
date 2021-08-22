import asyncio
import aiohttp
import time

async def get(url, session):
    try:
        async with session.get(url=url) as response:
            return(response.status)
    except Exception as e:
        resp = 404
        return(resp)
        print(e.__class__)


async def main(urls):
    for idx, url in enumerate(urls):
        if not url.startswith('http://') and not url.startswith('https://'):
            urls[idx] = 'http://' + url
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(url, session) for url in urls])
        return ret

def status_code(subdomains):
    yield asyncio.run(main(subdomains))