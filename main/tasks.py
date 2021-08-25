from celery import shared_task
from celery_progress.backend import ProgressRecorder
from scripts.Requests.status_code import status_code
from scripts.IPAddress.get_host import get_ip
from .subdomains import subdomain_list
from .models import ProjectModel
from .models import SubdomainModel
from celery import group

@shared_task(bind=True)
def scan_subdomains(self, user_id, project_session):
    subdomains = []
    
    progress_recorder = ProgressRecorder(self)
    project_model_instance = ProjectModel.objects.filter(project_user_id=user_id).filter(project_name__iexact=project_session)
    project_model_instance.update(subdomains=subdomains, progress=25)

    in_scope = project_model_instance.values('in_scope_domains')[0]['in_scope_domains']
    subdomains += list(next(subdomain_list(in_scope[0])))
    
    for idx, subdomain in enumerate(subdomains):
        subdomain_info = {}
        status = next(status_code(subdomain))
        ip_address = next(get_ip(subdomain))
        subdomain_model = SubdomainModel.objects.update_or_create(
            subdomain_user_id = user_id,
            project = ProjectModel.objects.get(project_name=project_session),
            hostname = subdomain,
            defaults = {        
                'status_code': status,
                'ip_address': ip_address,
                'screenshot': 'None',
                'waf': 'Absent',
                'ssl_info': {},
                'header_info': {},
                'directories': []
            })
        progress_recorder.set_progress(idx+1, len(subdomains))

    return 'Done'
