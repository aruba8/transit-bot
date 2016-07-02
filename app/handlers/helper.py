import re


def validate_stop_number(stop_number):
    r = re.compile("^[0-9]{5}$")
    if r.match(str(stop_number)) is None:
        return False
    else:
        return True
