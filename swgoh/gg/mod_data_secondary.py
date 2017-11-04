"""
A class representing a CrouchingRancor ModData object
"""

from swgoh.gg.mod_data import ModData


class ModDataSecondary(ModData):

    TYPE = "Secondary"

    def __init__(self, mod_type, stat, value):
        ModData.__init__(self, mod_type, stat, value)

    def print_self(self):
        print("ModData - Type: %s Stat: %s Value: %s" %
              (self.mod_type, self.stat, self.value))

    def to_csv(self, line):
        ModData.to_csv(self, line)

    def to_sec_agg_csv(self, line):
        ModData.to_sec_agg_csv(self, line)
