# Generated by Django 3.2.6 on 2021-08-14 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210814_1248'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payloadmodel',
            old_name='image',
            new_name='payload_image',
        ),
    ]