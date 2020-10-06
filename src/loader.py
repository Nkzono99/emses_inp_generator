import os

import PySimpleGUI as sg

from emsesinp import Plasmainp, UnitConversionKey
from units import Units


class Loader:
    def __init__(self):
        self.applyers = {}  # lambda Plasmainp, Units: value
        self.exceptors = {}  # lambda Plasmainp, Units: bool
    
    def add_applyer(self, key, applyer, exceptor=None):
        self.applyers[key] = applyer

        if exceptor is None:
            exceptor = lambda inp, unit: True
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
        return inp


def create_default_loader():
    loader = Loader()

    loader.add_applyer('use_em', lambda i, u: i['emflag'] == 1)
    loader.add_applyer('use_pe', lambda i, u: i['nspec'] == 3)
    
    loader.add_applyer('dx', lambda i, u: u.dx)
    loader.add_applyer('em_c', lambda i, u: u.to_c)

    loader.add_applyer('dt', lambda i, u: u.t.reverse(i['dt']))
    loader.add_applyer('nx', lambda i, u: int(i['nx']))
    loader.add_applyer('ny', lambda i, u: int(i['ny']))
    loader.add_applyer('nz', lambda i, u: int(i['nz']))
    loader.add_applyer('nstep', lambda i, u: int(i['nstep']))

    loader.add_applyer('n0', _n0)
    loader.add_applyer('Te', _Te)
    loader.add_applyer('Ti', _Ti)
    loader.add_applyer('mi2me', lambda i, u: 1/i['qm'][1])
    loader.add_applyer('vdrie', lambda i, u: u.v.reverse(i['vdri'][0]))
    loader.add_applyer('vdrii', lambda i, u: u.v.reverse(i['vdri'][1]))
    loader.add_applyer('B', _B)

    loader.add_applyer('nfbndx0', lambda i, u: i['nfbnd'][0] == 0)
    loader.add_applyer('nfbndx1', lambda i, u: i['nfbnd'][0] == 1)
    loader.add_applyer('nfbndy0', lambda i, u: i['nfbnd'][1] == 0)
    loader.add_applyer('nfbndy1', lambda i, u: i['nfbnd'][1] == 1)
    loader.add_applyer('nfbndz0', lambda i, u: i['nfbnd'][2] == 0)
    loader.add_applyer('nfbndz1', lambda i, u: i['nfbnd'][2] == 1)

    loader.add_applyer('npbndx0', lambda i, u: i['npbnd'][0] == 0)
    loader.add_applyer('npbndx1', lambda i, u: i['npbnd'][0] == 1)
    loader.add_applyer('npbndx2', lambda i, u: i['npbnd'][0] == 2)
    loader.add_applyer('npbndy0', lambda i, u: i['npbnd'][1] == 0)
    loader.add_applyer('npbndy1', lambda i, u: i['npbnd'][1] == 1)
    loader.add_applyer('npbndy2', lambda i, u: i['npbnd'][1] == 2)
    loader.add_applyer('npbndz0', lambda i, u: i['npbnd'][2] == 0)
    loader.add_applyer('npbndz1', lambda i, u: i['npbnd'][2] == 1)
    loader.add_applyer('npbndz2', lambda i, u: i['npbnd'][2] == 2)

    loader.add_applyer('jobnum', lambda i, u: ' '.join(list(map(str, i['jobnum']))))
    loader.add_applyer('nodesx', lambda i, u: i['nodes'][0])
    loader.add_applyer('nodesy', lambda i, u: i['nodes'][1])
    loader.add_applyer('nodesz', lambda i, u: i['nodes'][2])

    return loader


def _n0(inp, unit):
    wpe = unit.f.reverse(inp['plasma']['wp'][0])
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    e0 = unit.e0.from_unit
    return me * e0 * wpe * wpe / (qe * qe) * 1e-6


def _Te(inp, unit):
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    path = unit.v.reverse(inp['intp']['path'][0])
    return me * path * path / qe


def _Ti(inp, unit):
    qe = unit.qe.from_unit
    mi = unit.me.from_unit / inp['intp']['qm'][1]
    path = unit.v.reverse(inp['intp']['path'][1])
    return mi * path * path / qe


def _B(inp, unit):
    me = unit.me.from_unit
    qe = unit.qe.from_unit
    wc = unit.f.reverse(inp['plasma']['wc'])
    return me * wc / qe * 1e9
