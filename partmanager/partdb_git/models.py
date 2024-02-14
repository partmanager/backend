from django.db import models


class GitImportStatus(models.Model):
    part_db_name = models.CharField(max_length=200, unique=True)
    part_db_last_import_commit = models.CharField(max_length=40)

    class Meta:
        ordering = ['part_db_name', 'part_db_last_import_commit']
