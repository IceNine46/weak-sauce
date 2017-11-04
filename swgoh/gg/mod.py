"""
A class representing a CrouchingRancor modAsset
"""
from swgoh.gg.columns import Columns
from swgoh.gg.mod_data import ModData
from swgoh.gg.mod_data_secondary import ModDataSecondary
from selenium.common.exceptions import NoSuchElementException


class Mod:

    def __init__(self, mod):
        self.mod = mod
        self.pips = 0
        self.slot = None
        self.mod_set = None
        self.level = None
        self.character = None
        self.mod_data_list = []
        self.columns = Columns()

    def build_mod(self):
        self.set_slot_and_set()
        self.set_pips()
        self.set_level()
        self.build_mod_data_list()
        self.set_character()

    def set_slot_and_set(self):
        image = self.get_element("statmod-img")
        if image is None:
            self.slot = None
            self.mod_set = None
        else:
            image_text = image.get_attribute("alt")
            slot, mod_set = Mod.parse_slot_and_set(image_text)
            self.slot = slot
            self.mod_set = mod_set

    def set_pips(self):
        pips_parent = self.get_element("statmod-pips")
        if pips_parent is None:
            self.pips = 0
        else:
            self.pips = len(pips_parent.find_elements_by_class_name("statmod-pip"))

    def set_level(self):
        level_elm = self.get_element("statmod-level")
        if level_elm is None:
            self.level = 0
        else:
            self.level = level_elm.text.strip()

    def set_character(self):
        character = self.get_element("char-portrait-img")
        if character is None:
            self.character = ""
        else:
            self.character = character.get_attribute("alt")

    def build_mod_data_list(self):
        mod_data = self.get_element("statmod-details")
        if mod_data is None:
            return

        # Locate the primary and seconds stats blocks
        try:
            stat_elm = mod_data.find_element_by_class_name("statmod-stats-1")
            primary_elm = stat_elm.find_element_by_class_name("statmod-stat")
        except NoSuchElementException:
            return

        # Build the primary mod data
        primary_mod = Mod.build_mod_primary(primary_elm, "primary")
        self.mod_data_list.append(primary_mod)

        # Build all the secondary mod data
        try:
            secondary = mod_data.find_element_by_class_name("statmod-stats-2")
            secondary_list = secondary.find_elements_by_class_name("statmod-stat")
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
        print ("Mod - Pips: %i Level: %s Character: %s"
               % (self.pips, self.level, self.character))
        for mod_data in self.mod_data_list:
            mod_data.print_self()

    def to_csv(self, line):
        line.append(self.slot)
        line.append(self.mod_set)
        line.append(self.pips)
        line.append(self.level)
        line.append(self.character)
        for mod_data in self.mod_data_list:
            mod_data.to_csv(line)

    def to_csv_sec_agg(self, line, pct):
        self.columns.add_primary("Slot", self.slot)
        self.columns.add_primary("Set", self.mod_set)
        self.columns.add_primary("Pips", self.pips)
        self.columns.add_primary("Level", self.level)
        self.columns.add_primary("Character", self.character)

        for mod_data in self.mod_data_list:
            if mod_data.mod_type == "primary":
                self.columns.add_primary("Primary Stat", mod_data.stat)
                self.columns.add_primary("Primary Value", mod_data.value)
            elif mod_data.mod_type == "secondary":
                self.columns.add_column(mod_data.stat, mod_data.value)

        self.columns.to_csv(line, pct)

    @staticmethod
    def build_mod_primary(primary_elm, mod_type):
        # Set Primary stat and value
        value = primary_elm.find_element_by_class_name("statmod-stat-value").text.strip().split("+")[1]
        stat = primary_elm.find_element_by_class_name("statmod-stat-label").text.strip()
        return ModData(mod_type, stat, value)

    @staticmethod
    def build_mod_secondary(data, mod_type):
        # Set secondary stat and value
        value = data.find_element_by_class_name("statmod-stat-value").text
        stat = data.find_element_by_class_name("statmod-stat-label").text
        return ModDataSecondary(mod_type, stat, value)

    @staticmethod
    def parse_slot_and_set(value):
        mod_slot = "Unknown"
        mod_set = "Unknown"

        values = value.split(" ")
        if len(values) == 4:
            mod_set = values[2]
            mod_slot = Mod.get_mod_slot(values[3].strip())
        elif len(values) == 5:
            mod_set = values[2]+" "+values[3]
            mod_slot = Mod.get_mod_slot(values[4].strip())

        return mod_slot, mod_set

    @staticmethod
    def get_mod_slot(mod_type):
        if mod_type == 'Transmitter':
            return 'Square'
        elif mod_type == 'Receiver':
            return 'Arrow'
        elif mod_type == 'Processor':
            return 'Diamond'
        elif mod_type == 'Holo-Array':
            return 'Triangle'
        elif mod_type == 'Data-Bus':
            return 'Circle'
        elif mod_type == 'Multiplexer':
            return 'Cross'









