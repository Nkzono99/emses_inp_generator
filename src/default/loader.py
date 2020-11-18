import os

import PySimpleGUI as sg
from utils import Plasmainp, UnitConversionKey, Units


class Loader:
    def __init__(self):
        self.applyers = {}  # lambda Plasmainp, Units: value
        self.exceptors = {}  # lambda Plasmainp, Units: bool

    def add_applyer(self, key, applyer, exceptor=None):
        self.applyers[key] = applyer

        if exceptor is None:
            def exceptor(inp, unit): return True
        self.exceptors[key] = exceptor

    def apply(self, inp, convkey, window):
        unit = Units(convkey.dx, convkey.to_c)
        for key, applyer in self.applyers.items():
            if not self.exceptors[key](inp, unit):
                continue
            try:
                value = applyer(inp, unit)
            except KeyError:
                continue
            window[key].Update(value=value)

    def load(self, filename, window):
        if filename is None or not os.path.exists(filename):
            return None

        convkey = UnitConversionKey.load(filename)
        if convkey is None:
            dx = sg.PopupGetText('このパラメータファイルに用いたグリッド幅[m]を入力してください')
            try:
                dx = float(dx)
            except:
                return None

            to_c = sg.PopupGetText('このパラメータファイルに用いたEMSES単位系での光速の値を入力してください')
            try:
                to_c = float(to_c)
            except:
                return None

            convkey = UnitConversionKey(dx, to_c)

        inp = Plasmainp(filename)
        self.apply(inp, convkey, window)

        window['basefile'].Update('Base file: {}'.format(filename))

        return inp


def create_default_loader(use_physical_dt=False):
    loader = Loader()

    loader.add_applyer('use_em', lambda i, u: i['emflag'] == 1)
    loader.add_applyer('use_pe', lambda i, u: i['nspec'] == 3)

    loader.add_applyer('dx', lambda i, u: u.dx)
    loader.add_applyer('em_c', lambda i, u: u.to_c)

    if use_physical_dt:
        loader.add_applyer('dt', lambda i, u: u.t.reverse(i['dt']))
    else:
        loader.add_applyer('dt', lambda i, u: i['dt'])

    loader.add_applyer('nx', lambda i, u: int(i['nx']))
    loader.add_applyer('ny', lambda i, u: int(i['ny']))
    loader.add_applyer('nz', lambda i, u: int(i['nz']))
    loader.add_applyer('nstep', lambda i, u: int(i['nstep']))

    loader.add_applyer('jobnum', lambda i, u: ' '.join(
        list(map(str, i['jobnum']))))
    loader.add_applyer('nodesx', lambda i, u: i['nodes'][0])
    loader.add_applyer('nodesy', lambda i, u: i['nodes'][1])
    loader.add_applyer('nodesz', lambda i, u: i['nodes'][2])

    return loader
