from celery_progress.backend import ProgressRecorder
from scripts.Requests.status_code import status_code
from scripts.IPAddress.get_host import get_ip
from scripts.PortScan.misc import Portscanner
from .subdomains import subdomain_list
from .models import ProjectModel
from .models import SubdomainModel
from celery import shared_task


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
        response_header = {}
        portscanner = Portscanner(subdomain)
        port, ip, status, response = portscanner.run_scanner(100)
        if len(response) > 0:
            response_header[response[0]] = response_header.get(response[0], response[1])
            for header in response[2:]:
                if len(header) > 0 and ":" in header:
                    temp = header.split(":", 1)
                    response_header[temp[0]] = temp[1]
        SubdomainModel.objects.update_or_create(
            subdomain_user_id = user_id,
            project = ProjectModel.objects.get(project_name=project_session),
            hostname = subdomain,
            defaults = {        
                'status_code': status,
                'ip_address': ip,
                'screenshot': 'None',
                'waf': 'Absent',
                'ssl_info': {},
                'header_info': response_header,
                'directories': [],
                'ports': port,
            })
        progress_recorder.set_progress(index+1, len(subdomains))
        project_model_instance.update(progress=int((index+1/len(subdomains)* 100)/4))
    return 'Done'
