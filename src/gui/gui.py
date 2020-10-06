"""
GUI設定.

keyとパラメータの関係
    use_em : Use em mode
    use_pe : Use photoelectron

    dx : Grid Width [m]
    c : Light speed [m/s]
    qe/me : Electron charge-to-mass ratio
    e0 : FS-Permittivity [Fm^-1]

    em_dx : Grid Width (EMSES Unit)
    em_c : Light speed (EMSES Unit)
    em_qe/me : Electron charge-to-mass ratio (EMSES Unit)
    em_e0 : FS-Permittivity (EMSES Unit)

    dt : dt [s]
    nx : nx
    ny : ny
    nz : nz
    nstep : nstep

    jobnum : jobnum
    nodesx : nodes x
    nodesy : nodes y
    nodesz : nodes z

    debye : Debye Length [m]
    egyro : Electron gyro radius [m]
    igyro : Ion gyro radius [m]

"""
import glob

import PySimpleGUI as sg

import gui.basic_components as bc


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

    def create_window(self):
        sg.theme(self.theme)

        template_frame = bc.create_template_frame()
        main_frame = bc.create_main_frame(self.tab_creators)

        layout = [
            [template_frame, main_frame]
        ]

        window = sg.Window(self.title, layout)
        return window
