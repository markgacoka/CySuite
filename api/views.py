import json
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

def home(request):
    response = json.dumps([{}])
    return HttpResponse(response, content_type='text/json')

class TestView(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            'username': 'admin',
            'years_active': 10
        }
        return Response(data)