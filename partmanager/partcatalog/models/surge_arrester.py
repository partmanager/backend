from .part import Part
from .fields.capacitance import CapacitanceAtFreq
from .fields.current import CurrentAtTemp
from .fields.insulation_resistance import InsulationResistance
from .fields.voltage import Voltage


class SurgeArrester(Part):
    dc_spark_over_voltage = Voltage()
    arc_voltage = Voltage()
    glow_voltage = Voltage()
    glow_to_arc_transition_current = CurrentAtTemp()
    insulation_resistance = InsulationResistance()
    capacitance = CapacitanceAtFreq()

    def generate_description(self):
        description = "Surge Arrester {}".format(self.dc_spark_over_voltage)
        if self.capacitance:
            description = description + ", " + str(self.capacitance)
        return description
