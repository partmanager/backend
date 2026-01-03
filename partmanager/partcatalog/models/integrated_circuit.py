from .part import Part
from .fields.supply_voltage_range import SupplyVoltageRange
from .choices import PART_TYPE


class IntegratedCircuit(Part):
    part_type_subset = list(dict(dict(PART_TYPE)['Integrated Circuits']).keys())
    supply_voltage = SupplyVoltageRange()
