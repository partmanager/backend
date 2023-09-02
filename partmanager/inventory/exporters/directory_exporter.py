import time
import os
import json


def create_json_file(filename, inventory_positions):
    inventory_positions_array = []
    for inventory_position in inventory_positions:
        inventory_positions_array.append(inventory_position.to_dict())
    with open(filename, 'w') as inventory_file:
        json.dump(inventory_positions_array, inventory_file)


def export(inventory_positions, storage_locations, categories, workdir=None):
    if workdir is None:
        workdir = '/tmp/inventory_export/' + time.strftime("%Y%m%d-%H%M%S")
    os.makedirs(workdir)
    os.makedirs(workdir + '/files')

    create_json_file(workdir + '/inventory_positions.json', inventory_positions)
    create_json_file(workdir + '/storage_locations.json', storage_locations)
    create_json_file(workdir + '/categories.json', categories)
    return workdir
