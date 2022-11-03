# Generated by Django 4.1 on 2022-10-05 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounting', '0008_remove_personalaccount_owner_and_more'),
        ('houses', '0013_alter_flat_floor_alter_flat_owner_alter_flat_section_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='personal_account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='account_flat', to='crm_accounting.personalaccount'),
        ),
    ]
