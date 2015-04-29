from fabric.api import env
from fabric.operations import sudo
from fabric.context_managers import cd
import helper
import common

env.hosts = ['root@104.130.24.157']


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

    # upload and install glance-cloud88.
    # common.put_and_untar('glance-cloud88.tar', '/root')
    # with cd('/root/glance-cloud88'):
    #    sudo('python setup.py install')

    # sync nova taba
    # sudo("./nova-cloud88/bin/nova-manage db sync")
