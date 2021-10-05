from scripts.screenshots.screenshot import upload_screenshot
from scripts.screenshots.screenshot import get_status_code
from celery_progress.backend import ProgressRecorder
from scripts.PortScan.portscan import Portscanner
from .subdomains import subdomain_list
from .models import ProjectModel
from .models import SubdomainModel
from celery import shared_task
import boto3
import re, os
from dotenv import load_dotenv
load_dotenv()

@shared_task(bind=True)
def scan_subdomains(self, user_id, project_session):
    subdomains = []
    project_model_instance = ProjectModel.objects.filter(project_user_id=user_id).filter(project_name__iexact=project_session)
    in_scope = project_model_instance.values('in_scope_domains')[0]['in_scope_domains']
    for domain in in_scope:
        subdomains += list(next(subdomain_list(domain)))
    project_model_instance.update(subdomains=subdomains)

    progress_recorder = ProgressRecorder(self)
    for index, subdomain in enumerate(subdomains):
        portscanner = Portscanner(subdomain)
        port, ip, status, response_header = portscanner.run_scanner(100)
        if ip == None:
            screenshot = None
            ip = 'No IP address'
        if get_status_code(subdomain) == True:
            screenshot = upload_screenshot(subdomain)
        else:
            screenshot = None

        if status == None:
            status = 'Not Applicable'
        if len(response_header) > 0 and type(response_header) == bytes:
            if len(re.findall('\r\n\r\n', response_header.decode())) > 1:
                response_header_clean = str(response_header.decode().split('\r\n\r\n')[-2])
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
        progress_recorder.set_progress(index+1, len(subdomains))
        project_model_instance.update(progress=int((index+1/len(subdomains)* 100)/4))
    return 'Done'
