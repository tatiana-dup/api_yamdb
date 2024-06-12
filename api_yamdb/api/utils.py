from django.core.mail import send_mail


# Пока только функция отправки письма, генерация кода будет добавлена позже
def send_conform_mail(user):
    subject = 'Ваш код подтверждения'
    message = 'Ваш код подтверждения'
    from_email = 'yamdb@example.com'
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
