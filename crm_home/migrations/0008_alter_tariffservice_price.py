# Generated by Django 4.1 on 2022-09-19 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_home', '0007_alter_tariffservice_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariffservice',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
    ]