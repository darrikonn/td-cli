CSI = "\033["


def code_to_chars(code):
    return CSI + str(code) + "m"


class AnsiCodes(object):
    def __init__(self):
        for name in dir(self):
            if not name.startswith("_"):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))
