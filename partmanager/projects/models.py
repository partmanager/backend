from django.db import models
from django.contrib.postgres.fields import ArrayField
from partmanager.choices import Status


class Project(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    # projectversion_set -> reverse relation from ForeignKey in ProjectVersion class


class ProjectVersion(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.PROTECT)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    # bom_set -> reverse relation from ForeignKey in BOM class
    # assembly_set -> reverse relation from ForeignKey in Assembly class

    class Meta:
        unique_together = ['name', 'project']
        ordering = ['project', 'name']

    def to_dict(self):
        project_dict = {'name': self.project.name,
                        'version': self.name,
                        'boms': []}
        for bom in self.bom_set.all():
            project_dict['boms'].append(bom.to_dict())

        return project_dict


class BOM(models.Model):
    name = models.CharField(max_length=200)
    note = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey('ProjectVersion', on_delete=models.CASCADE, related_name="bom_set")
    bom_file = models.FileField(upload_to='BOMs/', max_length=100, null=True,
                                blank=True)  # nice looking file that is used only for reference and manual verification
    raw_source_file = models.FileField(upload_to='BOMs/', max_length=100, null=True,
                                       blank=True)  # file used for bom import may be used for manual veriifcation
    # item_set -> reverse relation from ForeignKey in BOMItem class

    class Meta:
        unique_together = ['name', 'project']
        ordering = ['project', 'name']

    def to_dict(self):
        bom_dict = {'name': self.name,
                    'note': self.note,
                    'description': self.description,
                    'multiply': self.multiply,
                    'bom_file': self.bom_file.name,
                    'items': []}
        for item in self.item_set.all():
            bom_dict['items'].append(item.to_dict())
        return bom_dict


class BOMItem(models.Model):
    GROUP = (
        ('r', 'Resistors'),
        ('c', 'Capacitors'),
        ('l', 'Inductors'),
        ('t', 'Transistors'),
        ('d', 'Diodes'),
        ('i', 'Integrated Circuits'),
        ('k', 'Connectors'),
        ('m', 'Modules'),
        ('u', 'Unknown'),
    )

    bom = models.ForeignKey('BOM', on_delete=models.CASCADE, related_name="item_set")
    designators = ArrayField(models.CharField(max_length=10))
    group = models.CharField(max_length=1, choices=GROUP, default='u')
    part_not_found_fallback = models.JSONField(blank=True, null=True)
    part = models.ForeignKey('partcatalog.Part', on_delete=models.CASCADE, related_name="bom_item_set", blank=True,
                             null=True)
    manufacturer_order_number = models.ForeignKey('partcatalog.ManufacturerOrderNumber', on_delete=models.PROTECT,
                                                  related_name="bom_item_set", blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['bom', 'designators', 'part__manufacturer__name']

    def to_dict(self):
        item_dict = {'quantity': self.quantity,
                     'part': {'mpn': self.part.manufacturer_part_number,
                              'manufacturer': self.part.manufacturer.name} if self.part else None,
                     'mon': {'mon': self.manufacturer_order_number.manufacturer_order_number,
                             'manufacturer': self.manufacturer_order_number.part.manufacturer.name} if self.manufacturer_order_number else None,
                     'designators': self.designators,
                     'note': self.note}
        return item_dict

    def get_part_number_display(self):
        if self.manufacturer_order_number:
            return self.manufacturer_order_number.manufacturer_order_number
        elif self.part:
            return self.part.manufacturer_part_number
        elif self.part_not_found_fallback:
            if 'manufacturer_order_number' in self.part_not_found_fallback:
                return self.part_not_found_fallback['manufacturer_order_number']
            elif 'mpn' in self.part_not_found_fallback:
                return self.part_not_found_fallback['mpn']
            elif 'MPN' in self.part_not_found_fallback:
                return self.part_not_found_fallback['MPN']
            else:
                print(self.part_not_found_fallback)
                return "Unknown"

    def get_manufacturer_display(self):
        if self.part:
            return self.part.manufacturer.name
        else:
            return self.part_not_found_fallback['manufacturer']

    def __str__(self):
        return "{} -> {}, {}".format(self.bom.project.name, self.bom.name, self.get_part_number_display())


class AssemblyJob(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.DATA_PREPARATION)
    project_version = models.ForeignKey('ProjectVersion', on_delete=models.PROTECT, related_name="assembly_job_set")
    assembly_contractor = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField()
    rework = models.OneToOneField('Rework', on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ['name', 'project_version']
        ordering = ['project_version', 'name']

    def generate_from_bom(self):
        latest_sn = Assembly.objects.all().order_by('-serial_number').first()
        if latest_sn:
            print(latest_sn.serial_number)
            latest_sn = latest_sn.serial_number
        else:
            latest_sn = 0

        for i in range(self.quantity):
            serial_number = int(latest_sn) + 1 + i
            assembly = Assembly(project_version=self.project_version,
                                assembly_job=self,
                                serial_number=serial_number,
                                name=f"Autogenerated assembly {self.project_version.name} {serial_number}")
            assembly.save()

            rework = Rework(assembly=assembly,
                            name='Assembly')
            rework.save()
            self.rework = rework
            self.save()

            for item in self.project_version.bom_set.first().item_set.all():
                for designator in item.designators:
                    assembly_item = AssemblyItem(assembly=assembly,
                                                 rework=rework,
                                                 designator=designator,
                                                 part=item.part,
                                                 manufacturer_order_number=item.manufacturer_order_number)
                    assembly_item.save()


class Assembly(models.Model):
    project_version = models.ForeignKey('ProjectVersion', on_delete=models.PROTECT, related_name="assembly_set")
    assembly_job = models.ForeignKey('AssemblyJob', on_delete=models.PROTECT)
    serial_number = models.IntegerField(null=True)
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    component_cost = models.FloatField(null=True)
    build_cost = models.FloatField(null=True)
    # assembly_item_set -> reverse key from AssemblyItem class
    # rework_set -> reverse key from Rework class

    class Meta:
        unique_together = ['name', 'project_version']
        ordering = ['project_version', 'name']


class Rework(models.Model):
    assembly = models.ForeignKey('Assembly', on_delete=models.CASCADE, related_name="rework_set")
    name = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    closed = models.BooleanField(default=False)


class AssemblyItem(models.Model):
    assembly = models.ForeignKey('Assembly', on_delete=models.CASCADE, related_name="assembly_item_set")
    rework = models.ForeignKey('Rework', on_delete=models.CASCADE)
    designator = models.CharField(max_length=10)
    assembled = models.BooleanField(default=False)
    sourced_externally = models.BooleanField(default=False)
    part = models.ForeignKey('partcatalog.Part', on_delete=models.CASCADE, related_name="assembly_item_set", blank=True,
                             null=True) # delete
    manufacturer_order_number = models.ForeignKey('partcatalog.ManufacturerOrderNumber', on_delete=models.PROTECT,
                                                  related_name="assembly_item_set", blank=True, null=True)
    invoice_item = models.ForeignKey('invoices.InvoiceItem', on_delete=models.PROTECT, blank=True, null=True)
    LOT = models.CharField(max_length=20, null=True, blank=True, verbose_name="Lot number")
    note = models.CharField(max_length=200, blank=True, null=True)
    # inventoryreservation_set -> reverse key from InventoryReservation

    class Meta:
        unique_together = ['assembly', 'rework', 'designator']
        ordering = ['assembly', 'rework', 'designator', 'manufacturer_order_number', 'part']

from .signals import *