from django.contrib import admin

from main.models import ProjectModel
from main.models import PayloadModel
from main.models import WordlistModel

admin.site.register(ProjectModel)
admin.site.register(PayloadModel)
admin.site.register(WordlistModel)
