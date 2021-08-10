from django.db import models
from cyauth.models import Account
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

class Transaction(models.Model):
    user_account = models.TextField(max_length=30, unique=False, null=False, default='None')
    given_name = models.TextField(max_length=50, blank=True, null=True)
    last_name = models.TextField(max_length=50, blank=True, null=True)
    payer_email = models.EmailField(max_length=254, blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    currency = models.TextField(max_length=10, blank=True, null=True)
    status = models.TextField(max_length=254, blank=True, null=True)
    transaction_code = models.TextField(max_length=50, blank=True, null=True, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)

class Newsletter(models.Model):
    subscriber = models.EmailField(max_length=254, blank=True, null=True)

class ProjectModel(models.Model):
    project_user = models.OneToOneField(Account, primary_key=True, related_name='project', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=30, unique=False, null=False, blank=True)
    program = models.TextField(max_length=30, unique=False, null=False, blank=False)
    in_scope_domains = ArrayField(models.CharField(max_length=250, blank=True), default=list)

    class Meta():
        db_table = 'project'
        verbose_name = _('project')
        verbose_name_plural = _('projects')

    def __str__(self):
        return self.project_user.name + 'Project'