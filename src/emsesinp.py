import re
from collections import OrderedDict

import f90nml

from units import Units


def create_empty_namelist():
    namelist = OrderedDict()
    namelist['real'] = {}
    namelist['realcv'] = {}
    namelist['esorem'] = {}
    namelist['jobcon'] = {}
    namelist['digcon'] = {}
    namelist['plasma'] = {}
    namelist['tmgrid'] = {}
    namelist['system'] = {}
    namelist['intp'] = {}
    namelist['inp'] = {}
    namelist['ptcond'] = {}
    namelist['scrnt'] = {}
    namelist['emissn'] = {}
    namelist['dipole'] = {}
    namelist['mpi'] = {}
    namelist['verbose'] = {}
    return namelist


class UnitConversionKey:
    def __init__(self, dx, to_c):
        self.dx = dx
        self.to_c = to_c

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            line = f.readline()

        if not line.startswith('!!'):
            return None

        text = line[6:].strip()
        pattern = r'dx=\[([+-]?\d+(?:\.\d+)?)\],to_c=\[([+-]?\d+(?:\.\d+)?)\]'
        m = re.match(pattern, text)
        dx = float(m.group(1))
        to_c = float(m.group(2))
        return UnitConversionKey(dx, to_c)

    @property
    def keytext(self):
        return 'dx=[{}],to_c=[{}]'.format(self.dx, self.to_c)


class Plasmainp:
    def __init__(self, filename=None):
        if filename is None:
            self.namelist = create_empty_namelist()
        else:
            self.namelist = f90nml.read(filename)

    def __getitem__(self, item):
        return self.namelist[item]

    def save(self, filename, convkey=None):
        with open(filename, 'wt', encoding='utf-8') as f:
            if convkey is not None:
                f.write('!!key {}\n'.format(convkey.keytext))
            f90nml.write(self.namelist, f, force=True)
