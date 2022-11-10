from django.template.loader import render_to_string
from django.core.signing import Signer
from django.urls import register_converter

from home24.settings import ALLOWED_HOSTS
from .tasks import send_activation_letter

signer = Signer()


def send_activation_notification(user):
    if ALLOWED_HOSTS:
        host = 'http://' + ALLOWED_HOSTS[0]
    else:
        host = 'http://127.0.0.1:8000'
    context = {'user': user,
               'host': host,
               'sign': signer.sign(user.email)}
    subject = render_to_string('users/elements/email/activation_letter_subject.txt', context)
    body_text = render_to_string('users/elements/email/activation_letter_body.txt', context)
    send_activation_letter.delay(subject, body_text, user.email)

