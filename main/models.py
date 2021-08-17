from django.db import models
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
    subscriber = models.EmailField(max_length=254, blank=True, null=True)

class ProjectModel(models.Model):
    project_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="projects", default=1, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=30, unique=True, null=False, blank=True)
    program = models.TextField(max_length=30, unique=False, null=False, blank=False)
    in_scope_domains = ArrayField(models.CharField(max_length=250, blank=True), default=list)
    progress = models.IntegerField(default=100)
    subdomains = ArrayField(models.CharField(max_length=250, blank=True), default=list)

    class Meta():
        db_table = 'project'
        verbose_name = _('project')
        verbose_name_plural = _('projects')
        ordering = ("project_user", "project_name", "program", "in_scope_domains", "progress", "subdomains")

    def __str__(self):
        return self.project_user.name + 'Project'

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