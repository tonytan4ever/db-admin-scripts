'''
Cloud-88 Compute Node Deployment Script

@author: Tony Tan
'''
from fabric.api import env, settings, hide, prompt
from fabric.operations import run, put, sudo
from fabric.utils import warn

env.hosts = ['root@166.78.114.252.bast']


packages = [
    "python-dev",
    "python-setuptools"
]


def apt_get(packages):
    packages_string = ' '.join(packages)
    sudo('apt-get -y --no-upgrade install %s' % packages_string)


def install_prerequisite():
    apt_get(packages)
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
