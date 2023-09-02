from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    # projectversion_set -> reverse relation from ForeignKey in ProjectVersion class


class ProjectVersion(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.PROTECT)
    # bom_set -> reverse relation from ForeignKey in BOM class
    # assembly_set -> reverse relation from ForeignKey in Assembly class

    class Meta:
        unique_together = ['name', 'project']
        ordering = ['project', 'name']

    def to_dict(self):
        project_dict = {'name': self.project.name,
                        'varsion': self.name,
                        'boms': []}
        for bom in self.bom_set.all():
            project_dict['boms'].append(bom.to_dict())

        return project_dict


class BOM(models.Model):
    name = models.CharField(max_length=200)
    note = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey('ProjectVersion', on_delete=models.PROTECT, related_name="bom_set")
    multiply = models.IntegerField(default=1)  # number of BOM instances per project
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

    quantity = models.IntegerField()
    bom = models.ForeignKey('BOM', on_delete=models.CASCADE, related_name="item_set")
    group = models.CharField(max_length=1, choices=GROUP, default='u')
    part_not_found_fallback = models.JSONField(blank=True, null=True)
    part = models.ForeignKey('partcatalog.Part', on_delete=models.CASCADE, related_name="bom_item_set", blank=True,
                             null=True)
    manufacturer_order_number = models.ForeignKey('partcatalog.ManufacturerOrderNumber', on_delete=models.PROTECT,
                                                  related_name="bom_item_set", blank=True, null=True)
    designators = models.TextField(blank=True, null=True)  # coma separated designator list
    note = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['bom', 'manufacturer_order_number__manufacturer__name']

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


class Assembly(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    quantity = models.IntegerField(default=1)
    project = models.ForeignKey('ProjectVersion', on_delete=models.PROTECT, related_name="assembly_set")
    build_cost = models.FloatField(null=True)
    # assembly_item_set -> reverse key from AssemblyItem class

    class Meta:
        unique_together = ['name', 'project']
        ordering = ['project', 'name']

    def save(self, *args, **kwargs):
        try:
            previous = Assembly.objects.get(pk=self.pk)
            super().save(*args, **kwargs)
            if previous.quantity != self.quantity:
                print("Updating assembly quantity")
                self.update_items()
        except Assembly.DoesNotExist:
            super().save(*args, **kwargs)
            self.update_items()

    def update_items(self):
        for bom in self.project.bom_set.all():
            for bom_item in bom.item_set.all():
                if bom_item.part is None and bom_item.manufacturer_order_number is None:
                    found = self.assembly_item_set.filter(
                        part_not_found_fallback=bom_item.part_not_found_fallback)
                    if len(found) == 0:
                        self.add_assembly_item(bom_item)
                    elif len(found) == 1:
                        self.update_assembly_item(found[0], bom_item)
                elif bom_item.manufacturer_order_number is not None:
                    found = self.assembly_item_set.filter(
                        manufacturer_order_number=bom_item.manufacturer_order_number)
                    if len(found) == 0:
                        self.add_assembly_item(bom_item)
                    elif len(found) == 1:
                        self.update_assembly_item(found[0], bom_item)
                else:
                    found = self.assembly_item_set.filter(part=bom_item.part)
                    if len(found) == 0:
                        self.add_assembly_item(bom_item)
                    elif len(found) == 1:
                        self.update_assembly_item(found[0], bom_item)

    def update_assembly_item(self, assembly_item, bom_item):
        assembly_item.quantity = assembly_item.quantity + bom_item.bom.multiply * bom_item.quantity
        origins = assembly_item.item_origins
        if bom_item.id not in origins:
            print(origins)
            assembly_item.item_origins.update(self._generate_origin_info(bom_item))
        assembly_item.save()

    def add_assembly_item(self, bom_item):
        part_not_found_fallback = {'Manufacturer': None, 'MPN': None, 'MON': None}
        if bom_item.manufacturer_order_number:
            part_not_found_fallback['Manufacturer'] = bom_item.manufacturer_order_number.manufacturer.name
            part_not_found_fallback['MPN'] = bom_item.part.manufacturer_part_number
            part_not_found_fallback['MON'] = bom_item.manufacturer_order_number.manufacturer_order_number
        elif bom_item.part:
            part_not_found_fallback['Manufacturer'] = bom_item.part.manufacturer.name
            part_not_found_fallback['MPN'] = bom_item.part.manufacturer_part_number
        else:
            part_not_found_fallback = bom_item.part_not_found_fallback

        assembly_item = AssemblyItem(assembly=self,
                                     quantity=bom_item.bom.multiply * bom_item.quantity,
                                     quantity_correction=0,
                                     group=bom_item.group,
                                     item_origins=self._generate_origin_info(bom_item),
                                     part=bom_item.part,
                                     manufacturer_order_number=bom_item.manufacturer_order_number,
                                     part_not_found_fallback=part_not_found_fallback)
        assembly_item.save()

    @staticmethod
    def _generate_origin_info(bom_item):
        origin = {bom_item.id: {'name': bom_item.bom.name,
                                'bom_id': bom_item.bom.id,
                                'bom_qty': bom_item.quantity,
                                'project_qty': bom_item.bom.multiply * bom_item.quantity,
                                'designators': bom_item.designators}}
        return origin


class AssemblyItem(models.Model):
    assembly = models.ForeignKey('Assembly', on_delete=models.CASCADE, related_name="assembly_item_set")
    quantity = models.IntegerField(default=1)
    quantity_correction = models.IntegerField(default=0)
    group = models.CharField(max_length=1, choices=BOMItem.GROUP, default='u')
    item_origins = models.JSONField(blank=True, null=True)
    part_not_found_fallback = models.JSONField(blank=True, null=True)
    part = models.ForeignKey('partcatalog.Part', on_delete=models.CASCADE, related_name="assembly_item_set", blank=True,
                             null=True)
    manufacturer_order_number = models.ForeignKey('partcatalog.ManufacturerOrderNumber', on_delete=models.PROTECT,
                                                  related_name="assembly_item_set", blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ['assembly', 'item_origins']
        ordering = ['assembly', 'group', 'manufacturer_order_number', 'part', 'part_not_found_fallback']

    def build_cost(self):
        price = 0
        for bom_item in self.bom.item_set.all():
            part = bom_item.part
            part_stock_detail = part.get_on_stock_quantity()
            assembly_quantity = bom_item.quantity * self.quantity
            on_stock_quantity = part_stock_detail['quantity']
            if assembly_quantity > on_stock_quantity:
                price = price + on_stock_quantity * part_stock_detail['average_price']
            else:
                price = price + assembly_quantity * part_stock_detail['average_price']
        return price
