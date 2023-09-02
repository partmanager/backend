from packages.models import ChipResistorPackage
from .common import save_freecad_script
from .common import run as common_run


def generate_packages():
    packages = ChipResistorPackage.objects.all()
    package_data = []
    for package in packages:
        length = package.length + package.length_tolerance_positive
        width = package.width + package.width_tolerance_positive
        thickness = package.thickness + package.thickness_tolerance_positive
        length_code = str(int(length * 1000))
        width_code = str(int(width * 1000))
        thickness_code = str(int(thickness * 1000))
        """
            Filename structure:
            chip_capacitor_ <case code imperial> ( <case code metric> )_ <length> x <width> x <thickness> _ <primary key>
            ie.:
            chip_capacitor_2220(5750)_6100x5400x2700_32140
        """
        name = 'chip_resistor_' + package.case_code_imperial + '(' + package.case_code_metric + ')_' + \
               length_code + 'x' + width_code + 'x' + thickness_code + '_' + str(package.pk)
        package_data.append({'name': name,
                             'pk': package.pk,
                             'dimensions': {'length': str(length),
                                            'width': str(width),
                                            'thickness': str(thickness),
                                            't1': '0.05',
                                            't2': '0.05'}})
    save_freecad_script(package_data)
    return package_data


def run():
    return common_run(generate_packages, ChipResistorPackage)