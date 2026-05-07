from ..part import Part
from ..fields.current import CurrentAtTemp
from ..fields.voltage import Voltage


class Triac(Part):
    V_gt = Voltage(verbose_name="Gate threshold voltage")
    I_GT = CurrentAtTemp(verbose_name="Gate trigger current")
    V_DRM = Voltage(verbose_name="Repetitive peak off-state forward voltage")
    V_RRM = Voltage(verbose_name="Repetitive peak off-state reverse voltage")

    def generate_description(self):
        description = f"Triac {self.I_GT.max} {self.V_gt.min}"
        return description
