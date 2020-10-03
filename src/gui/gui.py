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

    n0 : Plasma density [/cc]
    Te : Electron temperature [eV]
    Ti : Ion temperature [eV]
    mi2me : Ion-to-electron mass ratio
    vdrie : Electron flow speed [m/s]
    vdrii : Ion flow speed [m/s]
    B : Magntic field [nT]

    np_per_grid : Number of superparticles per grid

    Jp : PE current density [microA/m^2]
    Tp : PE temprature [eV]
    dnsfp : Number of superparticles per photoelectron

    nbndx[0-1] : Field Boundary X
    nbndy[0-1] : Field Boundary Y
    nbndz[0-1] : Field Boundary Z
    npbndx[0-2] : Particles Boundary X
    npbndx[0-2] : Particles Boundary Y
    npbndx[0-2] : Particles Boundary Z

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
    default_tab_creators = [
        bc.create_plasma_tab,
        bc.create_boundary_tab,
        bc.create_pic_parameter,
        bc.create_photo_tab
    ]

    def __init__(self,
                 tab_creators=None,
                 title='plasma.inp generator',
                 theme='Dark Blue 3'):
        self.title = title
        self.theme = theme

        if tab_creators is None:
            self.tab_creators = WindowCreator.default_tab_creators
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
