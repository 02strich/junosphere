#!/usr/bin/env python

from io import BytesIO
from pprint import pprint
import os
import os.path
import sys
from zipfile import ZipFile, ZIP_DEFLATED

import requests
from requests.auth import HTTPBasicAuth

USERNAME = 'stefric@amazon.com'
PASSWORD = ''


def list_topologies(sandbox_name):
    """List all topologies in the sandbox with the supplied name"""
    response = requests.get("https://junosphere.net/api/topologyService/topologies", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    assert response.status_code == 200
    for topology in response.json()['topologies']['topology']:
        if topology['sandboxLibrary']['sandbox']['name'] == sandbox_name:
            yield topology


def update_local_fileset(topology_id, fileset_id):
    """Download remote config files to local archive folder"""
    # step 1 delete current content

    # step 2 download updated content
    response = requests.get("https://junosphere.net/api/topologyService/topologies/" + str(topology_id) + '/fileset', auth=HTTPBasicAuth(USERNAME, PASSWORD))
    assert response.status_code == 200
    fileset = ZipFile(BytesIO(response.content))

    # step 3 extract it
    fileset.extractall(path=fileset_id)


def update_remote_fileset(topology_id, fileset_id):
    """Upload a local set of config files to a topology"""
    # step 1: zip up the files
    with ZipFile(fileset_id + '.zip', 'w') as zf:
        def addToZip(zf, path, zippath):
            if os.path.isfile(path):
                zf.write(path, zippath, ZIP_DEFLATED)
            elif os.path.isdir(path):
                if zippath:
                    zf.write(path, zippath)
                for nm in os.listdir(path):
                    addToZip(zf, os.path.join(path, nm), os.path.join(zippath, nm))
        
        addToZip(zf, fileset_id + '/', '')


def get_sandbox_active_vmachines(sandbox_name):
    """List the virtual machines in the active topology of the sandbox with the supplied name"""
    # step 1: find the sandbox ID
    response = requests.get("https://junosphere.net/api/sandboxService/sandboxes", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    assert response.status_code == 200
    sandbox_id = None
    for sandbox in response.json()['sandboxes']['sandbox']:
        if sandbox['name'] == sandbox_name:
            sandbox_id = sandbox['id']
            break
    if sandbox_id is None:
        raise Exception("Did not find sandbox: " + sandbox_name)

    # step 2: get details
    response = requests.get("https://junosphere.net/api/sandboxService/sandboxes/" + str(sandbox_id) + "/active/vmachines", auth=HTTPBasicAuth(USERNAME, PASSWORD))
    assert response.status_code == 200
    return response.json()['vmachines']['vmachine']


def main():
    if sys.argv[1] == 'topologies':
        print("{0:<7} | {1:25} | {2:3}".format("ID", "Name", "VMs"))
        print("-"*(7+25+3+6))
        for topology in list_topologies('stefric-sandbox'):
            print("{0:<7} | {1:25} | {2:3}".format(topology['id'], topology['name'], topology['numberOfVMs']))
    elif sys.argv[1] == 'download':
        update_local_fileset(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'upload':
        update_remote_fileset(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'vmachines':
        print("{0:<15} | {1:25} | {2:7}".format("IP", "Name", "State"))
        print("-"*(15+25+7+6))
        for vmachine in get_sandbox_active_vmachines('stefric-sandbox'):
            print("{0:<15} | {1:25} | {2:7}".format(vmachine['ip'], vmachine['name'], vmachine['state']))
    else:
        print("Did not understand the command, please use one off topologies, download or vmachines")

if __name__ == "__main__":
    main()
