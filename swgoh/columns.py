import collections

class ColumnInfo:

    def __init__(self, name, internal, index):
        self.name = name
        self.internal = internal
        self.index = index


class Columns:
    ICOL = collections.OrderedDict()
    # Main Info
    ICOL.update({"Slot": ColumnInfo("Slot", "Slot", 1)})
    ICOL.update({"Set": ColumnInfo("Set", "Set", 2)})
    ICOL.update({"Pips": ColumnInfo("Pips", "Pips", 3)})
    ICOL.update({"Level": ColumnInfo("Level", "Level", 4)})
    ICOL.update({"Rating": ColumnInfo("Rating", "Rating", 5)})
    ICOL.update({"Character": ColumnInfo("Character", "Character", 6)})

    # Primary stats
    ICOL.update({"Primary Stat": ColumnInfo("Primary Stat", "Primary Stat", 7)})
    ICOL.update({"Primary Value": ColumnInfo("Primary Value", "Primary Value", 8)})

    # Secondary stats
    ICOL.update({"Critical Chance": ColumnInfo("Critical Chance %", "Critical Chance", 9)})
    ICOL.update({"Defense": ColumnInfo("Defense", "Defense", 10)})
    ICOL.update({"Defense %": ColumnInfo("Defense %", "Defense", 11)})

    ICOL.update({"Health": ColumnInfo("Health", "Health", 12)})
    ICOL.update({"Health %": ColumnInfo("Health %", "Health", 13)})
    ICOL.update({"Offense": ColumnInfo("Offense", "Offense", 14)})
    ICOL.update({"Offense %": ColumnInfo("Offense %", "Offense", 15)})
    ICOL.update({"Potency": ColumnInfo("Potency", "Potency", 16)})

    ICOL.update({"Protection": ColumnInfo("Protection", "Protection", 17)})
    ICOL.update({"Protection %": ColumnInfo("Protection %", "Protection %", 18)})
    ICOL.update({"Speed": ColumnInfo("Speed", "Speed", 19)})
    ICOL.update({"Tenacity": ColumnInfo("Tenacity %", "Tenacity", 20)})

    def __init__(self):
        self.columns = {}

    def add_primary(self, name, value):
        # Validate parms
        if name is None or value is None:
            return

        self.columns.update({name: Column(name, value)})

    def add_column(self, name, value):

        # Validate parms
        if name is None or value is None:
            return

        f_name, f_value, op = Columns.format_value(name, value)
        col = self.columns.get(f_name, None)
        if col is None:
            if op == "+":
                self.columns.update({f_name: Column(f_name, f_value)})
            elif op == "-":
                self.columns.update({f_name: Column(f_name, 0-f_value)})
        else:
            if op == "+":
                col.add(f_value)
            elif op == "-":
                col.subtract(f_value)
            self.columns.update({f_name: col})

    @staticmethod
    def format_value(name, value):

        try:
            val = value.split("+", 2)  # Check for + sign
        except:
            print("Error parsing secondary mod sign")

        op = ""
        if len(val) == 2:
            op = "+"
        else:
            val = value.split("-", 2)  # Check for - sign
            if len(val) == 2:
                op = "-"

        val = val[1].split("%", 2)

        # Percent column
        if len(val) == 2:
            return name + " %", float(val[0].strip(' "')), op

        # Integer column
        return name, int(val[0].strip(' "')), op

    def to_csv(self, line, pct):
        for icol in Columns.ICOL.values():
            col = self.columns.get(icol.name)
            if col is not None:
                if pct and col.name.find("%") != -1:
                    line.append(str(col.value) + "%")  # Use % symbol
                else:
                    line.append(col.value)  # Don't use % symbol
            else:
                line.append("")  # No value for column


class Column:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def add(self, addend):
        self.value += addend

    def subtract(self, subtrahend):
        self.value -= subtrahend

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

