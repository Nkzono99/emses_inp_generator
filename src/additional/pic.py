"""PICのパラメータを管理する.

管理するパラメータ:
    &intp
        npin(1:2)

GUIのキー:
    np_per_grid: Number of super particles per grid
"""
import PySimpleGUI as sg
from gui.basic_components import parameter, radio_box


def add_pic_parameter(window_creator, loader, saver):
    window_creator.add_tab_creator(create_pic_tab)

    add_applyer(loader)

    saver.add_saver(save_pic)


def create_pic_tab():
    layout = [
        parameter('Number of super particles per grid', 40, key='np_per_grid')
    ]
    return sg.Tab('PICパラメータ', layout)


def add_applyer(loader):
    loader.add_applyer('np_per_grid', _np_per_grid)


def _np_per_grid(inp, unit):
    nx = inp['nx']
    ny = inp['ny']
    nz = inp['nz']
    return int(inp['npin'][0] / (nx * ny * nz))


def save_pic(inp, values, unit):
    nx = int(values['nx'])
    ny = int(values['ny'])
    nz = int(values['nz'])

    inp.setlist('intp', 'npin', [
                int(values['np_per_grid']) * nx * ny * nz] * 2)
