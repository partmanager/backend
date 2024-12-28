from django.db import models
from django.core.files.base import ContentFile
import requests
import pathlib


class File(models.Model):
    FILE_TYPE = [
        ('d', 'Datasheet'),
        ('u', 'Unspecified')
    ]
    name = models.CharField(max_length=250)
    file_type = models.CharField(max_length=1, choices=FILE_TYPE, default='u')
    url = models.URLField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    manufacturer = models.ForeignKey('manufacturers.Manufacturer', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.manufacturer:
            return '{}, {}, ({}), pk={}'.format(self.manufacturer.name, self.name, len(self.fileversion_set.all()), self.pk)
        return '{}, ({}), pk={}'.format(self.name, len(self.fileversion_set.all()), self.pk)


class FileVersion(models.Model):
    file_container = models.ForeignKey('partcatalog.File', on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    publication_date = models.DateField(auto_now=True)
    md5sum = models.CharField(max_length=100, null=True, unique=True)
    url = models.URLField(max_length=500, null=True, blank=True)
    file = models.FileField(max_length=250, upload_to='part_catalog/docs/')

    def generate_filename(self, name):
        filename = pathlib.Path(name)
        manufacturer_name = self.file_container.manufacturer.name.replace(' ', '_').lower()
        return f'part_catalog/docs/{manufacturer_name}/{filename.stem}__{self.md5sum}{"".join(filename.suffixes)}'


def create_file_version_from_url(file_model, filename, version, url):
    if url:
        if not url.startswith('http:') and not url.startswith('https:'):
            url = 'http://' + url
        response = requests.get(url, timeout=60)
        if response.status_code == 200:
            file_version = FileVersion(file_container=file_model, version=version)
            file_version.file.save(filename, ContentFile(response.content), save=True)
            file_version.save()
            return file_version


