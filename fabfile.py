import os
from fabric.api import local, run, env, execute, sudo, cd, settings, task, roles
from core.utils.globals import write_css_version
from hohl import local_settings

servers = {
    'production': [local_settings.PROJECT_PRODACTION_IP],
}
env.roledefs.update(servers)

project_dir = '/home/myuser/hohl/www'
venv_dir = '/home/myuser/hohl/venv'

@roles('production')
def deploy(git_push=0):
    if git_push:
        local('git push origin master')
        print('============================================== NICE GIT push')

    with settings(user=local_settings.PROD_USER):
        with cd(project_dir):
            run('git pull origin master')
            print('============================================== NICE GIT pull')
            run('%s/bin/pip install -r requirements.txt' % (venv_dir))
            print('============================================== NICE pip install')
            run('%s/bin/python manage.py migrate' % (venv_dir))
            print('============================================== NICE migrate')
            run('%s/bin/python manage.py collectstatic --noinput' % (venv_dir))
            print('============================================== NICE collectstatic')
            run('%s/bin/python manage.py update_static_ver' % (venv_dir))
            print('============================================== NICE update_static_ver')
    print(('='*100 + '\n')*4)
    print('FINISH')

def update_static_ver():
    new_version = write_css_version()
    print('NICE update static version. NOW version: %s' % new_version)
