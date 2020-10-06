import math

from emsesinp import UnitConversionKey
from units import Units


class Saver:
    def __init__(self):
        self.savers = []
        self.exceptors = []
    
    def add_saver(self, saver, exceptor=None):
        if exceptor is None:
            exceptor = lambda inp, values, unit: True

        self.savers.append(saver)
        self.exceptors.append(exceptor)
    
    def save(self, filename, inp, values):
        dx = float(values['dx'])
        to_c = float(values['em_c'])

        unit = Units(dx=dx, to_c=to_c)
        convkey = UnitConversionKey(dx=dx, to_c=to_c)

        for saver, exceptor in zip(self.savers, self.exceptors):
            if exceptor(inp, values, unit):
                saver(inp, values, unit)
        inp.save(filename, convkey=convkey)


def create_default_saver():
    saver = Saver()

    saver.add_saver(save_esorem)
    saver.add_saver(save_job_con)
    saver.add_saver(save_plasma)
    saver.add_saver(save_tmgrid)
    saver.add_saver(save_system)
    saver.add_saver(save_mpi)

    return saver


def save_esorem(inp, values, unit):
    inp['esorem']['emflag'] = 1 if values['use_em'] else 0


def save_job_con(inp, values, unit):
    inp['jobcon']['jobnum'] = list(map(int, values['jobnum'].split(' ')))
    inp['jobcon']['nstep'] = int(values['nstep'])


def save_plasma(inp, values, unit):
    inp['plasma']['cv'] = float(values['em_c'])


def save_tmgrid(inp, values, unit):
    inp['tmgrid']['dt'] = unit.t.trans(float(values['dt']))
    inp['tmgrid']['nx'] = int(values['nx'])
    inp['tmgrid']['ny'] = int(values['ny'])
    inp['tmgrid']['nz'] = int(values['nz'])


def save_system(inp, values, unit):
    nspec = 3 if values['use_pe'] else 2
    inp['system']['nspec'] = nspec


def save_mpi(inp, values, unit):
    inp['mpi']['nodes'] = [int(values['nodesx']),
                           int(values['nodesy']),
                           int(values['nodesz'])]


def selectIndex(values, name):
    for key, value in values.items():
        if key.startswith(name) and value == True:
            return int(key.replace(name, ''))
    return None
