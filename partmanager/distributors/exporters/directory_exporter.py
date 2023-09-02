import json
import time
import os


def create_distributor_file(distributor, filename):
    with open(filename, 'w') as distributor_file:
        json.dump(distributor.to_dict(), distributor_file)


def export(distributors, workdir=None):
    if workdir is None:
        workdir = '/tmp/distributor/export/' + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(workdir)
    os.makedirs(workdir + '/files')
    for distributor in distributors:
        filename = "{}.json".format(distributor.name)
        create_distributor_file(distributor, workdir + '/' + filename)
    return workdir
