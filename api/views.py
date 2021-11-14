from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import permissions
from cyauth.models import Account
from .serializers import UsersSerializer, UserSerializer 

from django.conf import settings
from django.urls import URLPattern, URLResolver

urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

class ListUrlView(APIView):
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
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        qs = Account.objects.all()
        serializer = UsersSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})

class UserView(APIView):
    def get(self, request, *args, **kwargs):
        qs = Account.objects.filter(user_id=request.user.user_id)
        serializer = UserSerializer(qs, many=False)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'indent': 2})
    
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
