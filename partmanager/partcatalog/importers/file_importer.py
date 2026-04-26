import os
import logging
from urllib.parse import urlparse
from partcatalog.models.files import FileVersion, File


logger = logging.getLogger('partcatalog')


def add_files(part, files_json):
    files = []
    for file_type_str in files_json:
        file_dict = files_json[file_type_str]
        manufacturer = part.manufacturer
        parsed_file = get_or_create_file(manufacturer, file_dict)
        if 'varsions' in file_dict:
            create_or_update_file_versions(parsed_file, file_dict['versions'])

        if parsed_file not in part.files.all():
            part.files.add(parsed_file)
    part.save()
    return files


def get_filetype(field):
    if 'datasheet' in field:
        return 'd'
    if 'SPICEmodel' in field:
        return 'm'
    if 'Sparameter' in field:
        return 'p'
    else:
        return 'u'


def get_or_create_file(manufacturer, file_data):
    parsed_url = urlparse(file_data['url'])
    filename = os.path.basename(parsed_url.path)
    defaults = {
        "file_type": get_filetype(file_data),
        "description": file_data['description'] if 'description' in file_data else None,
    }
    obj, created = File.objects.update_or_create(
        url=file_data['url'],
        name=filename,
        manufacturer=manufacturer,
        defaults=defaults
    )
    if created:
        logger.info(f"File {filename} created")
    return obj


def create_or_update_file_versions(parsed_file, file_dict):
    for file_version in file_dict['versions']:
        file_version_dict = file_dict['versions'][file_version]
        create_or_update_file_version(parsed_file, file_version, file_version_dict)


def create_or_update_file_version(file_model, file_version, file_version_dict):
    if 'md5sum' not in file_version_dict:
        logger.error(f"Missing required 'md5sum' key for {file_model.name}, version: {file_version}")
    else:
        update_data = {
            'file_container': file_model,
            'version': file_version,
            'publication_date': file_version_dict['date'],
            'url': file_version_dict['url'] if 'url' in file_version_dict else None,
        }
        file_version, created = FileVersion.objects.update_or_create(
            md5sum=file_version_dict['md5sum'],
            defaults=update_data
        )
        if created:
            logger.info(f"File {file_version} created")
        file_version_name = file_version.generate_filename(file_model.name)
        if not file_version.file.name:
            file_version.file.name = file_version_name
            file_version.save()
            logger.info(f"Assigned existing file into {file_version}")