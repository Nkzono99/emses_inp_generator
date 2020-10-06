import glob
import os

import PySimpleGUI as sg

name_size = (30, 1)
value_size = (20, 1)


def basis_parameter(name, default, em_default, key, fix_unit=False, fix_em_unit=False):
    name_text = sg.Text(name, size=name_size)
    if fix_unit:
        physical_unit = sg.Text(str(default), size=value_size, key=key)
    else:
        physical_unit = sg.InputText(str(default), size=value_size, key=key)
    if fix_em_unit:
        emses_unit = sg.Text(str(em_default), size=value_size,
                             key='em_{}'.format(key))
    else:
        emses_unit = sg.InputText(str(em_default), size=value_size,
                                  key='em_{}'.format(key))
    return [name_text, physical_unit, sg.Text('=>'), emses_unit]


def parameter(name, default, key, fix_unit=False):
    name_text = sg.Text(name, size=name_size)
    if fix_unit:
        physical_unit = sg.Text(str(default), size=value_size, key=key)
    else:
        physical_unit = sg.InputText(str(default), size=value_size, key=key)
    return [name_text, physical_unit]


def radio_box(name, *selections, group_id, default_index=0):
    name_text = sg.Text(name, size=name_size)
    radios = [sg.Radio(selection,
                       group_id=group_id,
                       default=(i == default_index),
                       key='{}{}'.format(group_id, i))
              for i, selection in enumerate(selections)]
    box = [name_text]
    for radio in radios:
        box.append(radio)
    return box


def create_basis_frame():
    layout = [
        basis_parameter('Grid width [m]', 1.0, 1.0,
                        key='dx', fix_em_unit=True),
        basis_parameter('Light speed [m/s]', 2.997925e8,
                        10000, key='c', fix_unit=True),
        basis_parameter('Electron charge-to-mass ratio',
                        -1.758820e11, -1.0, key='qe/me', fix_unit=True, fix_em_unit=True),
        basis_parameter(
            'FS-Permittivity [Fm^−1]', 8.854188e-12, 1.0, key='e0', fix_unit=True, fix_em_unit=True)
    ]
    return sg.Frame('基準パラメータ', layout)


def create_simulation_frame():
    layout = [
        parameter('dt [s]', 0.01, key='dt'),
        parameter('nx', 64, key='nx'),
        parameter('ny', 64, key='ny'),
        parameter('nz', 512, key='nz'),
        parameter('nstep', 100000, key='nstep')
    ]
    return sg.Frame('シミュレーションパラメータ', layout)


def create_extra_frame():
    layout = [
        parameter('jobnum', '0 1', key='jobnum'),
        parameter('nodes x', 4, key='nodesx'),
        parameter('nodes y', 2, key='nodesy'),
        parameter('nodes z', 32, key='nodesz')
    ]
    return sg.Frame('その他設定', layout)


def create_check_frame():
    layout = [
        parameter('Debye Length [m]', 0, key='debye', fix_unit=True),
        parameter('Electron gyro radius [m]', 0, key='egyro', fix_unit=True),
        parameter('Ion gyro radius [m]', 0, key='igyro', fix_unit=True)
    ]
    return sg.Frame('チェック', layout)


def create_main_frame(tab_creators):
    tmgrid_frame = create_simulation_frame()
    basis_frame = create_basis_frame()
    parameter_tabs = sg.TabGroup([[creator() for creator in tab_creators]])

    check_frame = create_check_frame()
    extra_frame = create_extra_frame()

    layout = [
        [sg.Checkbox('use em mode', default=False, key='use_em'), sg.Checkbox(
            'use photoelectron', default=False, key='use_pe')],
        [basis_frame],
        [parameter_tabs, sg.Button('=>', key='Check'), check_frame],
        [tmgrid_frame, extra_frame],
        [sg.Submit(button_text='Save'), sg.Submit(
            button_text='Load'), sg.Button('Restart Window')]
    ]
    return sg.Frame('Parameter settings', layout)


def create_template_frame():
    template_files = glob.glob('template/*.inp')
    template_files = [os.path.basename(filename)
                      for filename in template_files]
    layout = [
        [sg.Listbox(template_files, key='template_file', size=(30, 30))],
        [sg.Button('Apply Template'), sg.Button('Save Template')]
    ]
    return sg.Frame('Template files', layout)
