# Generated by Django 4.1 on 2022-09-25 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='father_name',
            field=models.CharField(blank=True, default='', help_text='Отчество', max_length=30, null=True),
        ),
    ]
