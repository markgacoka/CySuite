## Database Models
### Get all API endpoints:
```
curl -X GET http://localhost:8000/api/

{
  "urls": [
    "api/",
    "api/token/",
    "api/users/",
    "api/user/",
    "api/api-auth/login/",
    "api/api-auth/logout/"
  ]
}
```

### Get all users:
```
curl -X GET http://localhost:8000/api/users/

C:\Users\Gacoka>curl -X GET http://localhost:8000/api/users/
[
  {
    "user_id": "a94fe36c-355c-4156-8cf4-abad477e3280",
    "first_name": "Admin",
    "last_name": "Account",
	...
    "api_token": "0279607f2c7bd041a51de1484a1694f268a29289",
    "badges": [
      "Novice"
    ]
  }
]
```

### Get User Token:
```
curl -X POST http://localhost:8000/api/token/ -d "username=email@example.com&password=foobar"

{"token":"02796...a29289"}
```

### Get Authenticated User Details:
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

### Get Authenticated User Projects:
```
curl -X GET http://localhost:8000/api/user/projects/ -H "Authorization: Token 02796...a29289"

[
  {
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


```json
Subdomains
[
	{
		"Starbucks": {
			"Program": "HackerOne",
			"Progress": 0,
			"In-scope domains": {
				"*.starbucks.com": {
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
							"Not Before": "Oct 10 12:00:00 2021 GMT",
							"Version": "3",
							"OCSP": "http://ocsp.digicert.com",
							"caIssuers": "digicert.com/cert.crt",
							"Country": "US"
						},
						"Screenshot": "starbucks_home.jpg",
						"Headers": {
							"Date": "Mon, 19 Jul 2021 18:24:53 GMT",
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
			}
		} 
	}
]
```

```
Domains
[
	{
		"www.starbucks.com/login": {
			"accepts": ["http", "https"],
			"status": "200",
			"parameters": ["id", "utm-medium"],
			"vulnerabilities": {
				"XSS": {
					"found": true,
					"payload": "PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pgo=",
					"target": "https://www.starbucks.com/login?id="
				},
				"SQL": {
					"found": true,
					"payload": "JyBBTkQgMT0xCg==",
					"target": "https://www.starbucks.com/login?id="
				}
			},
			"notified": true,
			"platform": "Telegram",
		}		
	}
]
```

### User abilities
[ x ] Get all the available user projects
[ x ] Get project details with in-scope domains, project name
- Get subdomains with IP, SSL, DNS, ports
- Get directories, parameters, protocols of subdomains


### Functions
- getUser()
`Permissions: currentuser`
`/api/currentuser/`
```
[PK] user_id:
username:
email:
first_name:
last_name:
date_joined:
last_login_date:
is_admin:
is_premium:
feedback:
profile_image:
beta:
dark:
```

- getAllUsers()
`Permissions: admin`
`/api/allusers/`
```
[:]
[PK] user_id: 
username:
email:
last_login_date:
is_admin:
is_premium:
feedback:
beta:
```

- getProjects()
`Permissions: currentuser`
`/api/projects/`
```
[PK] project_user_id:
project:
program:
in_scope_domains:
progress:
```

- getSubdomains()
`Permissions: currentuser`
`/api/subdomains/<in-scope-domain>`
```
"in_scope_domain": "google.com",

```

- getDirectories()
`Permissions: currentuser`
`/api/directories/<subdomain>`
```
```

TODO: Limit requests sent to API per user