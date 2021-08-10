# Generated by Django 3.2.6 on 2021-08-10 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_alter_projectmodel_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='project_user',
            field=models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
