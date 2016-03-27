import re


def validate_stop_number(stopnumber):
    r = re.compile('^[0-9]{5}$')
    if r.match(str(stopnumber)) is None:
        return False
    else:
        return True
