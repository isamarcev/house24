# Generated by Django 4.1 on 2022-09-10 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.role'),
        ),
    ]
