import math
import os

import PySimpleGUI as sg

from loader import create_default_loader
from emsesinp import Plasmainp, UnitConversionKey
from gui.gui import WindowCreator
from savedata import create_default_saver
from units import Units

default_inp_path = 'template/default.inp'


def debye(values):
    unit = Units()
    qe = unit.qe.from_unit
    e0 = unit.e0.from_unit
    n0 = float(values['n0']) * 1e6
    Te = float(values['Te'])
    return math.sqrt(e0 * qe * Te / (n0 * qe * qe))


def egyro(values):
    unit = Units()
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    Te = float(values['Te'])
    B = float(values['B']) * 1e-9
    if B == 0:
        return -1
    return math.sqrt(me * qe * Te) / (qe * B)


def igyro(values):
    unit = Units()
    qe = unit.qe.from_unit
    mi = unit.me.from_unit * float(values['mi2me'])
    Ti = float(values['Ti'])
    B = float(values['B']) * 1e-9
    if B == 0:
        return -1
    return math.sqrt(mi * qe * Ti) / (qe * B)


def main():
    wc = WindowCreator()

    window = wc.create_window()
    window.finalize()

    loader = create_default_loader(window)
    saver = create_default_saver()

    inp = loader.load(default_inp_path)
    if inp is None:
        inp = Plasmainp()

    while True:
        event, values = window.read()

        if event is None:
            break

        if event == 'Save':
            filename = sg.popup_get_file('保存するファイル名を指定してください',
                                         save_as=True,
                                         default_path='plasma.inp',
                                         default_extension='inp',
                                         no_window=True,
                                         file_types=(('Input Files', '.inp'), ('ALL Files', '*')))
            if filename is None or len(filename) == 0:
                continue
            saver.save(filename, inp, values)

        if event == 'Load':
            filename = sg.popup_get_file('読み込むファイル名を指定してください',
                                         default_path='plasma.inp',
                                         default_extension='inp',
                                         no_window=True,
                                         file_types=(('Input Files', '.inp'), ('ALL Files', '*')))
            if filename is None or len(filename) == 0:
                continue
            res = loader.load(filename)
            if res is not None:
                inp = res

        if event == 'Apply Template':
            if len(values['template_file']) == 0:
                continue
            filename = values['template_file'][0]
            res = loader.load(filename)
            if res is not None:
                inp = res

        if event == 'Save Template':
            filename = sg.popup_get_file('保存するファイル名を指定してください',
                                         save_as=True,
                                         default_path='template.inp',
                                         default_extension='inp',
                                         initial_folder='template',
                                         no_window=True,
                                         file_types=(('Input Files', '.inp'), ('ALL Files', '*')))
            if filename is None or len(filename) == 0:
                continue
            if not os.path.exists(filename):
                continue
            saver.save(filename, inp, values)

        if event == 'Check':
            window['debye'].Update(value=debye(values))
            window['egyro'].Update(value=egyro(values))
            window['igyro'].Update(value=igyro(values))

        if event == 'Restart Window':
            res = sg.popup_ok_cancel('Can I just restart this window?')
            if res == 'OK':
                window.close()
                main()
                return
    window.close()


if __name__ == '__main__':
    main()
