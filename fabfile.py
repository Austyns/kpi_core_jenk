#!/usr/bin/env python
# Author Augustine Okorougo,
# All rights reserved
import os
import sys
import time
import shutil
import traceback
from contextlib import contextmanager as context
from django import *
from datetime import datetime

from fabric.api import local, run, cd, sudo, prefix, execute, task, hosts, env
from fabric.operations import put

# env.use_ssh_config = True
env.hosts = ["68.183.103.72"]
env.user = "root"
# env.key_filename = "path/to/key/file"
env.password = ""
env.port = 22

sys.path.append(".")

version = 0.5

dist = "dist"
env = 'env'
root = "~/kpi"
home = os.path.join(root, "kpi-app")
project = 'kpi-app-%s' % version
base = os.path.join(home, project)
# static = "~/static/"

@context
def use(env):
    '''Activates a particular the virtual environment in @env'''
    with cd(base):
        expression = "source %s/bin/activate" % env
        with prefix(expression):
            yield

def mkvirtualenv(env):
    '''Creates a new virtual environment'''
    run("virtualenv --python=python3 %s" % env)

def package():
    '''Transfer most version of the application to the server'''
    header("packaging and transferring love to the server")
    print("Transfering the current version of the application to the server")
    archive = "kpi_core-{0}.tar.gz".format(version)
    local("git archive -o {0} HEAD".format(archive))
    put("./{0}".format(archive), base, use_sudo=True)
    # sudo("test -d {0} || mkdir -p {0}".format(static))
    with cd(base):
        run("tar -xvf {0}".format(archive))
        run("rm {0}".format(archive))
    local("rm {0}".format(archive))
    print("Finished transfering the application,")
    print "updating nginx configuration on the server"
    sudo("test -d {0} || mkdir -p {0}".format("~/nginx/conf/backup"))
    if run("test -f {0}".format("/etc/nginx/sites-enabled/default"), warn_only=True).succeeded:
        print("Moving the default nginx configuration to the backup directory")
        sudo("mv {0} ~/nginx/conf/backup/".format("/etc/nginx/sites-enabled/default"))
    print "updating nginx configuration on the server"
    put("./settings/sites.conf", "/etc/nginx/conf.d/", use_sudo=True)

    print "Setting up Cors Midware for Django Rest Framework"
    # put("./.env/lib/python2.7/site-packages/corsheaders/middleware.py", base+"/env/lib/python2.7/site-packages/corsheaders/middleware.py", use_sudo=True)

    print "Whitenose to serve Djangos static file in gunicorn"
    put("./settings/wsgi.py", base+"/kpi_core/wsgi.py", use_sudo=True)
 
@task   
def setup():
    '''Install dependencies for the project on the server'''
    sudo("apt-get update")
    sudo("apt-get -y install git")
    sudo("apt-get -y install python-pip")
    sudo("apt-get -y install fabric")
    sudo("pip install virtualenv")
    sudo("apt-get -y install nginx")
    sudo("apt-get install postgresql")
    sudo("apt-get install postgresql-contrib")
    sudo('-u postgres psql -c "ALTER USER postgres PASSWORD 'pass1234'; " ')
    with cd(base):
        mkvirtualenv(env)
    with use(env):
        sudo("pip install gunicorn")
        sudo("pip install whitenoise")

@task
def start():
    '''serve kpi_core API using gunicorn in the cloud.'''
    with use(env):
        # sudo("ls")
        sudo("pip install -r requirements.txt")
        run("gunicorn --bind 0.0.0.0:8000 kpi_core.wsgi:application ", pty=False)
    sudo("service nginx restart")

@task
def restart():
    '''serve kpi_core API using gunicorn in the cloud.'''
    with use(env):
        # sudo("ls")
        sudo("pip install -r requirements.txt")
        execute(stop)
        run("gunicorn --bind 0.0.0.0:8000 kpi_core.wsgi:application ", pty=False)
    sudo("service nginx restart")


@task
def stop():
    '''stop service'''
    with cd(base):
        run("pkill gunicorn")
    sudo("service nginx stop")
    
@task
def undeploy():
    '''Clean old install'''
    print "Cleaning out old install of kpi"
    execute(stop)
    sudo("rm -rf %s" % root)
    sudo("rm /etc/nginx/conf.d/sites.conf")
    print "Finished cleaning out the old installation"

@task
def deploy():
    '''Setup, and run the kpi_core API'''
    print "Creating required application directories"
    for name in (base,):
        run("test -d {0} || mkdir -p {0}".format(name))
    execute(setup)
    execute(package)
    execute(start)
    
@task
def update():
    '''Update, and run the mark API'''
    print "Creating required application directories"
    for name in (base,):
        run("test -d {0} || mkdir -p {0}".format(name))
    execute(package)
    execute(restart)
    

def header(message, char= "*"):
    '''formats messages within this script in a particular way'''
    width = 70
    padding = (width - len(message))/2
    print(char * padding + message + char * padding)

@task
def clean():
    '''Remove all build related stuff,'''
    header("clean")
    dir = os.getcwd()
    print("Working directory: %s" % dir)
    print("Removing all .pyc and temporary files")
    for root, dirs, files in os.walk(dir):
        for f in files:
            deletable = [".pyc", ".tar.gz", "~", ".sqlite", ".db"]
            for extension in deletable:
                if f.endswith(extension):
                    path = os.path.join(root,f)
                    print("Removing: %s" % path)
                    os.unlink(path)
        for d in dirs:
            if d.endswith('.egg-info'):
                path = os.path.join(root, d)
                print("Removing Directory: %s" % path)
                shutil.rmtree(path)
    header('')
 
 



