import time
import os
import json


def create_json_file(filename, manufacturers):
    manufacturers_array = []
    for manufacturer in manufacturers:
        manufacturers_array.append(manufacturer.to_dict())
    with open(filename, 'w') as manufacturers_file:
        json.dump(manufacturers_array, manufacturers_file)


def export(manufacturers, workdir=None):
    if workdir is None:
        workdir = '/tmp/manufacturers/export/' + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(workdir)
    os.makedirs(workdir + '/files')
    filename = "manufacturers.json"
    create_json_file(workdir + '/' + filename, manufacturers)
    return workdir
