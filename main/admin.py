from django.contrib import admin

from main.models import ProjectModel
from main.models import PayloadModel

admin.site.register(ProjectModel)
admin.site.register(PayloadModel)
