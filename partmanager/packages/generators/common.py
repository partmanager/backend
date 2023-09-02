import tempfile
import subprocess


def save_freecad_script(package_data):
    with open(tempfile.gettempdir() + '/freecad_script.py', "w") as write_file:
        write_file.write("packages=")
        write_file.write(str(package_data))
        write_file.close()


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


def run(generate_packages, model):
    package_data = generate_packages()
    run_freecad()
    for data in package_data:
        package = model.objects.all().filter(pk=data['pk'])
        update_model(package[0], data['name'])
    # at last run:  find *.xhtml -type f -exec sed -i 's/ width="1280px"  height="1024px"//g' {} \;