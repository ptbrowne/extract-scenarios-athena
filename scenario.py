from collections import namedtuple
from utils import flatten
import csv

_Scenario = namedtuple('Scenario', ['id', 'refs', 'rfactor', 'chinu', 'rfactor_delta'])
_Ref = namedtuple('Reference', ['name', 'weight'])

def percentage(v):
    return round(v * 10000)/100

# Columns
RFACTOR = 0
CHINU = 1

class Ref(_Ref):
    def __str__(self):
        return '%s * %s%%' % (self.name, percentage(self.weight))

class Scenario(_Scenario):
    def as_line(self):
        """
        Ecrit un scenario comme une ligne
        Exemple :
        Scenario 8      Zn_Methionine_FAME_He * 10.23%  B_decembre_2016_030_001_tr.avg * 89.15% 0.0047853       0.0024418       0.138586288803
        """
        return '\t'.join(map(str, flatten([
            'Scenario %s' % self.id,
            list(map(str, self.refs)),
            self.rfactor,
            self.chinu,
            self.rfactor_delta
        ])))

    def as_block(self):
        """Ecrit un scenario comme un block
        Exemple :
        Scenario 8
        Zn_Methionine_FAME_He * 10.23%
        B_decembre_2016_030_001_tr.avg * 89.15%
        """
        return '\n'.join(map(str, [
            'Scenario %s' % self.id,  # Nom du scenario
            '\n'.join(map(str, self.refs)) # Chaque ref sur une ligne
        ]))

    @staticmethod
    def parse_cell(cell):
        """Transformer la valeur d'une cellule en nombre. 0 s'il n'y a rien"""
        try:
            return float(cell) if cell else 0
        except Exception:
            return cell

    @staticmethod
    def parse_row(line):
        """Transformer les valeurs d'une ligne en nombres"""
        return list(map(Scenario.parse_cell, line))

    @staticmethod
    def parse_scenario(line, headers, subheaders, ref_line):
        """Transformer une ligne en un scenario"""
        chinu = line[CHINU]
        rfactor = line[RFACTOR]
        rfactor_ref = ref_line[RFACTOR]
        rfactor_delta = (rfactor - rfactor_ref) / rfactor_ref * 100
        refs = [Ref(headers[i], cell) for i, cell in enumerate(line) if cell and subheaders[i] == 'weight']
        refs = sorted(refs, key=lambda ref: -ref.weight)
        return (refs, rfactor, chinu, rfactor_delta)

    @staticmethod
    def from_file(filename, limit=10):
        """Extraire d'un CSV les scenarios"""
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            reader = list(reader)
        headers = reader[0]
        subheaders = reader[1]
        results = reader[2:]
        results = list(map(Scenario.parse_row, results))
        scenarios = []
        ref_line = results[0]
        for i, line in enumerate(results[:limit]):
            line = [float(x) if x else 0 for x in line]
            results[i] = line
            chinu = line[CHINU]
            s = Scenario.parse_scenario(line, headers, subheaders, ref_line)
            scenario_id = i + 1
            scenario = Scenario(*([scenario_id] + list(s)))
            scenarios.append(scenario)
        return scenarios
