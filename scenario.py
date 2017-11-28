from collections import namedtuple
from utils import flatten

_Scenario = namedtuple('Scenario', ['id', 'refs', 'rfactor', 'chinu', 'rfactor_delta'])
_Ref = namedtuple('Reference', ['name', 'weight'])

def percentage(v):
    return round(v * 10000)/100

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
            map(str, self.refs),
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
