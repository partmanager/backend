def min_typ_max_to_str(min_value, typ, max_value, to_string):
    if min_value is not None and typ is not None and max_value is not None:
        if abs(typ - min_value) == abs(typ - max_value):
            return "{} ±{}".format(to_string(typ), to_string(abs(typ - min_value)))
        else:
            return "{} {}/{}".format(to_string(typ), to_string(min_value), to_string(max_value))
    elif min_value is None and max_value is None and typ is not None:
        return to_string(typ)
    elif typ is None and min_value is not None and max_value is not None:
        return "{} ~ {}".format(to_string(min_value), to_string(max_value))
    elif min_value is not None:
        return "min. {}".format(to_string(min_value))
    elif max_value is not None:
        return "max. {}".format(to_string(max_value))
    return ''
