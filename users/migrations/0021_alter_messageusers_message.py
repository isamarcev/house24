# Generated by Django 4.1 on 2022-10-22 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_alter_message_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messageusers',
            name='message',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.message'),
        ),
    ]
