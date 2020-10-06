"""PICのパラメータを管理する.

管理するパラメータ:
    &intp
        npin(1:2)

GUIのキー:
    np_per_grid: Number of super particles per grid
"""
import PySimpleGUI as sg
from gui.basic_components import parameter, radio_box
from additional.additional_parameter import AdditionalParameters

class PICParameters(AdditionalParameters):
    def create_tab(self):
        layout = [
            parameter('Number of super particles per grid', 40, key='np_per_grid')
        ]
        return sg.Tab('PICパラメータ', layout)
    
    def add_applyers(self, loader):
        loader.add_applyer('np_per_grid', _np_per_grid)
    
    def add_savers(self, saver):
        saver.add_saver(self._save_pic)

    def _save_pic(self, inp, values, unit):
        nx = int(values['nx'])
        ny = int(values['ny'])
        nz = int(values['nz'])
        np = int(values['np_per_grid']) * nx * ny * nz

        inp.setlist('intp', 'npin', [np] * 2)


def _np_per_grid(inp, unit):
    nx = inp['nx']
    ny = inp['ny']
    nz = inp['nz']
    return int(inp['npin'][0] / (nx * ny * nz))
