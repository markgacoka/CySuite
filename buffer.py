# find . -type d -name __pycache__ -exec rm -r {} \+

import json
import aiohttp
import asyncio
import psycopg2

found = []

async def fb_cert(hostname, conf_path, session):
	global found
	with open('{}/keys.json'.format(conf_path), 'r') as keyfile:
		json_read = keyfile.read()

	json_load = json.loads(json_read)
	fb_key = json_load['facebook']

	if fb_key != None:
		print('[!]' + ' Requesting ' + 'Facebook')
		url = 'https://graph.facebook.com/certificates'
		fb_params = {
			'query': hostname,
    		'fields': 'domains',
    		'access_token': fb_key
		}
		try:
			async with session.get(url, params=fb_params) as resp:
				sc = resp.status
				if sc == 200:
					json_data = await resp.text()
					json_read = json.loads(json_data)
					domains = json_read['data']
					for i in range (0, len(domains)):
						found.extend(json_read['data'][i]['domains'])
				else:
					print('[-]' + ' Facebook Status : ' + str(sc))
		except Exception as e:
			print('[-]' + ' Facebook Exception : ' + str(e))
	else:
		pass

def subdomains(hostname, tout, output, data, conf_path):
	global found
	result = {}

	print('\n' + Y + '[!]' + Y + ' Starting Sub-Domain Enumeration...' + W + '\n')

	loop = asyncio.new_event_loop()
	asyncio.set_event_loop(loop)
	loop.run_until_complete(query(hostname, tout, conf_path))
	loop.close()

	from urllib.parse import urlparse
	found = [item for item in found if item.endswith(hostname)]
	valid = r"^[A-Za-z0-9._~()'!*:@,;+?-]*$"
	import re
	found = [item for item in found if re.match(valid, item)]
	found = set(found)
	total = len(found)

	if len(found) != 0:
		print('\n' + G + '[+]' + C + ' Results : ' + W + '\n')
		for url in found:
			print(G + '[+] ' + C + url)

	print('\n' + G + '[+]' + C + ' Total Unique Sub Domains Found : ' + W + str(total))

	if output != 'None':
		result['Links'] = list(found)
		subd_output(output, data, result, total)

def subd_output(output, data, result, total):
	data['module-Subdomain Enumeration'] = result
	data['module-Subdomain Enumeration'].update({'Total Unique Sub Domains Found': str(total)})


subdomains()

