# Generated by Django 3.2.6 on 2021-08-22 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmodel',
            name='project_name',
            field=models.CharField(blank=True, max_length=30, primary_key=True, serialize=False),
        ),
    ]
