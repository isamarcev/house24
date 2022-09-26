# Generated by Django 4.1 on 2022-09-25 18:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('houses', '0005_alter_house_image_1_alter_house_image_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]