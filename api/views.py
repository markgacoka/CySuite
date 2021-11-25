from django.http import JsonResponse

from cyauth.models import Account
from main.models import ProjectModel

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.urls import URLPattern, URLResolver
from rest_framework.decorators import permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
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
        print(serializer.data)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})

class UserView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})

    # @action(methods=['delete'], detail=False, url_path='api/user/(?P<user_id>\w+)')
    def delete(self, request, user_id):
        Account.objects.filter(user_id__iexact=user_id).delete()
        return JsonResponse({"success":"true"}, status=202)

class ProjectView(APIView):
    @authentication_classes((TokenAuthentication,))
    @permission_classes((IsAuthenticated,))
    def get(self, request):
        try:
            qs = ProjectModel.objects.filter(project_user_id=request.user.user_id)
        except ProjectModel.DoesNotExist:
            qs = ProjectModel.objects.none()
        serializer = ProjectSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})