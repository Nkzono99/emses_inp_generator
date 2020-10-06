"""シンプルなプラズマパラメータを管理する.

管理するパラメータ:
    &plasma
        wp(1:2)
        wc
    &intp
        qm(1:2)
        path(1:2)
        peth(1:2)
        vdri(1:2)

GUIのキー:
    n0 : Plasma density [/cc]
    Te : Electron temperature [eV]
    Ti : Ion temperature [eV]
    mi2me : Ion-to-electron mass ratio
    vdrie : Electron flow speed [m/s]
    vdrii : Ion flow speed [m/s]
    B : Magntic field [nT]
"""
import math

import PySimpleGUI as sg
from gui.basic_components import parameter

from additional.additional_parameter import AdditionalParameters


class SimplePlasmaParameters(AdditionalParameters):
    def create_tab(self):
        layout = [
            parameter('Plasma density [/cc]', 5000, key='n0'),
            parameter('Electron temperature [eV]', 1.0, key='Te'),
            parameter('Ion temperature [eV]', 0.5, key='Ti'),
            parameter('Ion-to-electron mass ratio', 1000, key='mi2me'),
            parameter('Electron flow speed [m/s]', 1000, key='vdrie'),
            parameter('Ion flow speed [m/s]', 1000, key='vdrii'),
            parameter('Magnetic field [nT]', 0, key='B')
        ]
        return sg.Tab('プラズマパラメータ', layout)

    def add_applyers(self, loader):
        loader.add_applyer('n0', _n0)
        loader.add_applyer('Te', _Te)
        loader.add_applyer('Ti', _Ti)
        loader.add_applyer('mi2me', lambda i, u: 1/i['qm'][1])
        loader.add_applyer('vdrie', lambda i, u: u.v.reverse(i['vdri'][0]))
        loader.add_applyer('vdrii', lambda i, u: u.v.reverse(i['vdri'][1]))
        loader.add_applyer('B', _B)

    def add_savers(self, saver):
        saver.add_saver(self._save_simple_plasma)

    def _save_simple_plasma(self, inp, values, unit):
        inp.setlist('plasma', 'wp', [wpe(values, unit), wpi(values, unit)])
        inp['plasma']['wc'] = wc(values, unit)

        inp.setlist('intp', 'qm', [-1.0, 1.0/float(values['mi2me'])])
        inp.setlist('intp', 'path', [pathe(values, unit), pathi(values, unit)])
        inp.setlist('intp', 'peth', [pathe(values, unit), pathi(values, unit)])
        inp.setlist('intp', 'vdri', [vdrie(values, unit), vdrii(values, unit)])


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


def wpe(values, unit):
    ne = float(values['n0']) * 1e6  # /cc to /m^3
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    e0 = unit.e0.from_unit
    wpe_phisic = math.sqrt(ne * qe * qe / me / e0)
    return unit.f.trans(wpe_phisic)


def wpi(values, unit):
    ni = float(values['n0']) * 1e6
    qe = unit.qe.from_unit
    mi = unit.me.from_unit * float(values['mi2me'])
    e0 = unit.e0.from_unit
    wpi_phisic = math.sqrt(ni * qe * qe / mi / e0)
    return unit.f.trans(wpi_phisic)


def wc(values, unit):
    B = float(values['B']) * 1e-9
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    wc_phisic = qe * B / me
    return unit.f.trans(wc_phisic)


def pathe(values, unit):
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    Te = float(values['Te'])
    pathe_phisic = math.sqrt(qe * Te / me)
    return unit.v.trans(pathe_phisic)


def pathi(values, unit):
    qe = unit.qe.from_unit
    mi = unit.me.from_unit * float(values['mi2me'])
    Ti = float(values['Ti'])
    pathi_phisic = math.sqrt(qe * Ti / mi)
    return unit.v.trans(pathi_phisic)


def vdrie(values, unit):
    return unit.v.trans(float(values['vdrie']))


def vdrii(values, unit):
    return unit.v.trans(float(values['vdrii']))
