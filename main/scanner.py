from .models import ProjectModel
from .models import SubdomainModel
from scripts.screenshots.screenshot import upload_screenshot
from scripts.subdomains.apis.projectsonar3 import projectsonar_script3

def subdomain_scanner(user_id, project_session):
    subdomains = []
    project_model_instance = ProjectModel.objects.filter(project_user_id=user_id).filter(project_name__iexact=project_session)
    in_scope = project_model_instance.values('in_scope_domains')[0]['in_scope_domains']
    for domain in in_scope:
        subdomains, sub_details = projectsonar_script3(domain)
    project_model_instance.update(subdomains=list(subdomains))

    for subdomain, port, ip, status, response_header in sub_details:
        if ip == None:
            screenshot = None
            ip = 'No IP address'
        if status == '200':
            screenshot = upload_screenshot(subdomain)
        else:
            screenshot = None

        if status == None:
            status = 'Not Applicable'
        if len(response_header) > 0:
            response_header_clean = dict(response_header)
        else:
            response_header_clean = ''
        SubdomainModel.objects.update_or_create(
            subdomain_user_id = user_id,
            project = ProjectModel.objects.get(project_name=project_session),
            hostname = subdomain,
            defaults = {
                'status_code': status,
                'ip_address': ip,
                'screenshot': screenshot,
                'waf': 'Absent',
                'ssl_info': {},
                'header_info': response_header_clean,
                'directories': [],
                'ports': port,
            })
    project_model_instance.update(progress=25)
