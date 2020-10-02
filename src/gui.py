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


def radio_box(name, *selections, group_id):
    name_text = sg.Text(name, size=name_size)
    radios = [sg.Radio(selection, group_id=group_id, default=(
        i == 0), key='{}{}'.format(group_id, i)) for i, selection in enumerate(selections)]
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


def create_plasma_tab():
    layout = [
        parameter('Plasma density [/cc]', 5000, key='n0'),
        parameter('Electron temperature [eV]', 1.0, key='Te'),
        parameter('Ion temperature [eV]', 0.5, key='Ti'),
        parameter('Ion-to-electron mass ratio', 1000, key='mi2me'),
        parameter('Electron flow speed [m/s]', 1000, key='vdrie'),
        parameter('Ion flow speed [m/s]', 1000, key='vdrii'),
        parameter('Magnetic field [nT]', 0, key='B')
    ]
    return sg.Tab('プラズマパラメータ', layout)


def create_pic_parameter():
    layout = [
        parameter('Number of super particles per grid', 40, key='np_per_grid')
    ]
    return sg.Tab('PICパラメータ', layout)


def create_photo_tab():
    layout = [
        parameter('PE current density [microA/m^2]', 0, key='Jp'),
        parameter('PE temprature [eV]', 1.0, key='Tp'),
        parameter('Number of superparticles per PE', 40, key='dnsfp')
    ]
    return sg.Tab('光電子パラメータ', layout)


def create_boundary_tab():
    layout = [
        radio_box('Field Boundary X', 'periodic', 'free', group_id='nfbndx'),
        radio_box('Field Boundary Y', 'periodic', 'free', group_id='nfbndy'),
        radio_box('Field Boundary Z', 'periodic', 'free', group_id='nfbndz'),
        radio_box('Particles Boundary X', 'periodic',
                  'Dirichlet', 'Neumann', group_id='npbndx'),
        radio_box('Particles Boundary Y', 'periodic',
                  'Dirichlet', 'Neumann', group_id='npbndy'),
        radio_box('Particles Boundary Z', 'periodic',
                  'Dirichlet', 'Neumann', group_id='npbndz'),
    ]
    return sg.Tab('境界条件', layout)


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


def create_main_frame():
    tmgrid_frame = create_simulation_frame()
    basis_frame = create_basis_frame()

    plasma_tab = create_plasma_tab()
    boundary_tab = create_boundary_tab()
    pic_tab = create_pic_parameter()
    photo_tab = create_photo_tab()
    parameter_tabs = sg.TabGroup(
        [[plasma_tab, boundary_tab, pic_tab, photo_tab]])

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
    layout = [
        [sg.Listbox(template_files, key='template_file', size=(30, 30))],
        [sg.Button('Apply Template'), sg.Button('Save Template')]
    ]
    return sg.Frame('Template files', layout)


def create_window():
    sg.theme('Dark Blue 3')

    template_frame = create_template_frame()
    main_frame = create_main_frame()

    layout = [
        [template_frame, main_frame]
    ]

    window = sg.Window('plasma.inp generator', layout)
    return window
