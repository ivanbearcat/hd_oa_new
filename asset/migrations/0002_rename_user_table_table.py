# Generated by Django 3.2.4 on 2021-06-16 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='user_table',
            new_name='table',
        ),
    ]
