import os

import PySimpleGUI as sg

from emsesinp import Plasmainp, UnitConversionKey
from units import Units


def n0(inp, unit):
    wpe = unit.f.reverse(inp['plasma']['wp'][0])
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    e0 = unit.e0.from_unit
    return me * e0 * wpe * wpe / (qe * qe) * 1e-6


def Te(inp, unit):
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    path = unit.v.reverse(inp['intp']['path'][0])
    return me * path * path / qe


def Ti(inp, unit):
    qe = unit.qe.from_unit
    mi = unit.me.from_unit / inp['intp']['qm'][1]
    path = unit.v.reverse(inp['intp']['path'][1])
    return mi * path * path / qe


def Tp(inp, unit):
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    path = unit.v.reverse(inp['intp']['path'][2])
    return me * path * path / qe


def B(inp, unit):
    me = unit.me.from_unit
    qe = unit.qe.from_unit
    wc = unit.f.reverse(inp['plasma']['wc'])
    return me * wc / qe * 1e9


def apply_parameter(window, inp, convkey):
    unit = Units(convkey.dx, convkey.to_c)
    nx = int(inp['tmgrid']['nx'])
    ny = int(inp['tmgrid']['ny'])
    nz = int(inp['tmgrid']['nz'])

    window['use_em'].Update(value=(inp['esorem']['emflag'] == 1))
    window['use_pe'].Update(value=(inp['system']['nspec'] == 3))
    window['dx'].Update(value=convkey.dx)
    window['em_c'].Update(value=convkey.to_c)
    window['dt'].Update(value=unit.t.reverse(inp['tmgrid']['dt']))
    window['nx'].Update(value=nx)
    window['ny'].Update(value=ny)
    window['nz'].Update(value=nz)
    window['nstep'].Update(value=inp['jobcon']['nstep'])

    window['n0'].Update(value=n0(inp, unit))
    window['Te'].Update(value=Te(inp, unit))
    window['Ti'].Update(value=Ti(inp, unit))
    window['mi2me'].Update(value=1/inp['intp']['qm'][1])
    window['vdrie'].Update(value=unit.v.reverse(inp['intp']['vdri'][0]))
    window['vdrii'].Update(value=unit.v.reverse(inp['intp']['vdri'][1]))
    window['B'].Update(value=B(inp, unit))

    window['np_per_grid'].Update(value=int(inp['intp']['npin'][0]/(nx*ny*nz)))

    if inp['system']['nspec'] == 3:
        window['Jp'].Update(value=unit.J.reverse(
            inp['emissn']['curf'][-1]) * 1e6)
        window['Tp'].Update(value=Tp(inp, unit))
        window['dnsfp'].Update(value=inp['emissn']['dnsf'][-1])

    window['nfbndx{}'.format(inp['system']['nfbnd'][0])].Update(value=True)
    window['nfbndy{}'.format(inp['system']['nfbnd'][1])].Update(value=True)
    window['nfbndz{}'.format(inp['system']['nfbnd'][2])].Update(value=True)
    window['npbndx{}'.format(inp['system']['npbnd'][0])].Update(value=True)
    window['npbndy{}'.format(inp['system']['npbnd'][1])].Update(value=True)
    window['npbndz{}'.format(inp['system']['npbnd'][2])].Update(value=True)

    window['jobnum'].Update(value=' '.join(
        list(map(str, inp['jobcon']['jobnum']))))
    window['nodesx'].Update(value=inp['mpi']['nodes'][0])
    window['nodesy'].Update(value=inp['mpi']['nodes'][1])
    window['nodesz'].Update(value=inp['mpi']['nodes'][2])


def load(filename, window):
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
    apply_parameter(window, inp, convkey)
    return inp
