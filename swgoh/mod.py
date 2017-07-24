"""
A class representing a CrouchingRancor modAsset
"""

from swgoh.mod_data import ModData
from swgoh.mod_data_secondary import ModDataSecondary
from selenium.common.exceptions import NoSuchElementException


class Mod:

    def __init__(self, mod):
        self.mod = mod
        self.pips = 0
        self.level = None
        self.rating = None
        self.character = None
        self.mod_data_list = []

    def build_mod(self):
        self.set_pips()
        self.set_level()
        self.build_mod_data_list()
        self.set_rating()
        self.set_character()

    def set_pips(self):
        pips_parent = self.get_element("pips")
        if pips_parent is None:
            self.pips = 0
        else:
            self.pips = len(pips_parent.find_elements_by_class_name("pip"))

    def set_level(self):
        level_elm = self.get_element("modLevel")
        if level_elm is None:
            self.level = 0
        else:
            self.level = level_elm.text.strip()

    def set_rating(self):
        rating = self.get_element("modRating")
        if rating is None:
            self.rating = 0
        else:
            self.rating = rating.text.strip()

    def set_character(self):
        character = self.get_element("modCharacter")
        if character is None:
            self.character = ""
        else:
            self.character = character.text.strip()

    def build_mod_data_list(self):
        mod_data = self.get_element("modData")
        if mod_data is None:
            return

        # Build the primary mod data
        try:
            primary_elm = mod_data.find_element_by_class_name("modPrimary")
        except NoSuchElementException:
            return

        primary_mod = Mod.build_mod_primary(primary_elm, "primary")
        self.mod_data_list.append(primary_mod)

        # Build all the secondary mod data
        try:
            secondary_list = mod_data.find_elements_by_class_name("modSecondary")
        except NoSuchElementException:
            return

        for secondary in secondary_list:
            sec_mod = Mod.build_mod_secondary(secondary, "secondary")
            self.mod_data_list.append(sec_mod)

    def get_element(self, name):
        try:
            return self.mod.find_element_by_class_name(name)
        except NoSuchElementException:
            return None

    def get_elements(self, name):
        try:
            return self.mod.find_elements_by_class_name(name)
        except NoSuchElementException:
            return None

    def print_self(self):
        print ("Mod - Pips: %i Level: %s Rating: %s Character: %s"
               % (self.pips, self.level, self.rating, self.character))
        for mod_data in self.mod_data_list:
            mod_data.print_self()

    def toCsv(self, line):
        line.append(self.pips)
        line.append(self.level)
        line.append(self.rating)
        line.append(self.character)
        for mod_data in self.mod_data_list:
            mod_data.toCsv(line)

    @staticmethod
    def build_mod_primary(data, mod_type):
        # Parse out stat and value
        value, stat = Mod.parse_mod_value(data.text)
        return ModData(mod_type, stat, value)

    @staticmethod
    def build_mod_secondary(data, mod_type):
        # Parse out stat and value
        value, stat, rating = Mod.parse_secondary_mod_value(data.text)
        return ModDataSecondary(mod_type, stat, value, rating)

    @staticmethod
    def parse_mod_value(value):
        values = value.split()
        count = len(values)
        if count == 3:
            return values[0], values[1]+" "+values[2]
        elif count == 2:
            return values[0], values[1]
        else:
            return None, None

    @staticmethod
    def parse_secondary_mod_value(value):
        values = value.split()
        count = len(values)
        if count == 4:
            return values[0], values[1]+" "+values[2], values[3]
        elif count == 3:
            try:
                int(values[2])
                return values[0], values[1], values[2]
            except ValueError:
                return values[0], values[1]+" "+values[2], None
        elif count == 2:
            return values[0], values[1], None
        else:
            return None, None, None










