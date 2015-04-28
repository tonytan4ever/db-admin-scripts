'''
Created on Mar 31, 2015

@author: tony7514
'''
import os
from fabric.context_managers import cd
from fabric.operations import run, put, sudo


def put_file(file_path, remote_path='/root'):
    put(file_path, remote_path)


def put_and_untar(file_path, remote_path='/root'):
    # make sure the root irectory is there!
    sudo('mkdir -p %s' % remote_path)

    # Put local nova-cloud88.tar to the root directory
    # of the server
    if not os.path.exists(file_path):
        raise ValueError("File %s does not exist" % file_path)

    put_file(file_path, remote_path)
    with cd(remote_path):
        sudo('tar xvf %s' % os.path.basename(file_path))
