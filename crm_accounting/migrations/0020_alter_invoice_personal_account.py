# Generated by Django 4.1 on 2022-10-26 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounting', '0019_alter_invoiceservice_invoice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='personal_account',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]