# Generated by Django 4.1 on 2022-09-28 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounting', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalaccount',
            name='flat',
        ),
    ]
