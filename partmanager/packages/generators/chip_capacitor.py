import subprocess

from packages.models import ChipCapacitorPackage
import tempfile


def generate_packages():
    packages = ChipCapacitorPackage.objects.all()
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
        name = 'chip_capacitor_' + package.case_code_imperial + '(' + package.case_code_metric + ')_' + \
               length_code + 'x' + width_code + 'x' + thickness_code + '_' + str(package.pk)
        package_data.append({'name': name,
                             'pk': package.pk,
                             'dimensions': {'length': str(length),
                                            'width': str(width),
                                            'thickness': str(thickness),
                                            'terminal_size': '0.14'}})

    with open(tempfile.gettempdir() + '/freecad_script.py', "w") as write_file:
        write_file.write("packages=")
        write_file.write(str(package_data))
        write_file.close()
    return package_data


def run_freecad():
    subprocess.run(["freecad-daily", "../../generators/freecad_projects/freecad_export.py"],
                   cwd="packages/static/package_image")


def update_model(package_model, filename):
    print(package_model.name)
    path = "/home/pokas/work/django/partmanager/packages/static/package_image/"
    package_model.freecad_file = path + filename + ".FCStd"
    package_model.iges_file = path + filename + ".iges"
    package_model.xhtml_file = path + filename + ".xhtml"
    package_model.step_file = path + filename + ".step"
    package_model.rendering_png_file = path + filename + ".png"
    package_model.save()


def run():
    package_data = generate_packages()
    run_freecad()
    for data in package_data:
        package = ChipCapacitorPackage.objects.all().filter(pk=data['pk'])
        update_model(package[0], data['name'])
    # at last run:  find *.xhtml -type f -exec sed -i 's/ width="1280px"  height="1024px"//g' {} \;

