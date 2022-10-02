# Generated by Django 4.1 on 2022-09-30 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0008_alter_flat_personal_account'),
        ('crm_accounting', '0006_alter_personalaccount_account_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalaccount',
            name='flat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.flat'),
        ),
    ]