from .part import Part
from .fields.power import Power
from .fields.resistance import Resistance, ResistanceAtTemp
from .fields.max_current import MaxCurrentAtTemp
from .fields.time_at_current import TimeAtCurrent
from .fields.max_voltage import MaxVoltageAtTemp


class PTCFuse(Part):
    part_type_subset = ['PFU']
    hold_current = MaxCurrentAtTemp()  # I_H
    trip_current = MaxCurrentAtTemp()  # I_T
    rated_voltage = MaxVoltageAtTemp()  # V_MAX
    fault_current = MaxCurrentAtTemp()  # I_MAX
    tripped_power_dissipation = Power(verbose_name="Pd, maximum power dissipation at tripped state.")  # Pd, maximum power dissipation at tripped state
    time_to_trip = TimeAtCurrent()  #
    resistance = ResistanceAtTemp()  # resistance when not tripped
    tripped_resistance = Resistance()  # resistance at tripped state

    def generate_description(self):
        description = "PTC Fuse"
        if self.hold_current:
            description = description + ", Ih=" + str(self.hold_current)
        if self.rated_voltage:
            description = description + ", " + str(self.rated_voltage)
        return description

