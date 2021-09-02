# Generated by Django 3.2.4 on 2021-06-16 09:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0002_rename_user_table_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='最后更新时间'),
            preserve_default=False,
        ),
    ]
