import jwt
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def generate_confirmation_code(user):
    payload = {
        'username': user.username,
        'email': user.email,
        'exp': timezone.now() + timedelta(hours=1)
    }
    confirmation_code = jwt.encode(
        payload, settings.SECRET_KEY, algorithm='HS256')
    return confirmation_code


def send_conform_mail(user):
    confirmation_code = generate_confirmation_code(user)
    subject = 'Ваш код подтверждения'
    message = f'Ваш код подтверждения {confirmation_code}'
    from_email = 'yamdb@example.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list,
              fail_silently=False)
