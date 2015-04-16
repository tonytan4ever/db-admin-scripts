'''
@author: Tony Tan
'''
from fabric.api import env, settings, hide, prompt
from fabric.operations import run, put, sudo
from fabric.utils import warn

from ubuntu import common

env.hosts = ['root@166.78.114.252']


packages = [
    "python2.7-dev",
    "python-setuptools"
]


def install_prerequisite():
    common.apt_get_install(packages)
    # create nova log path
    sudo('mkdir /var/log/nova')
    # install rabbitmq and mysqlserver
    sudo('cd /etc/apt; echo "deb http://www.rabbitmq.com/debian/ testing main" >> sources.list;')
    sudo('cd /home; wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc;')
    sudo('cd /home; apt-key add rabbitmq-signing-key-public.asc;')

    sudo('apt-get install -y rabbitmq-server')

    install_mysql()


def install_mysql():
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show mysql-server')
    if result.failed is False:
        warn('MySQL is already installed')
        return
    mysql_password = prompt('Please enter MySQL root password:')
    sudo('echo "mysql-server-5.0 mysql-server/root_password password ' \
                              '%s" | debconf-set-selections' % mysql_password)
    sudo('echo "mysql-server-5.0 mysql-server/root_password_again password ' \
                              '%s" | debconf-set-selections' % mysql_password)
    apt_get('mysql-server')
