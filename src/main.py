from gui import create_window
import PySimpleGUI as sg
from emsesinp import Plasmainp, UnitConversionKey
import os
from savedata import save
from apply_parameter_on_gui import load
from units import Units
import math


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
    window = create_window()
    window.finalize()

    inp = load(default_inp_path, window)
    if inp is None:
        inp = Plasmainp()

    while True:
        event, values = window.read()

        if event is None:
            break

        if event == 'Save':
            filename = sg.popup_get_file('保存するファイル名を指定してください',
                                         default_path='plasma.inp',
                                         default_extension='inp')
            if filename is None:
                continue
            save(inp, filename, values)

        if event == 'Load':
            filename = sg.popup_get_file('読み込むファイル名を指定してください',
                                         default_path='plasma.inp',
                                         default_extension='inp')
            res = load(filename, window)
            if res is not None:
                inp = res

        if event == 'Apply Template':
            if len(values['template_file']) == 0:
                continue
            filename = values['template_file'][0]
            res = load(filename, window)
            if res is not None:
                inp = res

        if event == 'Save Template':
            filename = sg.popup_get_file('保存するファイル名を指定してください',
                                         default_path='template.inp',
                                         default_extension='inp',
                                         initial_folder='template')
            if filename is None:
                continue
            save(inp, os.path.join('template', filename), values)

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
