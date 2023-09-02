from partcatalog.models.fields.return_loss import ReturnLoss
from .field_decoder_common import parameter_str_to_dict
from .value_decoder import dB_decode as __dB_decode


def return_loss_decoder(json_data):
    value = parameter_str_to_dict(json_data['value'], __dB_decode)
    if value:
        return_loss = ReturnLoss()
        return_loss.min = value['min']
        return_loss.typ = value['typ']
        return_loss.max = value['max']
        return return_loss
