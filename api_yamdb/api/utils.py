from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from api_yamdb.settings import DEFAULT_FROM_EMAIL


def generate_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    return confirmation_code


def send_conform_mail(user):
    confirmation_code = generate_confirmation_code(user)
    subject = 'Ваш код подтверждения'
    message = f'Ваш код подтверждения {confirmation_code}'
    recipient_list = [user.email]

    send_mail(subject, message, DEFAULT_FROM_EMAIL, recipient_list,
              fail_silently=False)
