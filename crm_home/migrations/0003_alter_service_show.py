# Generated by Django 4.1 on 2022-09-18 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_home', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='show',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]