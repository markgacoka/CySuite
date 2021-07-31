# Generated by Django 3.2.5 on 2021-07-31 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20210731_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='user',
        ),
        migrations.AddField(
            model_name='transaction',
            name='user_account',
            field=models.TextField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='transaction_code',
            field=models.TextField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
