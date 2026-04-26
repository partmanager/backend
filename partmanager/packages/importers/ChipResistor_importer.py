from ..models.ChipResistorPackage import ChipResistorPackage
from ..models.common import inch_to_mm
#from .common import decode_dimensions
from .ChipCommon import package_dimensions_to_name
from .common import str_to_dimension_and_tolerance


class ChipResistorImporter:
    def get_or_create(self, package_data_dict):
        dimensions_dict = package_data_dict['dimensions']
        dimensions = decode_dimensions(dimensions_dict)
        size = package_dimensions_to_name(dimensions)
        name = str(f"{size}({inch_to_mm[size]})")
        description = ChipResistorPackage.generate_description(size, dimensions_dict)
        try:
            result = ChipResistorPackage.objects.get_or_create(
                type='Chip Resistor', #PackageTypes.RESISTOR_CHIP,
                name=name,
                description=description,
                **dimensions
            )
        except Exception as e:
            print("unable to get package", e)
            return None, False
        return result


def decode_dimensions(dimensions_dict):
    length = str_to_dimension_and_tolerance(dimensions_dict['l'])
    width = str_to_dimension_and_tolerance(dimensions_dict['w'])
    thickness_field_name = 'thickness' if 'thickness' in dimensions_dict else 'h'
    thickness = str_to_dimension_and_tolerance(dimensions_dict[thickness_field_name])
    t1 = str_to_dimension_and_tolerance(dimensions_dict['t1'])
    t2 = str_to_dimension_and_tolerance(dimensions_dict['t2'])
    dimensions = {
        'length_value': length['value'],
        'length_tolerance_oversize': length['tolerance_oversize'],
        'length_tolerance_undersize': length['tolerance_undersize'],
        'width_value': width['value'],
        'width_tolerance_oversize': width['tolerance_oversize'],
        'width_tolerance_undersize': width['tolerance_undersize'],
        'thickness_value': thickness['value'],
        'thickness_tolerance_oversize': thickness['tolerance_oversize'],
        'thickness_tolerance_undersize': thickness['tolerance_undersize'],
        't1_value': t1['value'],
        't1_tolerance_oversize': t1['tolerance_oversize'],
        't1_tolerance_undersize': t1['tolerance_undersize'],
        't2_value': t2['value'],
        't2_tolerance_oversize': t2['tolerance_oversize'],
        't2_tolerance_undersize': t2['tolerance_undersize']
    }
    return dimensions