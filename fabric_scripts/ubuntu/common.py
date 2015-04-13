'''
Created on April 15th, 2015

@author: tony7514
'''
from fabric.operations import sudo

def apt_get_install(packages):
    packages_string = ' '.join(packages)
    sudo('apt-get -y --no-upgrade install %s' % packages_string)