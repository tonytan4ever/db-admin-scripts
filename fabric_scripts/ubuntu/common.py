'''
Created on Mar 31, 2015

@author: tony7514
'''
from fabric.operations import run, put


def copy():
    # make sure the root irectory is there!
    run('mkdir -p /root')

    # Put local nova-cloud88.tar to the root directory
    # of the server
    put('nova-cloud88.tar', '/root')
    run('tar xvf nova-cloud88.tar')
