"""
A class representing a CrouchingRancor ModData object
"""

from swgoh.mod_data import ModData


class ModDataSecondary(ModData):

    def __init__(self, mod_type, stat, value, rating=0):
        ModData.__init__(self, mod_type, stat, value)
        self.rating = rating

    def print_self(self):
        print("ModData - Type: %s Stat: %s Value: %s Rating: %s" %
              (self.mod_type, self.stat, self.value, self.rating))

    def toCsv(self, line):
        ModData.toCsv(self, line)
        line.append(self.rating)
