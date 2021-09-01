import uuid
from django.db import models
from jsonfield import JSONField
from django.conf import settings
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

    class Meta():
        db_table = 'payments'

class Newsletter(models.Model):
    subscriber = models.EmailField(max_length=254, blank=True, null=True, unique=True)

    class Meta():
        db_table = 'periodical'
        verbose_name = _('periodical')
        verbose_name_plural = _('periodicals')

    def __str__(self):
        return self.subscriber + 'Newsletter'

class ProjectModel(models.Model):
    project_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="projects", on_delete=models.CASCADE)
    project_name = models.CharField(max_length=30, unique=False, null=False, blank=True)
    program = models.TextField(max_length=30, unique=False, null=False, blank=False)
    in_scope_domains = ArrayField(models.CharField(max_length=250, blank=True), blank=True, null=True, default=list)
    progress = models.IntegerField(default=0, blank=True, null=True)
    subdomains = ArrayField(models.CharField(max_length=250, blank=True), blank=True, null=True, default=list)

    class Meta():
        db_table = 'project'
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        ordering = ("project_user", "project_name", "program", "in_scope_domains", "progress", "subdomains")

    def __str__(self):
        return self.project_user.name + 'Project'

    def get_project_details(self):
        return [self.project_name, self.program, self.progress]

class PayloadModel(models.Model):
    payload_user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, unique=True, related_name='payload', on_delete=models.CASCADE)
    payload_image = models.ImageField(default='default.png', upload_to='payloads/', blank=True, null=True)

    class Meta():
        db_table = 'payload'
        verbose_name = _('payload')
        verbose_name_plural = _('payloads')

    def __str__(self):
        return self.payload_user.name + ' Payloads'

class WordlistModel(models.Model):
    wordlist_user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, unique=True, related_name='wordlist', on_delete=models.CASCADE)
    wordlist_file_1 = models.FileField(default='media/rockyou.txt', editable="False")
    wordlist_file_2 = models.FileField(default='media/all.txt', editable="False")
    wordlist_file_3 = models.FileField(default=None, upload_to='wordlists/', blank=True, null=True)
    wordlist_file_4 = models.FileField(default=None, upload_to='wordlists/', blank=True, null=True)
    wordlist_file_5 = models.FileField(default=None, upload_to='wordlists/', blank=True, null=True)

    class Meta():
        db_table = 'wordlist'
        verbose_name = _('wordlist')
        verbose_name_plural = _('wordlists')

    def __str__(self):
        return self.wordlist_user.name + ' Wordlists'

    def return_db_values(self):
        return [self.wordlist_file_3, self.wordlist_file_4, self.wordlist_file_5]

class SubdomainModel(models.Model):
    subdomain_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='subdomain', on_delete=models.CASCADE)
    project = models.ForeignKey(ProjectModel, max_length=30, unique=False, blank=True, null=False, on_delete=models.CASCADE)
    hostname = models.TextField(max_length=200, unique=True)
    status_code = models.TextField(max_length=30, unique=False, null=True, blank=False)
    screenshot = models.FileField(default=None, upload_to='screenshots/', blank=True, null=True)
    ip_address = models.CharField(max_length=30, unique=False, null=True, blank=True)
    waf = models.TextField(max_length=30, unique=False, null=True, blank=False)
    ports = ArrayField(models.CharField(max_length=10, blank=True), blank=True, null=True, default=list)
    ssl_info = JSONField()
    header_info = models.TextField(max_length=500, unique=False, null=True, blank=True)
    directories = ArrayField(models.CharField(max_length=3000, blank=True), blank=True, null=True, default=list)

    class Meta():
        db_table = 'subdomain'
        verbose_name = _('subdomain')
        verbose_name_plural = _('subdomains')

    def __str__(self):
        return self.subdomain_user.name + ' Subdomains'

class CeleryTaskModel(models.Model):
    task_user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, unique=True, related_name='celerytask', on_delete=models.CASCADE)
    subdomain_task = models.TextField(max_length=50, unique=False, null=True, blank=True)

    class Meta():
        db_table = 'celerytask'
        verbose_name = _('celerytask')
        verbose_name_plural = _('celerytask')

    def __str__(self):
        return self.task_user.name + ' Celery Tasks'
