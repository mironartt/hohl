import smtplib
from email.mime.text import MIMEText
from email.header import Header

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


def send_confirm_code(letter_type, user, link, language_key):
    if language_key not in settings.PROJECT_LANGUAGES:
        raise ('Language key is not availabled')

    subjects_keyworks = {
        'email_confirm': {
            'ru': 'Подтверждение регистрации',
            'en': 'Registration confirmation',
        },
        'remind_password': {
            'ru': 'Восстановление пароля',
            'en': 'Password recovery',
        },
    }
    text_keyworks = {
        'email_confirm': {
            'ru': '''ДОБРО ПОЖАЛОВАТЬ
В МИР MAGIRANI!
ДЛЯ ЗАВЕРШЕНИЯ РЕГИСТРАЦИИ ПРОЙДИТЕ ПО ССЫЛКЕ:
{0}'''.format(link),
            'en': '''WELCOME
TO THE WORLD OF MAGIRANI!
TO COMPLETE THE REGISTRATION CLICK ON THE LINK:
{0}'''.format(link),
        },
        'remind_password': {
            'ru': '''Здравствуйте.
На сайте {0} поступил запрос на восстановление пароля и был указан данный email адрес.
Для восставновления пароля, пройдите по данной ссылке:
{1}

Данная ссылка действительна 24 часа.

Если вы не совершали данный запрос, проигнорируйте данное письмо.
С любовью, команда Magirani'''.format(settings.SITE_DOMAIN, link),
            'en': '''Hello.
The site {0} received a request to restore your password and specified this email address.
To restore your password, follow this link:
{1}

This link is valid for 24 hours.

If you didn't make this request, ignore this email.
With love, Magirani team'''.format(settings.SITE_DOMAIN, link),
        },
    }
    print('.\n\nsubject: {0}\ntext: {1}\nuser.email : {2}'.format(subjects_keyworks[letter_type][language_key], text_keyworks[letter_type][language_key], user.email))
    # send_mail(subjects_keyworks[letter_type][language_key], text_keyworks[letter_type][language_key], settings.EMAIL_HOST_USER, [user.email])



    smtp_host = settings.EMAIL_HOST
    login = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    recipients_emails = user.email

    msg = MIMEText(text_keyworks[letter_type][language_key], 'plain', 'utf-8')
    msg['Subject'] = Header(subjects_keyworks[letter_type][language_key], 'utf-8')
    msg['From'] = login
    msg['To'] = recipients_emails

    s = smtplib.SMTP(smtp_host, 587, timeout=10)
    s.set_debuglevel(1)
    try:
        s.starttls()
        s.login(login, password)
        s.sendmail(msg['From'], recipients_emails, msg.as_string())
        print('@#######################@@@@@@@@@@@@@@@@ NICE SEND !@!!!!!!!!!!!!!!!!!!!')
    finally:
        print(msg)
        s.quit()

    return True
