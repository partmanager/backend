import time
import os
import shutil
import json


def create_project_file(project, filename):
    with open(filename, 'w') as project_file:
        json.dump(project.to_dict(), project_file)


def copy_project_bom_files(project, destination):
    pass
    #if project.invoice_file:
    #    shutil.copy(project.invoice_file.path, destination)


def export(projects, workdir=None):
    if workdir is None:
        workdir = '/tmp/project_export/' + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(workdir)
    os.makedirs(workdir + '/files')
    for project in projects:
        filename = "{}.json".format(project.name)
        create_project_file(project, workdir + '/' + filename)
        copy_project_bom_files(project, workdir + '/files')
    return workdir
