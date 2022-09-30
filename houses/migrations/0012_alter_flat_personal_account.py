# Generated by Django 4.1 on 2022-09-30 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounting', '0007_personalaccount_flat'),
        ('houses', '0011_alter_flat_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='personal_account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account_flat', to='crm_accounting.personalaccount'),
        ),
    ]
