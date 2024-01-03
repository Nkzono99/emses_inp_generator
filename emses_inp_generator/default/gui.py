import glob
import os

import PySimpleGUI as sg

from ..gui import basis_parameter, parameter


class WindowCreator:
    def __init__(self,
                 tab_creators=None,
                 title='plasma.inp generator',
                 theme='Dark Blue 3'):
        self.title = title
        self.theme = theme

        if tab_creators is None:
            self.tab_creators = []
        else:
            self.tab_creators = tab_creators

    def add_tab_creator(self, tab_creator):
        self.tab_creators.append(tab_creator)

    def create_window(self, use_physical_dt=False):
        sg.theme(self.theme)

        template_frame = create_template_frame()
        main_frame = create_main_frame(self.tab_creators, use_physical_dt)

        layout = [
            [template_frame, main_frame]
        ]

        window = sg.Window(self.title, layout, finalize=True)
        window['template_file'].bind('<Double-Button-1>', '_double_clicked')
        return window


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


def create_simulation_frame(use_physical_dt):
    if use_physical_dt:
        layout = [
            parameter('dt [s]', 0.01, key='dt'),
            parameter('nx', 64, key='nx'),
            parameter('ny', 64, key='ny'),
            parameter('nz', 512, key='nz'),
            parameter('nstep', 100000, key='nstep')
        ]
    else:
        layout = [
            parameter('dt', 0.01, key='dt'),
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


def create_main_frame(tab_creators, use_physical_dt):
    tmgrid_frame = create_simulation_frame(use_physical_dt=use_physical_dt)
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
        [sg.Submit(button_text='Save'),
         sg.Button(button_text='Load'),
         sg.Button('Restart Window'),
         sg.Button('Open Config'),
         sg.Button('Open Conversion'),
         sg.Text('Base file: None', key='basefile', size=(100, 1))]
    ]
    return sg.Frame('Parameter settings', layout)


def create_template_frame():
    from pathlib import Path

    template_dir = str((Path(__file__).parent.parent / "template").resolve())
    print(template_dir)
    template_files = glob.glob(f'{template_dir}/*.inp')
    template_files = [os.path.basename(filename)
                      for filename in template_files]
    template_list = sg.Listbox(
        template_files, key='template_file', size=(30, 30))
    layout = [
        [template_list],
        [sg.Button('Apply Template'), sg.Button('Save Template')]
    ]
    return sg.Frame('Template files', layout)
