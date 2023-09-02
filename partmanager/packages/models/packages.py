from .ChipResistorPackage import ChipResistorPackage
from .ChipCapacitorPackage import ChipCapacitorPackage


def get_package(package_type, name, dimensions):
    if package_type == 'Chip Capacitor':
        return ChipCapacitorPackage.objects.filter(type='Chip Capacitor',
                                                   name=name,
                                                   **dimensions)
    if package_type == 'Chip Resistor':
        return ChipResistorPackage.objects.filter(type='Chip Resistor',
                                                  name=name,
                                                  **dimensions)


def add_package(package_type, name, dimensions):
    package = get_package(package_type, name, dimensions)
    if package:
        return package[0]
    elif package_type == 'Chip Capacitor':
        print("Package not found, adding new package:", name, "L=", dimensions['length_value'], "W=", dimensions['width_value'],
              "T=", dimensions['thickness_value'])
        record = ChipCapacitorPackage.create(name, dimensions)
        record.save()
        return record
    elif package_type == 'Chip Resistor':
        print("Package not found, adding new package:", name, "L=", dimensions['length_value'], "W=", dimensions['width_value'],
              "T=", dimensions['thickness_value'])
        record = ChipResistorPackage.create(name, dimensions)
        record.save()
        return record
