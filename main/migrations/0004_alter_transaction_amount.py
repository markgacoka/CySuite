# Generated by Django 3.2.5 on 2021-07-31 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20210731_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.TextField(blank=True, max_length=10, null=True),
        ),
    ]
