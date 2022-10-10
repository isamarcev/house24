# Generated by Django 4.1 on 2022-10-04 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houses', '0013_alter_flat_floor_alter_flat_owner_alter_flat_section_and_more'),
        ('crm_accounting', '0007_personalaccount_flat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalaccount',
            name='owner',
        ),
        migrations.AlterField(
            model_name='personalaccount',
            name='flat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='houses.flat'),
        ),
    ]