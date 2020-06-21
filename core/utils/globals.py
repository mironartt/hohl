import os
import time
from django.conf import settings
from hohl import local_settings

def get_css_version():
    temp_vers = str(time.time())[:-8]
    if not os.path.exists('%s/%s/css_version.txt' % (os.path.abspath(os.curdir), local_settings.PROJECT_NAME)):
        return temp_vers
    now_vers = open('%s/%s/css_version.txt' % (os.path.abspath(os.curdir), local_settings.PROJECT_NAME), 'r').read()
    return now_vers if now_vers else temp_vers

def write_css_version():
    with open('%s/%s/css_version.txt' % (os.path.abspath(os.curdir), local_settings.PROJECT_NAME), 'w') as f:
        new_version = str(time.time())[:-8]
        f.write(new_version)
        return new_version
