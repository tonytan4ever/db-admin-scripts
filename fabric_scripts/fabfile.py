from fabric.api import env
from fabric.operations import sudo
import helper

env.hosts = ['root@166.78.112.69']


def cloud_88_nova_compute_node():
    helper.install_prerequisite()
    helper.install_rabbitmq()
    helper.install_mysql(username='nova', password='nova',
                         new_database='nova')
    # python dependencies
    # helper.install_pip()
    # helper.install_python_packages()
    # c
    sudo("mkdir /var/log/nova", user="root")
