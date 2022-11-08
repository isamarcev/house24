from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.utils.html import strip_tags
from openpyxl.writer.excel import save_virtual_workbook

from home24.celery import app
from home24.settings import EMAIL_HOST_USER


@shared_task
def send_invoice(invoice_number, email_address, filepath):
    email = EmailMessage(
        'CRM 24 Administarions',
        f'Квитанция',
        None,
        [email_address]
    )
    email.attach(f'Квитанция № {invoice_number}.xlsx', save_virtual_workbook(filepath),
                 'application/vnd.ms-excel')
    return email.send()
