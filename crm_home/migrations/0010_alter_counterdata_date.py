# Generated by Django 4.1 on 2022-10-06 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_home', '0009_alter_tariffservice_tariff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counterdata',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]