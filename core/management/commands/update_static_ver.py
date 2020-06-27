import os
from django.utils import timezone
from django.core.management.base import BaseCommand
from core.utils.globals import write_css_version


class Command(BaseCommand):
    help = 'update_static_ver'

    def handle(self, *args, **options):
        print('=================================================   START | update_static_ver | ')
        update_static_ver()
        print('=================================================   FINISH| update_static_ver | ')


def update_static_ver():
    new_version = write_css_version()
    print('NICE update static version. NOW version: %s' % new_version)