# Generated by Django 4.1 on 2022-11-09 20:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.IntegerField(blank=True, default=users.models.get_next_user_id, error_messages={'unique': 'Пользователь с таким ID уже существует.'}, help_text='Required', max_length=100, null=True, unique=True, verbose_name='User ID'),
        ),
        migrations.AlterField(
            model_name='request',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_request', to=settings.AUTH_USER_MODEL),
        ),
    ]
