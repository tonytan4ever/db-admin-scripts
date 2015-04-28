'''
@author: Tony Tan
'''
from fabric.api import env, settings, hide, prompt, puts
from fabric.context_managers import cd
from fabric.operations import run, put, sudo
from fabric.utils import warn
from pipes import quote

from ubuntu import common
import common as c_common


packages = [
    "python2.7-dev",       #for ubuntu 12.04 this should be python-dev
    "python-setuptools",
    "build-essential"
]


def install_prerequisite():
    common.apt_get_install(packages)


def install_rabbitmq():
    # install rabbitmq and mysqlserver
    sudo('cd /etc/apt; echo "deb http://www.rabbitmq.com/debian/ testing main" >> sources.list;')
    sudo('cd /home; wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc;')
    sudo('cd /home; apt-key add rabbitmq-signing-key-public.asc;')

    sudo('apt-get install -y rabbitmq-server')


def mysql_query(query, **kwargs):
    """
    Run a MySQL query.
    Adopted from:
        https://github.com/ronnix/fabtools/blob/master/fabtools/mysql.py
    """

    user = kwargs.get('mysql_user') or env.get('mysql_user')
    password = kwargs.get('mysql_password') or env.get('mysql_password')

    options = [
        '--batch',
        '--raw',
        '--skip-column-names',
    ]
    if user:
        options.append('--user=%s' % quote(user))
    if password:
        options.append('--password=%s' % quote(password))
    options = ' '.join(options)

    print options

    return sudo('mysql %(options)s --execute=%(query)s' % {
        'options': options,
        'query': quote(query),
    })


def install_mysql(username=None, password=None, new_database=None, root_password=None):
    """Install mysql server, create a user with username, password, and a new 
        database.
    """
    with settings(hide('warnings', 'stderr'), warn_only=True):
        result = sudo('dpkg-query --show mysql-server')
    if result.failed is False:
        warn('MySQL is already installed')
        return

    mysql_password = root_password or 'root'
    sudo('echo "mysql-server-5.0 mysql-server/root_password password ' \
                              '%s" | debconf-set-selections' % mysql_password)
    sudo('echo "mysql-server-5.0 mysql-server/root_password_again password ' \
                              '%s" | debconf-set-selections' % mysql_password)

    sudo('apt-get install -y mysql-server')

    kwargs = {
        'mysql_user': 'root',
        'mysql_pasword': mysql_password
    }

    print kwargs

    with settings(hide('running')):
        if username:
            mysql_query("CREATE USER '%(name)s'@'%(host)s' IDENTIFIED BY '%(password)s';" % {
                'name': username,
                'password': password,
                'host': 'localhost'
            }, **kwargs)

        if new_database:
            mysql_query("CREATE DATABASE %(name)s CHARACTER SET %(charset)s COLLATE %(collate)s;" % {
                'name': new_database,
                'charset': 'utf8',
                'collate': 'utf8_general_ci'
            }, **kwargs)

        if username:
            mysql_query("GRANT ALL PRIVILEGES ON %(name)s.* TO '%(owner)s'@'%(owner_host)s' WITH GRANT OPTION;" % {
                'name': new_database,
                'owner': username,
                'owner_host': 'localhost'
            }, **kwargs)


def install_pip():
    sudo('easy_install pip==1.5.4')


def install_python_packages(requirement_file_name='requirements.txt'):
    c_common.put_file(requirement_file_name)
    with cd('/root'):
        run('pip install -r requirements.txt')
