# Generated by Django 4.1 on 2022-10-13 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_home', '0014_alter_counterdata_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentstate',
            name='type',
            field=models.CharField(choices=[('in', 'Приход'), ('out', 'Расход')], max_length=30),
        ),
    ]
