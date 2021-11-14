from django.contrib import admin

from main.models import ProjectModel
from main.models import WordlistModel
from main.models import Newsletter

admin.site.register(Newsletter)
admin.site.register(ProjectModel)
admin.site.register(WordlistModel)
