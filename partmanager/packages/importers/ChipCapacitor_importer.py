from ..models.PackageTypes import PackageTypes
from ..models.ChipCapacitorPackage import ChipCapacitorPackage
from ..models.common import inch_to_mm
from .common import str_to_dimension_and_tolerance
from .ChipCommon import package_dimensions_to_name


class ChipCapacitorImporter:
    def get_or_create(self, package_data_dict):
        dimensions_dict = package_data_dict['dimensions']
        dimensions = decode_dimensions(dimensions_dict)
        size = package_dimensions_to_name(dimensions)
        name = f"{size}({inch_to_mm[size]})"
        return ChipCapacitorPackage.objects.get_or_create(
            type=PackageTypes.CAPACITOR_CHIP,
            name=name,
            description=ChipCapacitorPackage.generate_description(size, dimensions_dict),
            **dimensions
        )


def decode_dimensions(dimensions_dict):
    length = str_to_dimension_and_tolerance(dimensions_dict['Length'])
    width = str_to_dimension_and_tolerance(dimensions_dict['Width'])
    thickness_field_name = 'Thickness' if 'Thickness' in dimensions_dict else 'Height'
    thickness = str_to_dimension_and_tolerance(dimensions_dict[thickness_field_name])
    e = str_to_dimension_and_tolerance(dimensions_dict['e'])
    g = str_to_dimension_and_tolerance(dimensions_dict['g'])
    if g is None:
        g = {}
        g['value'] = length['value'] - 2 * e['value']
        g['tolerance_pos'] = None
        g['tolerance_neg'] = None
    dimensions = {'length_value': length['value'],
                  'length_tolerance_oversize': length['tolerance_pos'],
                  'length_tolerance_undersize': length['tolerance_neg'],
                  'width_value': width['value'],
                  'width_tolerance_oversize': width['tolerance_pos'],
                  'width_tolerance_undersize': width['tolerance_neg'],
                  'thickness_value': thickness['value'],
                  'thickness_tolerance_oversize': thickness['tolerance_pos'],
                  'thickness_tolerance_undersize': thickness['tolerance_neg'],
                  'e_value': e['value'],
                  'e_tolerance_oversize': e['tolerance_pos'],
                  'e_tolerance_undersize': e['tolerance_neg'],
                  'g_value': g['value'],
                  'g_tolerance_oversize': g['tolerance_pos'],
                  'g_tolerance_undersize': g['tolerance_neg']
                  }
    return dimensions