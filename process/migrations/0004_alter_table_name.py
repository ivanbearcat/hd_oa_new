# Generated by Django 3.2.7 on 2021-12-10 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0003_alter_table_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='name',
            field=models.CharField(max_length=16, verbose_name='申请人'),
        ),
    ]
