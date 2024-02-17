import logging
import os
import json
from projects.models import Project, ProjectVersion, BOM, BOMItem
from partcatalog.models.part import Part
from partcatalog.models.manufacturer_order_number import ManufacturerOrderNumber


logger = logging.getLogger('projects')


def create_project(project_dict):
    logger.info(f"Creating project: {project_dict['name']}")
    project, created = Project.objects.get_or_create(name=project_dict['name'])
    if created:
        logger.debug("\t project already exists")
    version = project_dict['version'] if 'version' in project_dict else project_dict['varsion']
    logger.info(f"Creating project version: {version}")
    project_version, created = ProjectVersion.objects.get_or_create(name=version,
                                                                    project=project)
    #project_version.save()
    return project_version


def create_bom(bom_dict, project):
    bom = BOM(name=bom_dict['name'],
              note=bom_dict['note'],
              description=bom_dict['description'],
              project=project,
              multiply=bom_dict['multiply'],
              #bom_file,
              )
    bom.save()
    for item_dict in bom_dict['items']:
        mon = None
        part = None
        fallback = None
        if item_dict['mon']:
            try:
                mon = ManufacturerOrderNumber.objects.get(manufacturer_order_number=item_dict['mon']['mon'],
                                                          manufacturer__name=item_dict['mon']['manufacturer'])
            except ManufacturerOrderNumber.DoesNotExist:
                fallback = {'manufacturer_order_number': item_dict['mon']}
        if item_dict['part']:
            try:
                part = Part.objects.get(manufacturer_part_number=item_dict['part']['mpn'],
                                        manufacturer__name=item_dict['part']['manufacturer'])
                if part is not None and mon is not None:
                    if mon.part != part:
                        logger.error(f"Parts don't match: MON part: {mon.part}, part: {part}, using MON part")
                        part = mon.part
            except Part.DoesNotExist:
                if fallback is None:
                    fallback = {}
                fallback['mpn'] = item_dict['part']['mpn']
                fallback['manufacturer'] = item_dict['part']['manufacturer']

        item = BOMItem(quantity=item_dict['quantity'],
                       bom=bom,
                       part_not_found_fallback=fallback,
                       part=part,
                       manufacturer_order_number=mon,
                       designators=item_dict['designators'],
                       note=item_dict['note'])
        item.save()
    return bom


def __process_project_file(project_filename, files_dir):
    logger.info(f"Importing project: {project_filename}")
    with open(project_filename, 'r') as project_file:
        project_dict = json.load(project_file)
        project = create_project(project_dict)
        logger.info(f"Adding BOMs for {project.name} project.")
        for bom in project_dict['boms']:
            create_bom(bom, project)


def import_project(workdir):
    if os.path.isdir(workdir):
        for project_file in os.listdir(workdir):
            if project_file.endswith('.json'):
                __process_project_file(workdir + '/' + project_file, workdir + '/files')
