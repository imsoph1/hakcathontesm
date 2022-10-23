from django.core.mail import send_mail


def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
    send_mail(
        'Hello! Activate your account!',
        f'To activate your account you need to link: {full_link}',
        'sagynbekovasofi@gmail.com',
        [user],
        fail_silently=False)



def send_code_email(user, code):
    send_mail(
        'Hello! Recovery your account!',
        f'CODE: {code}',
        'abdb2226@gmail.com',
        [user],
        fail_silently=False)