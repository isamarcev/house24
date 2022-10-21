# Generated by Django 4.1 on 2022-10-18 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_home', '0017_alter_paymentstate_type'),
        ('crm_accounting', '0016_alter_invoice_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceservice',
            name='invoice',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='crm_accounting.invoice'),
        ),
        migrations.AlterField(
            model_name='invoiceservice',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='crm_home.service'),
        ),
    ]
