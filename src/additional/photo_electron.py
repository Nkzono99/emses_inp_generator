"""光電子のパラメータを管理する.

管理するパラメータ:
    &plasma
        wp(3)
    &intp
        qm(3)
        path(3)
        peth(3)
        npin(3)
        np(3)
    &emissn
        nflag_emit(3)
        curf(3)
        dnsf(3)

GUIのキー:
    Jp : PE current density [microA/m^2]
    Tp : PE temprature [eV]
    dnsfp : Number of superparticles per photoelectron
"""
import math

import PySimpleGUI as sg
from gui import parameter

from additional import AdditionalParameters


class PhotoParameters(AdditionalParameters):
    @classmethod
    def is_active(cls, config):
        return config['Control'].getboolean('ControlPhotoelectronParameter')

    def create_tab(self):
        layout = [
            parameter('PE current density [microA/m^2]', 0, key='Jp'),
            parameter('PE temprature [eV]', 1.0, key='Tp'),
            parameter('Number of superparticles per PE', 40, key='dnsfp')
        ]
        return sg.Tab('光電子パラメータ', layout)

    def add_applyers(self, loader):
        def use_pe(i, u): return i['nspec'] == 3
        loader.add_applyer('Jp', _curf_load, exceptor=use_pe)
        loader.add_applyer('Tp', _Tp, exceptor=use_pe)
        loader.add_applyer('dnsfp', lambda i,
                           u: i['dnsf'][-1], exceptor=use_pe)

    def add_savers(self, saver):
        saver.add_saver(self._save_photo, exceptor=lambda i, v, u: v['use_pe'])
        saver.add_saver(self._remove_photo, exceptor=lambda i,
                        v, u: not v['use_pe'])

    def _save_photo(self, inp, values, unit):
        nx = int(values['nx'])
        ny = int(values['ny'])
        nz = int(values['nz'])

        inp.setlist('plasma', 'wp', _wpe(values, unit), start_index=3)

        inp.setlist('intp', 'qm', -1.0, start_index=3)
        inp.setlist('intp', 'path', _pathp(values, unit), start_index=3)
        inp.setlist('intp', 'peth', _pathp(values, unit), start_index=3)
        inp.setlist('intp', 'npin', 0, start_index=3)
        inp.setlist('intp', 'np', int(
            values['np_per_grid']) * nx * ny * nz, start_index=3)

        inp.setlist('emissn', 'curf', _curf_save(values, unit), start_index=3)
        inp.setlist('emissn', 'nflag_emit', 2, start_index=3)
        inp.setlist('emissn', 'dnsf', int(values['dnsfp']), start_index=3)

    def _remove_photo(self, inp, values, unit):
        inp.remove('nflag_emit', index=3)
        inp.remove('wp', index=3)
        inp.remove('path', index=3)
        inp.remove('peth', index=3)
        inp.remove('npin', index=3)
        inp.remove('np', index=3)
        inp.remove('curf', index=3)
        inp.remove('dnsf', index=3)


def _curf_load(inp, unit):
    return unit.J.reverse(inp['curf'][-1]) * 1e6


def _Tp(inp, unit):
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    path = unit.v.reverse(inp['intp']['path'][2])
    return me * path * path / qe


def _wpe(values, unit):
    ne = float(values['n0']) * 1e6  # /cc to /m^3
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    e0 = unit.e0.from_unit
    wpe_phisic = math.sqrt(ne * qe * qe / me / e0)
    return unit.f.trans(wpe_phisic)


def _pathp(values, unit):
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    Tp = float(values['Tp'])
    pathp_phisic = math.sqrt(qe * Tp / me)
    return unit.v.trans(pathp_phisic)


def _curf_save(values, unit):
    return unit.J.trans(float(values['Jp']) * 1e-6)
