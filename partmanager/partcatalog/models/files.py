from django.db import models
from django.core.files.base import ContentFile
import requests


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

    def to_ajax_response(self):
        files = []
        for file in self.fileversion_set.all():
            files.append({'version': file.version, 'url': file.file.url, 'publicationDate': file.publication_date})
        return {'name': self.name,
                'url': self.url,
                'description': self.description,
                'fileType': self.get_file_type_display(),
                'versions': files}

    def __str__(self):
        if self.manufacturer:
            return '{}, {}, ({}), pk={}'.format(self.manufacturer.name, self.name, len(self.fileversion_set.all()), self.pk)
        return '{}, ({}), pk={}'.format(self.name, len(self.fileversion_set.all()), self.pk)


class FileVersion(models.Model):
    file_container = models.ForeignKey('partcatalog.File', on_delete=models.CASCADE)
    version = models.CharField(max_length=100)
    publication_date = models.DateField(auto_now=True)
    file = models.FileField(max_length=250, upload_to='partcatalog/files/')


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


