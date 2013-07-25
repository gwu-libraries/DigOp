from fabric.operations import local as lrun
from fabric.api import *
from fabric.colors import green, red

import urllib


release = user = db = repo = repo_name = path = password = inv_key = inv_user = inv_url = host = email = ''

def localhost():
    env.run = lrun
    env.hosts = ['localhost']

def install_apache():
    local('sudo apt-get install apache2 python-dev  python-setuptools libapache2-mod-wsgi')

def install_db():
    local('sudo apt-get install postgresql postgresql-contrib libpq-dev')

def install_db_python():
    local('sudo apt-get build-dep python-psycopg2')

def install_git():
    local('sudo apt-get install git-core')

def install_virtualenv():
    local('sudo apt-get install python-setuptools')
    local('sudo easy_install virtualenv')

def setup():
    global release, user, db, repo, repo_name, path, password, inv_key, inv_user, inv_url, host, email
    release = prompt("what do you want to "
            "name the new release?: ",
            validate="^[a-zA-Z0-9\\-\\._]+$")
    user = db = release
    repo = prompt("enter https url of git repo")
    repo_name = prompt("Enter git repo name")
    path = prompt ("Enter the path to the root folder for installation")
    password = prompt ("Enter DB password")
    inv_key = prompt("Enter inventory API key")
    inv_user = prompt("Enter user name for inventory API")
    inv_url = prompt("Enter inventory url")
    inv_url = inv_url.replace('/', '\/')
    host = prompt("Enter the hostname on which app is getting deployed")
    email = prompt("Enter the email address of the admin for this deployment")


def deploy():
    setup()
    print(green("Installing Apache and other System Packages"))
    install_apache()
    print(green("Installing DB System Packages"))
    install_db()
    print(green("Installing DB dependencies"))
    install_db_python()
    print(green("installing git"))
    install_git()
    print(green("installing virtualenv"))
    install_virtualenv()
    print(green("Setting up Database"))
    #local('export PGPASSWORD=%s' %password)
    local('sudo -u postgres createuser --createdb --no-superuser  --no-createrole --pwprompt %s' %user)
    local('sudo -u postgres createdb -O %s %s' %(user,  db))
    local('cd %s' %path)
    local('mkdir %s' %release)
    with lcd('%s' %release):
        print(green("Pulling master from GitHub..."))
        local("pwd")
        local("git clone %s" %repo)
    with lcd ('%s/%s' %(release, repo_name)):
        local("pwd")
        print(green("Creating virtual ENV"))
        local('virtualenv --no-site-packages ENV')
        with prefix('/bin/bash ENV/bin/activate'):
            print(green("Installing requirement..."))
            local('ENV/bin/pip install -r requirements.txt')
            #edit the local_settings.py file
            local('cp %s/local_settings.py.template %s/local_settings.py' %(repo_name, repo_name))
            local("sed \"s/backends.mysql/backends.postgresql_psycopg2/g\" %s/local_settings.py> %s/local_settings.py.tmp" %(repo_name,repo_name))
            local("mv %s/local_settings.py.tmp %s/local_settings.py" %(repo_name, repo_name))
            local("sed \"s/'NAME': ''/'NAME': '%s'/g\" %s/local_settings.py> %s/local_settings.py.tmp" % (db, repo_name, repo_name))
            local("mv %s/local_settings.py.tmp %s/local_settings.py" %(repo_name, repo_name))
            local("sed \"s/'USER': ''/'USER': '%s'/g\" %s/local_settings.py> %s/local_settings.py.tmp" % (user, repo_name, repo_name))
            local("mv %s/local_settings.py.tmp %s/local_settings.py" %(repo_name, repo_name))
            local("sed \"s/'PASSWORD': ''/'PASSWORD': '%s'/g\" %s/local_settings.py> %s/local_settings.py.tmp" % (password, repo_name, repo_name))
            local("mv %s/local_settings.py.tmp %s/local_settings.py" %(repo_name, repo_name))
            local("sed \"s/INV_API_KEY = ''/INV_API_KEY = '%s'/g\" %s/local_settings.py> %s/local_settings.py.tmp" % (inv_key, repo_name, repo_name))
            local("mv %s/local_settings.py.tmp %s/local_settings.py" %(repo_name, repo_name))
            local("sed \"s/INV_USER = ''/INV_USER = '%s'/g\" %s/local_settings.py> %s/local_settings.py.tmp" % (inv_user, repo_name, repo_name))
            local("mv %s/local_settings.py.tmp %s/local_settings.py" %(repo_name, repo_name))
            local("sed \"s/INV_URL = ''/INV_URL = '%s\/api\/v1\/'/g\" %s/local_settings.py> %s/local_settings.py.tmp" % (inv_url, repo_name, repo_name))
            local("mv %s/local_settings.py.tmp %s/local_settings.py" %(repo_name, repo_name))
            local("sed \"s/'HOST': ''/'HOST': 'localhost'/g\" %s/local_settings.py> %s/local_settings.py.tmp" % (repo_name, repo_name))
            local("mv %s/local_settings.py.tmp %s/local_settings.py" %(repo_name, repo_name))
            #edit the wsgi file
            local("cp %s/wsgi.py.template %s/wsgi.py" %(repo_name, repo_name))
            local("sudo sed \"s/#import site/import site/g\" %s/wsgi.py> %s/wsgi.py.tmp" % (repo_name, repo_name))
            local("mv %s/wsgi.py.tmp %s/wsgi.py" %(repo_name, repo_name))
            local("sudo sed \"s/#ENV = '\/PATH\/TO\/YOUR\/VIRTUALENV'/ENV = '%s%s\/%s\/ENV'/g\" %s/wsgi.py> %s/wsgi.py.tmp" % (path.replace('/', '\/'), release, repo_name, repo_name, repo_name))
            local("mv %s/wsgi.py.tmp %s/wsgi.py" %(repo_name, repo_name))
            local("sudo sed \"s/#site.addsitedir(ENV + '\/lib\/python2.7\/site-packages')/site.addsitedir(ENV + '\/lib\/python2.7\/site-packages')/g\" %s/wsgi.py> %s/wsgi.py.tmp" % (repo_name, repo_name))
            local("mv %s/wsgi.py.tmp %s/wsgi.py" %(repo_name, repo_name))
            #create database schema
            local("ENV/bin/python manage.py syncdb")
            local("ENV/bin/python manage.py migrate")
            local("ENV/bin/python manage.py createsuperuser")
            #Edit the apache conf file
            local("sudo sed \"s/<your\.server\.name>/%s/g\" apache/DigOp> apache/DigOps" % host)
            local("mv apache/DigOps apache/DigOp")
            local("sudo sed \"s/you@example\.com/%s/g\" apache/DigOp> apache/DigOps" % email)
            local("mv apache/DigOps apache/DigOp")
            local("sudo sed \"s/\/DIGOPS-HOME\//%s%s\//g\" apache/DigOp> apache/DigOps" % (path.replace('/', '\/'), release))
            local("mv apache/DigOps apache/DigOp")
            local("sudo sed \"s/python2\.X/python2\.7/g\" apache/DigOp> apache/DigOps")
            local("mv apache/DigOps apache/DigOp")
            local("sudo cp apache/DigOp /etc/apache2/sites-available/DigOp")
            local("sudo a2ensite DigOp")
            local("sudo a2dissite default")
            local("sudo /etc/init.d/apache2 restart")






