import aiohttp
import asyncio
import ast

async def fetch(session, url):
    async with session.get(url) as response:
        return response.status, await response.text(), response.headers

async def main(url):
    async with aiohttp.ClientSession() as session:
        output = []
        status, html, _, = await fetch(session, 'https://sonar.omnisint.io/subdomains/{}'.format(url))
        if status == 200:
            subdomains_lst = set(ast.literal_eval(html))

            for subdomain in subdomains_lst:
                sub_status, _, headers = await fetch(session, 'http://' + subdomain)
                output.append([subdomain, ['80'], '127.0.0.1', str(sub_status), headers]) #subdomain, status, ports, ip_address, screenshot, server, WAF, SSL, header_info
            return subdomains_lst, output
        return None, []

def projectsonar_script3(domain):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(main(domain))