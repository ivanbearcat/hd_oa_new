# Generated by Django 3.2.7 on 2021-10-20 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='finish_time',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='完成时间'),
        ),
    ]