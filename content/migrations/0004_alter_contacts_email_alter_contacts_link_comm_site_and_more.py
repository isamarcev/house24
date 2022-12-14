# Generated by Django 4.1 on 2022-09-17 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_remove_servicepage_service_aboutservice_service_page'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='link_comm_site',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='map',
            field=models.URLField(blank=True, null=True),
        ),
    ]
