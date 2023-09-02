import csv
import json


def controller_parameter_decoder(csv):
    manufacturer, controller, interface = csv.split(',')
    return {'manufacturer': manufacturer.strip(), 'part number': controller.strip(), 'interface': interface.strip()}


def backlight_parameter_decoder(csv):
    source, color = csv.split(',')
    return {'source': source.strip(), 'color': color.strip()}


def resolution_parameter_decoder(csv):
    width, height = csv.split('x')
    return {'width': width.strip(), 'height': height.strip()}


class CSVToJsonBase:
    def __init__(self):
        self.parts = dict()
        self.file_types = ['datasheet', 'STEP', 'General Technical Information', 'S parameter', 'File STEP',
                           'Datasheet', 'General Technical Information']
        self.balun_parameters = ['Operating Frequency Range', 'Unbalanced Port Impedance',
                                 'Balanced Port Impedance',
                                 'Unbalanced Port Return Loss', 'Phase Balance', 'Amplitude Balance', 'Insertion Loss',
                                 'Power Rating']
        self.battery_parameters = ['Nominal Voltage', 'Nominal Internal Resistance', 'Capacity']
        self.battery_holder_parameters = ['Battery Count']
        self.bridge_rectifier_parameters = ['V_RRM Peak Repetitive Reverse Voltage',
                                            'V_RWM Working Peak Reverse Voltage', 'V_R DC Blocking Voltage',
                                            'V_R(RMS) RMS Reverse Voltage', 'I_O Average Rectified Output Current',
                                            'R_θJA Thermal Resistance, Junction to Ambient',
                                            'R_θJC  Thermal Resistance, Junction to Case',
                                            'R_θJL Thermal Resistance, Junction to Lead',
                                            'V_(BR)R Reverse Breakdown Voltage', 'V_F Forward Voltage (per element)',
                                            'I_R Leakage Current (per element)', 'C_T Total Capacitance (per element)']
        self.capacitor_parameters = []
        self.common_mode_chokes_parameters = ['Rated Current', 'DC Resistance', 'Impedance']
        self.connector_parameters = ['Pin Spacing', 'Row Count', 'Pin Count', 'Row Spacing', 'Height from PCB',
                                     'Pin Height', 'Pin Height from PCB', 'Housing Height']
        self.crystal_parameters = ['Load Capacitance', 'Shunt Capacitance', 'ESR', 'Drive Level', 'Ageing']
        self.diode_parameters = ['Forward Voltage', 'Reverse Current', 'Junction Capacitance',
                                 'I_F',
                                 'I_FRM',
                                 'I_FSM',  # Surge Forward Current
                                 'Power Rating', 'V_BR', 't_rr',
                                 'V_RRM',
                                 'V_R',  # Reverse Voltage
                                 'V_RSM'  # Peak Repetitive Reverse Voltage
                                 ]
        self.enclosure_parameters = ['Enclosure Type', 'Length', 'Width', 'Height', 'PCB Length', 'PCB Width']
        self.esd_suppressor_parameters = ['Rated Voltage', 'Clamping Voltage', 'Trigger Voltage', 'Capacitance',
                                          'Attenuation', 'Leakage Current', 'ESD pulse withstand', 'Directions']
        self.fuse_parameters = ['Voltage Drop', 'Melting Integral', 'Breaking Capacity']
        self.inductor_parameters = ['Inductance', 'DCR', 'DC Rated Current', 'DC Saturation Current', 'SRF', 'Q',
                                    'Heat Reating Current', 'Rated Operating Voltage']
        self.integrated_circuits = ['Package', 'Supply Voltage Range', 'Supply Voltage 2 Range']
        self.led_parameters = ['IF Continuous', 'IF Peak', 'VF', 'VR', 'I_R', 'Viewing Angle', 'Luminous Intensity']
        self.lightpipe_parameters = ['Lights Count', 'Length', 'Panel Cutout Diameter']
        self.ptc_fuse_parameters = ['Resistance 1h after tripping', 'Trip time', 'Trip Current', 'Tripped Power Dissipation', 'Hold Current', 'Max fault current']
        self.relay_parameters = ['Coil Voltage', 'Coil Must Release Voltage', 'Coil Resistance', 'Coil Power',
                                 'Switching Voltage', 'Switching Current', 'Contact Resistance',
                                 'Contact Operating Life', 'Operating time', 'Release time']
        self.resistors_parameters = ['Resistance', 'Rated Power', 'TCR', 'Working Voltage', 'Overload Voltage',
                                     'Dielectric Withstanding Voltage']
        self.resistor_array_parameters = ['Elements Count', 'Resistance', 'TCR', 'Power Rating Per Resistor',
                                          'Power Rating Package', 'Working Voltage', 'Overload Voltage']
        self.surge_arrester_parameters = ['DC Spark-Over Voltage', 'Insulation Resistance', 'Capacitance',
                                           'Arc voltage', 'Glow voltage', 'Arc to glow transition']
        self.switch_parameters = ['Position Count', 'Pin Pitch', 'Switching Voltage',
                                  'Switching Current', 'Contact Resistance', 'Insulation Resistance', 'Operating Life']
        self.transistor_string_parameters = ['Drain Source Breakdown Voltage', 'Forward Transconductance']
        self.varistor_parameters = ['DC Voltage', 'Varistor Voltage', 'RMS Voltage']

        self.parameter_name = ['Supply Voltage', 'Supply Current', 'Stand-by Current', 'Frequency',
                               'Frequency Stability Over Operating Temperature Range', 'Rise Time', 'Fall Time',
                               'Start-up Time', 'Output Load', 'Peak to Peak Jitter', 'RMS Jitter', 'Ageing',
                               'Enable pin',
                               'Tri-state Output'] + \
                              self.balun_parameters + self.battery_parameters + self.battery_holder_parameters + \
                              self.bridge_rectifier_parameters + self.common_mode_chokes_parameters + self.connector_parameters + self.crystal_parameters + self.diode_parameters + \
                              self.enclosure_parameters + self.esd_suppressor_parameters + self.fuse_parameters + self.inductor_parameters + self.led_parameters + self.lightpipe_parameters + \
                              self.ptc_fuse_parameters + self.relay_parameters + self.resistors_parameters + self.resistor_array_parameters + \
                              self.surge_arrester_parameters + self.switch_parameters + self.transistor_string_parameters + self.integrated_circuits + \
                              self.varistor_parameters
        # --------------------------- string parameters
        self.balun_string_parameters = ['Technology']
        self.battery_string_parameters = ['Battery Type', 'Battery Classification']
        self.battery_holder_string_parameters = ['Battery Type']
        self.capacitor_string_parameters = ['Dielectric Type', 'Dielectric Withstanding Voltage']
        self.connector_string_parameters = ['Contact Position', 'Bus Type', 'Pin Spacing', 'Row Count', 'Pin Count', 'Row Spacing', 'Wire Range', 'Height from PCB', 'Pin Height', 'Pin Height from PCB', 'Housing Height']
        self.crystal_string_parameters = ['Vibration Mode']
        self.display_parameters = ['Resolution', 'Controller', 'Controller Interface', 'Backlight', 'Backlight Color']
        self.enclosure_string_parameters = ['Material', 'Color', 'Flame Rating', 'IP Rating']
        self.lightpipe_string_parameters = ['Shape', 'Color']
        self.module_string_parameters = ['Module Type', 'Key']
        self.relay_string_parameters = ['Contact Configuration']
        self.switch_string_parameters = ['Switch Type', 'Configuration']
        self.transistor_string_parameters = []
        self.string_parameter_name = self.balun_string_parameters + self.battery_string_parameters + \
                                     self.battery_holder_string_parameters + self.capacitor_string_parameters + \
                                     self.connector_string_parameters + self.crystal_string_parameters + \
                                     self.display_parameters + \
                                     self.enclosure_string_parameters + self.lightpipe_string_parameters + \
                                     self.module_string_parameters + self.relay_string_parameters + self.switch_string_parameters

        self.parameter_decoder = {'Controller': controller_parameter_decoder,
                                  'Backlight': backlight_parameter_decoder,
                                  'Resolution': resolution_parameter_decoder}

    def get_parts_list(self):
        return [self.parts[x] for x in sorted(self.parts)]

    def parts_import(self, filename, dry=False):
        self.parts = dict()
        print("Importing parts from csv file")
        self.parts_load(filename)
        self.run(dry=dry)

    def export(self, filename):
        print("Exporting", len(self.parts), " parts to", filename)
        with open(filename, 'w') as json_file:
            partlist = self.get_parts_list()
            json.dump(partlist, json_file, indent=4)

    def parts_load(self, filename):
        with open(filename) as csvfile:
            csvreader = csv.DictReader(csvfile, dialect='unix')
            self.validate_parameters(csvreader.fieldnames, filename)
            for row in csvreader:
                part_json = self.csv_data_to_json(row)
                self.create_or_update_part(part_json)

    def validate_parameters(self, keys, filename):
        common_parameters = {'Manufacturer', 'Part Number', 'Production Status', 'Marking Code', 'Part Type', 'Series',
                             'Series Description', 'Description', 'Product URL', 'Notes', 'MSLevel',
                             'Storage Temp Range', 'Storage Humidity', 'Order Number', 'Symbol'}
        packaging_parameters = {'Packaging Qty', 'Packaging Code', 'Packaging Type',
                                'Tape D1', 'Tape D', 'Tape B1',  'Tape T', 'Reel Diameter', 'Working Temp Range',
                                'Tape P2', 'Tape K', 'Tape F', 'Tape W', 'Tape A0', 'Tape E', 'Reel Width', 'Tape P1',
                                'Tape B0', 'Tape Pin 1 Quadrant', 'Tape SO', 'Tape A1',  'Tape P0'}
        package_parameters = {'Package Height', 'Package l2', 'Package Type', 'Package l1', 'Package Length',
                              'Package Width', 'Package e', 'Weight'}
        files = set()
        for file in self.file_types:
            files.add("File " + file)
        csv_keys_set = set(keys)
        part_parameters_set = common_parameters
        part_parameters_set.update(packaging_parameters)
        part_parameters_set.update(package_parameters)
        part_parameters_set.update(files)
        part_parameters_set.update(self.parameter_name)
        part_parameters_set.update(self.string_parameter_name)
        additional_keys = csv_keys_set - part_parameters_set
        assert len(additional_keys) == 0, "CSV to JSON. Found unknown field, aborting" + str(additional_keys) + "in file: " + str(filename)

    def get_part(self, part_hash, manufacturer, part_number):
        if part_hash in self.parts:
            return self.parts[part_hash]
            #for part in self.parts:
            #    if part['manufacturer'] == manufacturer and part['partNumber'] == part_number:
            #        return part

    def create_or_update_part(self, part_json):
        part_hash = '{}_{}'.format(part_json['manufacturer'], part_json['partNumber'])
        #hashable_part_json = hashabledict(part_json)
        part = self.get_part(part_hash, part_json['manufacturer'], part_json['partNumber'])
        if part:
            self.update_part(part, part_json)
        else:
            #self.parts.append(part_json)
            self.parts[part_hash] = part_json

    def update_part(self, part, to_update):
        if self.compare_parts(part, to_update):
            new_order_numbers = list(to_update['orderNumbers'].keys())
            assert len(new_order_numbers) == 1
            if new_order_numbers[0] in part['orderNumbers']:
                assert False, "Already in order numbers: " + str(new_order_numbers[0])
            else:
                part['orderNumbers'].update(to_update['orderNumbers'])
        else:
            assert False, 'Part should be equal'

    def compare_parts(self, a, b):
        def all_fields_are_empty(dictionary):
            for key in dictionary:
                if dictionary[key] is not None and dictionary[key] != '':
                    return False
            return True

        for field in ['manufacturer', 'partNumber', 'productionStatus', 'markingCode', 'partType', 'series',
                      'description', 'productUrl', 'notes', 'tags', 'storageConditions', 'parameters', 'files',
                      'package', 'symbol&footprint']:
            if a[field] != b[field] and (b[field] is not None and b[field] != ''):
                if isinstance(b[field], dict) and not all_fields_are_empty(b[field]):
                    print(
f"""
Comparision of {a['partNumber']} and {b['partNumber']} failed,
\tfield "{field}" differ:
\t\tPart A: {a[field]}
\t\tPart B: {b[field]}
""")
                    return False
        return True

    def csv_data_to_json(self, csv_row):
        return {'manufacturer': csv_row['Manufacturer'],
                'partNumber': csv_row['Part Number'],
                'productionStatus': csv_row['Production Status'],
                'markingCode': csv_row['Marking Code'],
                'partType': csv_row['Part Type'],
                'series': {'name': csv_row['Series'], 'description': csv_row['Series Description']},
                'description': csv_row['Description'] if 'Description' in csv_row else '',
                'productUrl': csv_row['Product URL'],
                'notes': csv_row['Notes'],
                'tags': [],
                'storageConditions': {'temperature': csv_row['Storage Temp Range'],
                                      'humidity': '',
                                      'MSLevel': csv_row['MSLevel']},
                'parameters': self.parameters_to_json(csv_row),
                'files': self.files_to_json(csv_row),
                'package': self.package_to_json(csv_row),
                'symbol&footprint': self.symbol_and_footprint_to_json(csv_row),
                'orderNumbers': {csv_row['Order Number']: self.packaging_to_json(csv_row)}
                }

    def parameters_to_json(self, csv_row):
        parameters = {}
        for key in csv_row:
            if csv_row[key]:
                if key in self.parameter_decoder:
                    parameters[key] = self.parameter_decoder[key](csv_row[key])
                elif key in self.parameter_name:
                    parameters[key] = self.decode_parameter(csv_row[key])
                elif key in self.string_parameter_name:
                    parameters[key] = csv_row[key]
        return parameters

    def decode_parameter(self, parameter_str):
        if '|' in parameter_str:
            parameters = []
            for parameter in parameter_str.split('|'):
                if '@' in parameter:
                    value, condition = parameter.split('@')
                    parameters.append({'value': value.strip(), 'conditions': self.process_conditions(condition)})
                else:
                    parameters.append({'value': parameter})
            return parameters
        else:
            if '@' in parameter_str:
                value, condition = parameter_str.split('@')
                return {'value': value.strip(), 'conditions': self.process_conditions(condition)}
            else:
                return {'value': parameter_str}

    def process_conditions(self, conditions_string):
        #print(conditions_string)
        conditions = {}
        for condition in conditions_string.split(','):
            key_str, value = condition.split('=')
            key = key_str.strip()
            assert key not in conditions
            conditions[key] = value.strip()
        return conditions

    def symbol_and_footprint_to_json(self, csv_row):
        return {'symbolName': csv_row['Symbol'],
                'pinmap': {},
                'footprints': []}

    def files_to_json(self, csv_row):
        files = {}
        for key in csv_row:
            if 'File' in key:
                file_type = key.replace('File', '').strip()
                if file_type in self.file_types:
                    assert file_type not in files, "File already added, possible file overwrite."
                    files[file_type] = csv_row[key]
                else:
                    print("Unsupported file type:", file_type)
        return files

    def package_to_json(self, csv_row):
        if csv_row['Package Type']:
            return {'name': csv_row['Package Type']}
        else:
            return {}

    def packaging_to_json(self, csv_row):
        return {'Packaging Code': csv_row['Packaging Code'],
                'Packaging Type': csv_row['Packaging Type'],
                'Packaging Qty': csv_row['Packaging Qty'],
                'Packaging Data': self.packaging_detail_to_json(csv_row['Packaging Type'], csv_row)}

    def packaging_detail_to_json(self, packaging_type, csv_row):
        if 'Tape' in packaging_type:
            return self.tape_reel_packaging_to_json(csv_row)
        else:
            return {}

    def tape_reel_packaging_to_json(self, csv_row):
        return {"Reel Diameter": csv_row['Reel Diameter'],
                "Reel Width": csv_row['Reel Width'],
                "Tape Pin 1 Quadrant": csv_row['Tape Pin 1 Quadrant'],
                "Tape W": csv_row['Tape W'],
                "Tape E": csv_row['Tape E'],
                "Tape F": csv_row['Tape F'],
                "Tape SO": csv_row['Tape SO'],
                "Tape P0": csv_row['Tape P0'],
                "Tape P1": csv_row['Tape P1'],
                "Tape P2": csv_row['Tape P2'],
                "Tape D": csv_row['Tape D'],
                "Tape D1": csv_row['Tape D1'],
                "Tape A0": csv_row['Tape A0'],
                "Tape A1": csv_row['Tape A1'],
                "Tape B0": csv_row['Tape B0'],
                "Tape B1": csv_row['Tape B1'],
                "Tape T": csv_row['Tape T'],
                "Tape K": csv_row['Tape K']
                }
