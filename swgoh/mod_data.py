"""
A class representing a CrouchingRancor ModData object
"""


class ModData:

    def __init__(self, mod_type, stat, value):
        self.mod_type = mod_type
        self.stat = stat
        self.value = value

    def print_self(self):
        print("ModData - Type: %s Stat: %s Value: %s" % (self.mod_type, self.stat, self.value))

    def to_csv(self, line):
        line.append(self.mod_type)
        line.append(self.stat)
        line.append(self.value)


