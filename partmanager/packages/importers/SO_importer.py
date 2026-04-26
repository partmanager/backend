from ..models.SOPackage import SOPackage
from ..models.common import inch_to_mm
from .common import decode_dimensions
from .ChipCommon import package_dimensions_to_name


class SOImporter:
    def get_or_create(self, package_data_dict):
        dimensions_dict = package_data_dict['dimensions']
        dimensions = decode_dimensions(dimensions_dict)
        size = package_dimensions_to_name(dimensions)
        name = str(f"{size}({inch_to_mm[size]})")
        description = SOPackage.generate_description(size, dimensions_dict)
        try:
            result = SOPackage.objects.get_or_create(
                type='SOPackage',
                name=name,
                description=description,
                **dimensions
            )
        except Exception as e:
            print("unable to get package", e)
            return None, False
        return result