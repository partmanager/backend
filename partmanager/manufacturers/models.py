from django.db import models
from django.db.models import Count, F
from django.db.models import Q


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=500, unique=True, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    comment = models.CharField(max_length=2000, null=True, blank=True)
    # logo = models.ImageField()

    class Meta:
        ordering = ['name', 'full_name']

    @property
    def part_count(self):
        return len(self.part_set.all())

    @property
    def order_number_count(self):
        return len(self.manufacturerordernumber_set.all())

    def series(self):
        series_data = self.part_set.order_by('series').values('series', 'series_description', 'part_type').annotate(
            partCount=Count('manufacturer_part_number', distinct=True),
            orderNumberCount=Count('manufacturer_order_number_set'))
        return list(series_data)

    def __str__(self):
        return self.name

    def to_dict(self):
        manufacturer_dict = {'id': self.pk,
                             'name': self.name,
                             'full_name': self.full_name,
                             'address': self.address,
                             'website': self.website,
                             'email': self.email,
                             'phone': self.phone,
                             'comment': self.comment}
        return manufacturer_dict


def get_manufacturer_by_name(manufacturer_name):
    if manufacturer_name is not None:
        manufacturer = Manufacturer.objects.filter(Q(name__iexact=manufacturer_name) | Q(full_name__iexact=manufacturer_name))
        if manufacturer:
            if len(manufacturer) == 1:
                return manufacturer[0]
            else:
                raise RuntimeError("Multiple manufacturers with the same name found: " + str(manufacturer_name), manufacturer)


def get_or_create_manufacturer_by_name(manufacturer_name):
    manufacturer = get_manufacturer_by_name(manufacturer_name)
    if manufacturer is None and manufacturer_name is not None:
        manufacturer = Manufacturer(name=manufacturer_name)
        manufacturer.save()
    return manufacturer
