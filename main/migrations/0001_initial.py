# Generated by Django 3.2.6 on 2021-08-22 18:30

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cyauth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscriber', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'periodical',
                'verbose_name_plural': 'periodicals',
                'db_table': 'periodical',
            },
        ),
        migrations.CreateModel(
            name='PayloadModel',
            fields=[
                ('payload_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='payload', serialize=False, to='cyauth.account')),
                ('payload_image', models.ImageField(blank=True, default='default.png', null=True, upload_to='payloads/')),
            ],
            options={
                'verbose_name': 'payload',
                'verbose_name_plural': 'payloads',
                'db_table': 'payload',
            },
        ),
        migrations.CreateModel(
            name='ProjectModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(blank=True, max_length=30, unique=True)),
                ('program', models.TextField(max_length=30)),
                ('in_scope_domains', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250), blank=True, default=list, null=True, size=None)),
                ('progress', models.IntegerField(blank=True, default=0, null=True)),
                ('subdomains', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=250), blank=True, default=list, null=True, size=None)),
                ('project_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
                'db_table': 'project',
                'ordering': ('project_user', 'project_name', 'program', 'in_scope_domains', 'progress', 'subdomains'),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_account', models.TextField(default='None', max_length=30)),
                ('given_name', models.TextField(blank=True, max_length=50, null=True)),
                ('last_name', models.TextField(blank=True, max_length=50, null=True)),
                ('payer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('currency', models.TextField(blank=True, max_length=10, null=True)),
                ('status', models.TextField(blank=True, max_length=254, null=True)),
                ('transaction_code', models.TextField(blank=True, max_length=50, null=True, unique=True)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'payments',
            },
        ),
        migrations.CreateModel(
            name='WordlistModel',
            fields=[
                ('wordlist_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='wordlist', serialize=False, to='cyauth.account')),
                ('wordlist_file_1', models.FileField(default='media/rockyou.txt', editable='False', upload_to='')),
                ('wordlist_file_2', models.FileField(default='media/all.txt', editable='False', upload_to='')),
                ('wordlist_file_3', models.FileField(blank=True, default=None, null=True, upload_to='wordlists/')),
                ('wordlist_file_4', models.FileField(blank=True, default=None, null=True, upload_to='wordlists/')),
                ('wordlist_file_5', models.FileField(blank=True, default=None, null=True, upload_to='wordlists/')),
            ],
            options={
                'verbose_name': 'wordlist',
                'verbose_name_plural': 'wordlists',
                'db_table': 'wordlist',
            },
        ),
        migrations.CreateModel(
            name='SubdomainModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostname', models.TextField(max_length=200, unique=True)),
                ('status_code', models.TextField(max_length=30, null=True)),
                ('screenshot', models.FileField(blank=True, default=None, null=True, upload_to='screenshots/')),
                ('ip_address', models.CharField(blank=True, max_length=30, null=True)),
                ('waf', models.TextField(max_length=30, null=True)),
                ('ssl_info', jsonfield.fields.JSONField()),
                ('header_info', jsonfield.fields.JSONField()),
                ('directories', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=3000), blank=True, default=list, null=True, size=None)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subdomain', to='main.projectmodel')),
            ],
            options={
                'verbose_name': 'subdomain',
                'verbose_name_plural': 'subdomains',
                'db_table': 'subdomains',
            },
        ),
    ]
