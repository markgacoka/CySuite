from django.http import JsonResponse

from cyauth.models import Account
from main.models import ProjectModel

from django.conf import settings
from rest_framework.views import APIView
from django.urls import URLPattern, URLResolver
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UsersSerializer, UserSerializer, ProjectSerializer

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

class ListUrlView(APIView):
    permission_classes = (AllowAny,)
    def list_urls(self, lis, acc=None):
        if acc is None: acc = []
        if not lis: return
        l = lis[0]
        if isinstance(l, URLPattern):
            if acc[0] == 'api/':
                yield acc + [str(l.pattern)]
        elif isinstance(l, URLResolver):
            yield from self.list_urls(l.url_patterns, acc + [str(l.pattern)])
        yield from self.list_urls(lis[1:], acc)

    def get(self, request, *args, **kwargs):
        url_result = []
        for p in self.list_urls(urlconf.urlpatterns):
            url_result.append(''.join(p))

        return JsonResponse({'urls': url_result}, json_dumps_params={'indent': 2})

class UsersView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        qs = Account.objects.all()
        serializer = UsersSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})

class UserView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, user_id):
        qs = Account.objects.filter(user_id__iexact=user_id)
        serializer = UserSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})
    
    def delete(self, request, user_id):
        Account.objects.filter(user_id__iexact=user_id).delete()
        return JsonResponse({"success":"true"}, status=202)

class ProjectView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, user_id):
        qs = ProjectModel.objects.filter(project_user_id=user_id)
        serializer = ProjectSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})

class AuthenticatedUser(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})

class AuthenticatedProject(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            qs = ProjectModel.objects.filter(project_user=request.user)
        except ProjectModel.DoesNotExist:
            qs = ProjectModel.objects.none()
        serializer = ProjectSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})

from scripts.screenshots.screenshot import upload_screenshot
import requests
import json
import ast
class SubdomainView(APIView):
    def __init__(self):
        self.output = {}
        self.details = {}
    def run_script(self, request, in_scope_domain):
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
        r = requests.get(url = 'https://sonar.omnisint.io/subdomains/{}'.format(in_scope_domain))
        subdomains = list(set(ast.literal_eval(r.text)))
        if r.status_code == 200:
            for subdomain in subdomains:
                with requests.head('http://' + subdomain, allow_redirects=True, headers=headers) as response:
                    sub_status = response.status_code
                    headers = response.headers
                    total_time = response.elapsed.total_seconds()
                self.details['status'] = self.details.get('status', sub_status)
                self.details['headers'] = self.details.get('headers', headers)
                self.details['total_time'] = self.details.get('total_time', total_time)
                self.output[subdomain] = self.details
        return json.dumps(self.output, indent=2, sort_keys=True, default=str)

    permission_classes = (AllowAny,)
    def get(self, request, in_scope_domain):
        output = self.run_script(request, in_scope_domain)
        output = dict(ast.literal_eval(output))
        return JsonResponse(output, safe=False, json_dumps_params={'indent': 2})