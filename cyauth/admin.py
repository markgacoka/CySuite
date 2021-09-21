from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from cyauth.models import Account
from cyauth.models import UserProfile


class AccountAdmin(UserAdmin):
    list_display = ('email', 'username', 'given_name', 'family_name', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('user_id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile)