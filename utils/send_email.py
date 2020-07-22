from django.core.mail import send_mail
from django.conf import settings


def send_new_password(self, name, email, newpassword):
    subject = 'Recuperação de Senha'
    message = 'Olá ' + name + ', sua nova senha é: ' + newpassword
    context = {
        'message': message
    }
    message = message % context
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email])
