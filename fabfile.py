import os.path
from fabric.api import run, local, put, cd, sudo, env
from fabric.contrib.console import confirm

env.hosts = ['pfbp@prixfernandbaudinprijs.be']
env.path = '/home/pfbp/webapps/pfbp_registration/www.prixfernandbaudinprijs.be/'

def deploy():
    with cd(env.path):
        run('git pull origin master')
        run('python2.7 manage.py collectstatic --noinput')
        run('/home/pfbp/webapps/pfbp_registration/apache2/bin/restart')

def getdb():
    local('/usr/bin/scp pfbp@prixfernandbaudinprijs.be:webapps/pfbp_registration/www.prixfernandbaudinprijs.be/fernand/fernand.db fernand/fernand.db')

def backupdb():
    local('/bin/mkdir -p ~/fernand_db_backup/')
    local('/usr/bin/scp pfbp@prixfernandbaudinprijs.be:webapps/pfbp_registration/www.prixfernandbaudinprijs.be/fernand/fernand.db ~/fernand_db_backup/fernand.$(/bin/date -u +"%Y-%m-%dT%H:%M:%SZ").db')

