import ast
import requests
from main.models import ProjectModel, SubdomainModel
from scripts.screenshots.screenshot import upload_screenshot

def subdomain_scanner(user_id, project_session):
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/octet-stream',
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5 (.NET CLR 3.5.30729)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
        'Keep-Alive': '300',
        'Connection': 'keep-alive'
    }
    project_model_instance = ProjectModel.objects.filter(project_user_id=user_id).filter(project_name__iexact=project_session)
    in_scope = project_model_instance.values('in_scope_domains')[0]['in_scope_domains']
    for domain in in_scope:
        r = requests.get(url = 'https://sonar.omnisint.io/subdomains/{}'.format(domain))
        subdomains = list(set(ast.literal_eval(r.text)))
        project_model_instance.update(subdomains=subdomains)
        if r.status_code == 200:
            for subdomain in subdomains:
                with requests.head('http://' + subdomain, allow_redirects=True, headers=headers) as response:
                    ip_address = None
                    sub_status = response.status_code
                    headers = response.headers
                    total_time = response.elapsed.total_seconds()
                if ip_address == None:
                    ip_address = 'No IP address'
                if sub_status == 200:
                    screenshot = upload_screenshot(subdomain)
                else:
                    screenshot = None
                
                SubdomainModel.objects.update_or_create(
                    subdomain_user_id = user_id,
                    project = ProjectModel.objects.get(project_name=project_session),
                    hostname = subdomain,
                    defaults = {
                        'status_code': sub_status,
                        'ip_address': ip_address,
                        'screenshot': screenshot,
                        'waf': 'Absent',
                        'ssl_info': {},
                        'header_info': headers,
                        'directories': [],
                        'ports': ['80'],
                    }
                )
            project_model_instance.update(progress=int(25))
        return True