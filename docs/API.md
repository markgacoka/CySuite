## OAuth Tokens
```
Google:
Client ID: 171222177646-80l7bgb2jcds6c0o1o7akcsciigiv8hi.apps.googleusercontent.com
Secret Key: aR3hAa8UvrMWFw370fPr0c5r

Github
Client ID: 1652501d641cc3f66c9d
Secret Key: 8522743e7aa518fbd292ad538a741db768ae58f5

Gitlab:
Client ID: 65e790baa6e318f5fc5b3ae375a4e4b2ded5c16262fe5fcad5ea1648d63f673d
Secret Key: 28c54c23507c8f80602b62a5d7955ec11b3208726747cb69eb0bfd113a6de4ec
```

## Database Models
### Get all API endpoints:
```
curl -X GET http://localhost:8000/api/

{
  "urls": [
    "api/",
    "api/token/",
    "api/users/",
    "api/user/projects/",
    "api/user/<user_id>/",
    "api/user/<user_id>/projects/",
    "api/user/",
    "api/api-auth/login/",
    "api/api-auth/logout/"
  ]
}
```

### Get User Token:
```
curl -X POST http://localhost:8000/api/token/ -d "username=email@example.com&password=foobar"

{"token":"02796...a29289"}
```

### Get all users:
```
curl -X GET http://localhost:8000/api/users/

[
  {
    "user_id": "6aabf480-a7bc-4f38-9d6f-102b3342f645",
    "first_name": "Admin",
    "last_name": "Account",
    "username": "admin",
	...
    "hide_email": true,
    "feedback": "",
    "api_token": "0ce6d626af6450d6eaf87b0d8fb1b2ad96866c76",
    "badges": [
      "Novice"
    ]
  },
  {
    "user_id": "9c2374e0-8649-4289-a98c-b7e5d0a0fc14",
    "first_name": "Gacoka",
    "last_name": "Mbui",
    "username": "markgacoka",
	...
    "hide_email": true,
    "feedback": "",
    "api_token": "eb2ac4cb0a594b85a1079069a7b1926710b17217",
    "badges": [
      "Novice"
    ]
  }
]
```

### Get specific user by user_id:
```
curl -X GET http://localhost:8000/api/user/6aabf480-a7bc-4f38-9d6f-102b3342f645/

[
  {
    "user_id": "6aabf480-a7bc-4f38-9d6f-102b3342f645",
    "first_name": "Admin",
    "last_name": "Account",
    "username": "admin",
	...
    "is_premium": true,
    "hide_email": true,
    "feedback": "",
    "api_token": "0ce6d626af6450d6eaf87b0d8fb1b2ad96866c76",
    "badges": [
      "Novice"
    ]
  }
]
```

### Get specific user projects by user_id:
```
curl -X GET http://localhost:8000/api/user/6aabf480-a7bc-4f38-9d6f-102b3342f645/projects/

[
  {
    "project_user_id": "9c2374e0-8649-4289-a98c-b7e5d0a0fc14",
    "project_name": "Project 1 - Gacoka",
    "program": "HackerOne",
    "in_scope_domains": [
      "example.com"
    ],
    "progress": 0,
    "subdomains": []
  }
]
```

### Get User Information using Token Authentication:
```
curl -X GET http://localhost:8000/api/user/ -H "Authorization: Token 02796...a29289"

{
  "user_id": "a94fe36c-355c-4156-8cf4-abad477e3280",
  "first_name": "Admin",
  "last_name": "Account",
  "username": "admin",
	...
  "api_token": "0279607f2c7bd041a51de1484a1694f268a29289",
  "badges": [
    "Novice"
  ]
}
```


### Get Authenticated User Projects using Token Authentication:
```
curl -X GET http://localhost:8000/api/user/projects/ -H "Authorization: Token 02796...a29289"

[
  {
    "project_user_id": "a94fe36c-355c-4156-8cf4-abad477e3280",
    "project_name": "Project 1",
    "program": "HackerOne",
    "in_scope_domains": [
      "markgacoka.com"
    ],
    "progress": 0,
    "subdomains": []
  }
]
```

### Delete Specific User
```
curl -X DELETE http://localhost:8000/api/user/ea678f14-8df2-4f3b-9ae6-b0c1868337b8/

{
  "success": "true"
}
```

------------------------------------------------------------------------------

### In-scope Domain Scan Information
```
curl -X GET http://localhost:8000/api/in-scope/markgacoka.com/
```
```json
[
  {
	"markgacoka.com": {
		"sub.starbucks.com": {
			"Status": "200",
			"IP": "102.32.4.3",
			"Server": "Apache",
			"WAF": "Cloudflare",
			"SSL Information": {
				"Organization": "CloudFlare, Inc.",
				"Common Name": "sni.cloudflaressl.com",
				"Serial Number": "04E3283B3...8F2D7049834",
				"Not After": "Oct 10 00:00:00 2020 GMT",
				"Not Before": "Oct 10 12:00:00 2022 GMT",
				"Version": "3",
				"OCSP": "http://ocsp.digicert.com",
				"caIssuers": "digicert.com/cert.crt",
				"Country": "US"
			},
			"Screenshot": "starbucks_home.jpg",
			"Headers": {
				"Date": "Mon, 19 Jul 2022 18:24:53 GMT",
				"Content-Type": "text/html",
				"Transfer-Encoding": "chunked",
				"Connection": "keep-alive",
				"Last-Modified": "Fri, 09 Oct 2020",
				"Vary": "Accept-Encoding",
				"CF-Cache-Status": "DYNAMIC",
				"Server": "cloudflare",
				"CF-RAY": "6715fd3caacf4fbd-JNB",
				"Content-Encoding": "gzip"
			},
			"ASN": "103342",
			"DNS Records": {
				"A": "104.21.6.77",
				"A": "172.67.134.156",
				"MX": "_dc-mx.e4730ef3a4d3.markgacoka.com",
				"NS": "karina.ns.cloudflare.com",
				"NS": "jason.ns.cloudflare.com",
				"AAAA": "2606:4700:3036::6815:64d",
				"AAAA": "2606:4700:3036::ac43:869c",
				"SOA": "jason.ns.cloudflare.com",
				"TXT": "v=spf1 ip4:145.239.244.59 +a +mx",
				"TXT": "ca3-8cbd58825b85479ca878b1a357e",
			},
			"Ports": ["80", "443"],
			"Domains": ["www.starbucks.com"] 
		}
	}
  }
]
```

### Domain Information
```
curl -X GET http://localhost:8000/api/domain/markgacoka.com%2Flogin%2F
```
```json
[
  {
	"markgacoka.com/login/": {
		"accepts": ["http", "https"],
		"status": "200",
		"parameters": ["id", "utm-medium"],
		"vulnerabilities": {
			"XSS": {
				"found": true,
				"payload": "PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pgo=",
				"target": "https://markgacoka.com/login?id="
			},
			"SQL": {
				"found": true,
				"payload": "JyBBTkQgMT0xCg==",
				"target": "https://markgacoka.com/login?id="
			}
		},
		"notified": true,
		"platform": "Telegram",
		}
  }
]
```

### Functions
getUserToken()
`Permissions: currentuser, admin`
`Authentication: True`
`/api/user/`
```
token
```

getCurrentUser()
`Permissions: currentuser, admin`
`Authentication: True`
`/api/token/`
```
[PK] user_id:
first_name
last_name
username
occupation
email
image
date_joined
last_login
is_admin
is_premium
hide_email
feedback
api_token
badges
```

- getAllUsers()
`Permissions: admin`
`Authentication: True`
`/api/users/`
```
[PK] user_id:
first_name
last_name
username
occupation
email
image
date_joined
last_login
is_admin
is_premium
hide_email
feedback
api_token
badges
```

- getUserProjects()
`Permissions: currentuser`
`Authentication: True`
`/api/user/projects/`
```
[PK] project_user_id:
project_name
program
in_scope_domains
progress
subdomains
```

- getSubdomains()
`Permissions: currentuser`
`/api/api/in-scope/<in-scope-domain>/`
```
[PK] in-scope-domain:
subdomain
status
ip_address
server
waf
ssl_info
screenshot
headers
asn
dns
ports
domains
```

- getDirectories()
`Permissions: currentuser`
`/api/directories/<subdomain>`
```
[PK] domains[i]
accepts
status
parameters
vulnerabilities:
	found
	payload
	target_url
notified
platform
```

### User abilities
[x] Get all the available user projects
[x] Get project details with in-scope domains, project name
TODO: Limit requests sent to API per user
TODO: Get subdomains with IP, SSL, DNS, ports.
TODO: Get directories, parameters, protocols of subdomains.