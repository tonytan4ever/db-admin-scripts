from fabric.api import env
import helper

env.hosts = ['root@166.78.111.209']


def cloud_88_nova_compute_node():
    helper.install_prerequisite()
    helper.install_rabbitmq()
    helper.install_mysql()
    # python dependencies
    # helper.install_pip()
    # helper.install_python_packages()
