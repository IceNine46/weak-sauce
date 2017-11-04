"""
A class representing a CrouchingRancor ModData object
"""


class ModData:

    TYPE = "Primary"

    def __init__(self, mod_type, stat, value):
        self.mod_type = mod_type
        self.stat = stat
        self.value = value

    def print_self(self):
        print("ModData - Type: %s Stat: %s Value: %s" % (self.mod_type, self.stat, self.value))

    def to_csv(self, line):
        line.append(self.stat)
        line.append(self.value)

    def to_sec_agg_csv(self, line):
        line.append(self.stat)
        line.append(self.value)


