"""境界条件のパラメータを管理する.

管理するパラメータ:
    &system
        nfbnd(1:3)
        npbnd(1:3, nspec)

GUIのキー:
    nfbndx[0-1] : Field Boundary X
    nfbndy[0-1] : Field Boundary Y
    nfbndz[0-1] : Field Boundary Z
    npbndx[0-2] : Particles Boundary X
    npbndx[0-2] : Particles Boundary Y
    npbndx[0-2] : Particles Boundary Z
"""
import PySimpleGUI as sg
from gui import radio_box, selectIndex

from additional import AdditionalParameters


class BoundaryParameters(AdditionalParameters):
    @classmethod
    def is_active(cls, config):
        return config['Control'].getboolean('ControlBoundaryParameter')

    def create_tab(self):
        layout = [
            radio_box('Field Boundary X', 'periodic',
                      'free', group_id='nfbndx'),
            radio_box('Field Boundary Y', 'periodic',
                      'free', group_id='nfbndy'),
            radio_box('Field Boundary Z', 'periodic',
                      'free', group_id='nfbndz'),
            radio_box('Particles Boundary X', 'periodic',
                      'Dirichlet', 'Neumann', group_id='npbndx'),
            radio_box('Particles Boundary Y', 'periodic',
                      'Dirichlet', 'Neumann', group_id='npbndy'),
            radio_box('Particles Boundary Z', 'periodic',
                      'Dirichlet', 'Neumann', group_id='npbndz'),
        ]
        return sg.Tab('境界条件', layout)

    def add_applyers(self, loader):
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

    def add_savers(self, saver):
        saver.add_saver(self._save_boundary)

    def _save_boundary(self, inp, values, unit):
        nspec = 3 if values['use_pe'] else 2
        inp.setlist('system', 'nfbnd', [selectIndex(values, 'nfbndx'),
                                        selectIndex(values, 'nfbndy'),
                                        selectIndex(values, 'nfbndz')])
        inp['system']['npbnd'] = [selectIndex(values, 'npbndx'),
                                  selectIndex(values, 'npbndy'),
                                  selectIndex(values, 'npbndz')] * nspec
