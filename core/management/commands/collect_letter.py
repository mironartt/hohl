import os
from django.utils import timezone
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'The Zen of Python'

    def handle(self, *args, **options):
        print('=================================================   START | send_mail | ')
        send_mail()
        print('=================================================   FINISH| send_mail | ')


def send_mail():

    file_log = os.path.abspath(os.curdir) + '/logs/commands/send_mail.txt'
    if not os.path.isdir(os.path.abspath(os.curdir) + '/logs/commands'):
        os.mkdir(os.path.abspath(os.curdir) + '/logs/commands')

    file = open(file_log, 'a')
    file.writelines('******************************\nstart - {0}\n'.format(timezone.localtime()))

    # letters = TaskSendidng.objects.filter(is_complite=False).order_by('-priority')
    letters = []
    for letter in letters:
        pass

    file.writelines('    created new MailsSendings id: {}\n'.format('NONE'))
    file.writelines('finish - {0}\n******************************'.format(timezone.localtime()))
    file.close()