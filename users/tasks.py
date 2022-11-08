from django.core.mail import send_mail, EmailMultiAlternatives
from django.utils.html import strip_tags

from home24.celery import app
from home24.settings import EMAIL_HOST_USER


@app.task
def send_activation_letter(subject, body_text, email):
    return send_mail(subject, body_text, None, [email], fail_silently=False)


