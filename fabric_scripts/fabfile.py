from fabric.api import env
from fabric.operations import sudo
import helper
import common

env.hosts = ['root@162.209.99.116']


def cloud_88_nova_compute_node():
    helper.install_prerequisite()
    helper.install_rabbitmq()
    helper.install_mysql(username='nova', password='nova',
                         new_database='nova')
    # python dependencies
    helper.install_pip()
    helper.install_python_packages()
    sudo("mkdir /var/log/nova", user="root")

    # upload cloud-88 tar file
    # common.put_and_untar('nova-cloud88.tar', '/root')
