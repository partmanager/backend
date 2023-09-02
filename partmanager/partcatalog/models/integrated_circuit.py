from .part import Part
from .fields.supply_voltage_range import SupplyVoltageRange


class IntegratedCircuit(Part):
    part_type_subset = list(dict(dict(Part.PART_TYPE)['Integrated Circuits']).keys())
    supply_voltage = SupplyVoltageRange()
