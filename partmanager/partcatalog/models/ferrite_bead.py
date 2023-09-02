from .part import Part
from .fields.current import CurrentAtTemp
from .fields.impedance import ImpedanceAtFreq
from .fields.resistance import ResistanceAtTemp


class FerriteBead(Part):
    part_type_subset = ['FB']
    impedance_max_values_count = 4
    impedance_1 = ImpedanceAtFreq()
    impedance_2 = ImpedanceAtFreq()
    impedance_3 = ImpedanceAtFreq()
    impedance_4 = ImpedanceAtFreq()
    dc_rated_current_max_values_count = 4
    dc_rated_current_1 = CurrentAtTemp()
    dc_rated_current_2 = CurrentAtTemp()
    dc_rated_current_3 = CurrentAtTemp()
    dc_rated_current_4 = CurrentAtTemp()
    dc_resistance = ResistanceAtTemp()

    def generate_description(self):
        description = "Ferrite bead"
        if self.impedance_1:
            description = description + ", " + str(self.impedance_1)
        if self.dc_rated_current_1:
            description = description + ", " + str(self.dc_rated_current_1)
        if self.dc_resistance:
            description = description + ", " + str(self.dc_resistance)
        return description
