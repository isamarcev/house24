# Generated by Django 4.1 on 2022-09-25 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0003_remove_house_floor_remove_house_section_floor_house_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='address',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='house',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
