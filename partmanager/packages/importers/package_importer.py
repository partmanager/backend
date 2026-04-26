from ..models.ChipResistorPackage import ChipResistorPackage
from ..models.ChipCapacitorPackage import ChipCapacitorPackage
from ..models.SOPackage import SOPackage
from .common import decode_dimensions
from .ChipCapacitor_importer import ChipCapacitorImporter
from .ChipResistor_importer import ChipResistorImporter
from .SO_importer import SOImporter

package_type_map = {
    "Chip Resistor": ChipResistorPackage,
    "Chip Capacitor": ChipCapacitorPackage,
    "SO": SOPackage,
    "SOIC": SOPackage,
}

def package_import(data_dict):
    if "type" in data_dict:
        type_name = data_dict['type']
        print("Processing package type:", type_name)
        if type_name in importers_map:
            try:
                return importers_map[type_name]().get_or_create(data_dict)
            except Exception as e:
                print(f"Exception during package processing: {e}")
        else:
            print("Unknown package type:", type_name)
    return None, False


importers_map = {
    'Chip Resistor': ChipResistorImporter,
    'Chip Capacitor': ChipCapacitorImporter,
    'Chip Inductor': ChipCapacitorImporter,
    'SO': SOImporter,
    "SOIC": SOImporter
}


def get_or_create_package_from_dict(package_dictionary):
    if 'package_type' in package_dictionary and 'dimensions' in package_dictionary:
        package_type = package_dictionary["package_type"]
        if package_type not in package_type_map:
            print("Unable to find package type", package_type)
            raise ValueError("Unsupported package type")
        else:
            dimensions = decode_dimensions(package_dictionary["dimensions"])
            print(dimensions)
            package_class = package_type_map[package_type]

            package_object, created = package_class.objects.get_or_create(
                type=package_type,
                name=package_dictionary["name"],
                description=package_class(package_dictionary["name"], dimensions),
                pin_count = package_dictionary["pin_count"],
                **dimensions)
            print(package_object, created)
            return package_object, created
    return None, False
