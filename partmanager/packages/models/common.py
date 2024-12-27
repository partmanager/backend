from django.db import models
from .fields import Dimension
from polymorphic.models import PolymorphicModel


inch_to_mm = {'008004': '0201M',
              '0075': '0315',
              '01005': '0402',
              '0100': '0402',
              '015008': '05025M',
              '015015': '0404',
              '0102': '0306',
              '0201': '0603',
              '0204': '0510',
              '0306': '0816',
              '0402': '1005',
              '0603': '1608',
              '0704': '1810',
              '0805': '2012',
              '1206': '3216',
              '1210': '3225',
              '1218': '3245',
              '1806': '4516',
              '1808': '4520',
              '1812': '4532',
              '2010': '5025',
              '2020': '5050',
              '2220': '5750',
              '2412': '6232',
              '2512': '6432',
              '3637': '9194'}

mm_to_inch = {'0201M': '008004',
              '0402': '01005',
              '05025M': '015008',
              '0404': '015015',
              '0603': '0201',
              '1005': '0402',
              '1608': '0603',
              '1810': '0704',
              '2012': '0805',
              '3216': '1206',
              '3225': '1210',
              '4516': '1806',
              '4520': '1808',
              '4532': '1812',
              '5025': '2010',
              '5050': '2020',
              '5750': '2220',
              '6232': '2412',
              '6432': '2512',
              '9194': '3637'}


class Package(PolymorphicModel):
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    generated = models.BooleanField(default=False)
    freecad_file = models.FilePathField(path="/partmanager/packages/static/package_image",
                                        recursive=True, allow_files=True, allow_folders=False, max_length=200,
                                        blank=True, null=True)
    iges_file = models.FilePathField(path="/partmanager/packages/static/package_image",
                                     recursive=True, allow_files=True, allow_folders=False, max_length=200,
                                     blank=True, null=True)
    xhtml_file = models.FilePathField(path="/partmanager/packages/static/package_image",
                                      recursive=True, allow_files=True, allow_folders=False, max_length=200,
                                      blank=True, null=True)
    step_file = models.FilePathField(path="/partmanager/packages/static/package_image",
                                     recursive=True, allow_files=True, allow_folders=False, max_length=200,
                                     blank=True, null=True)
    rendering_png_file = models.FilePathField(path="/partmanager/packages/static/package_image",
                                              recursive=True, allow_files=True, allow_folders=False, max_length=200,
                                              blank=True, null=True)


class ChipPackageBase(Package):
    length = Dimension()  # in mm
    width = Dimension()  # in mm
    thickness = Dimension()  # in mm

    class Meta:
        abstract = True

    @property
    def dimensions(self):
        return {'length': ["{} mm".format(self.length), "+{} mm".format(self.length_tolerance_positive),
                           "{} mm".format(self.length_tolerance_negative)],
                'width': ["{} mm".format(self.width), "+{} mm".format(self.width_tolerance_positive),
                          "{} mm".format(self.width_tolerance_negative)],
                'thickness': ["{} mm".format(self.thickness), "+{} mm".format(self.thickness_tolerance_positive),
                              "{} mm".format(self.thickness_tolerance_negative)]}

    @property
    def case_code_metric(self):
        return inch_to_mm[self.name]

    @property
    def case_code_imperial(self):
        return self.name

    def __str__(self):
        return self.type + ' ' + self.name + '(' + inch_to_mm[self.name] + ')'


