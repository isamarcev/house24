# Generated by Django 4.1 on 2022-11-04 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounting', '0020_alter_invoice_personal_account'),
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='media/templates_invoice/')),
                ('name', models.CharField(default='New template', max_length=20)),
                ('default', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
    ]
