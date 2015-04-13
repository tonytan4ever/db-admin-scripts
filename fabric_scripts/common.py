'''
Created on Mar 31, 2015

@author: tony7514
'''
import os
from fabric.operations import run, put


def put_and_untar(file_path, remote_path='/root'):
    # make sure the root irectory is there!
    run('mkdir -p /root')

    # Put local nova-cloud88.tar to the root directory
    # of the server
    if not os.path.exists(file_path):
        raise ValueError("File %s does not exist" % file_path)
    
    put(file_path, remote_path)
    run('tar xvf %s' % file_path)
