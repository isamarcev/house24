# Generated by Django 4.1 on 2022-10-16 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_accounting', '0013_alter_invoice_date_alter_invoice_period_end_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceservice',
            name='unit',
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_state',
            field=models.BooleanField(blank=True, null=True, verbose_name='Проведена'),
        ),
    ]
