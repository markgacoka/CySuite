import cyauth.models
import django.contrib.postgres.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('user_id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=30, null=True)),
                ('last_name', models.CharField(max_length=30, null=True)),
                ('username', models.CharField(max_length=64, unique=True)),
                ('occupation', models.CharField(blank=True, default='Researcher', max_length=64, null=True)),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('image', models.TextField(default='default.jpeg', max_length=250)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_premium', models.BooleanField(default=False)),
                ('hide_email', models.BooleanField(default=True)),
                ('feedback', models.CharField(blank=True, default='', max_length=1200, null=True)),
                ('api_token', models.CharField(blank=True, max_length=64, null=True)),
                ('payload_image', models.ImageField(blank=True, default='https://cysuite-bucket.s3.us-west-2.amazonaws.com/media/default.png', null=True, upload_to='payloads/')),
                ('badges', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=3000), blank=True, default=cyauth.models.generate_badges, null=True, size=None)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'db_table': 'people',
                'abstract': False,
            },
            managers=[
                ('objects', cyauth.models.MyUserManager()),
            ],
        ),
    ]
