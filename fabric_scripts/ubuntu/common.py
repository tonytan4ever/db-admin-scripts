'''
Created on April 15th, 2015

@author: tony7514
'''
from fabric.operations import sudo


def apt_get_install(packages):
    sudo('add-apt-repository "deb http://archive.ubuntu.com/ubuntu $(lsb_release -sc) main universe restricted multiverse"')
    sudo('apt-get update')
    packages_string = ' '.join(packages)
    sudo('apt-get -y --no-upgrade install %s' % packages_string)