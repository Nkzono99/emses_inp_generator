import PySimpleGUI as sg
import math

from gui.basic_components import parameter, radio_box


def add_simple_hole_parameter(window_creator, loader, saver):
    window_creator.add_tab_creator(create_simple_hole_tab)
    add_applyer(loader)

    saver.add_saver(save_hole_shape, lambda i, v, u: v['use_hole'])
    saver.add_saver(remove_hole, lambda i, v, u: not v['use_hole'])

    saver.add_saver(save_emission, lambda i, v, u: v['use_pe'])
    saver.add_saver(remove_emission, lambda i, v, u: not v['use_pe'] or not v['use_hole'])


def create_simple_hole_frame():
    frame_layout = [
        [sg.Checkbox('Use hole', default=False, key='use_hole')],
        parameter('X side length [grid]', 10, key='hole_xlen'),
        parameter('Y side length [grid]', 10, key='hole_ylen'),
        parameter('depth [grid]', 10, key='hole_depth')
    ]
    return sg.Frame('Hole', layout=frame_layout)


def create_simple_hole_tab():
    layout = [
        parameter('Surface hight [grid]', 10, key='zssurf'),
        [create_simple_hole_frame()],
        radio_box('Direction of Sunlight', 'x', 'y',
                  'z', group_id='nemd', default_index=2),
        parameter('Sunlight incident angle z [dig]', 0.0, key='thetaz'),
        parameter('Sunlight incident angle xy [dig]', 180.0, key='thetaxy')
    ]
    return sg.Tab('穴パラメータ', layout)


def add_applyer(loader):
    loader.add_applyer('zssurf', lambda i, u: i['zssurf'])

    def use_hole(i, u): return 'xlrechole' in i['ptcond'].keys()
    def hole_xlen(i, u): return i['xurechole'][0] - i['xlrechole'][0]
    def hole_ylen(i, u): return i['yurechole'][0] - i['ylrechole'][0]
    def hole_depth(i, u): return i['zurechole'][0] - i['zlrechole'][1]
    loader.add_applyer('use_hole', use_hole)
    loader.add_applyer('hole_xlen', hole_xlen, exceptor=use_hole)
    loader.add_applyer('hole_ylen', hole_ylen, exceptor=use_hole)
    loader.add_applyer('hole_depth', hole_depth, exceptor=use_hole)
    loader.add_applyer('nemd0', lambda i, u: i['nemd'][0] == 1)
    loader.add_applyer('nemd1', lambda i, u: i['nemd'][0] == 2)
    loader.add_applyer('nemd2', lambda i, u: i['nemd'][0] == 3)
    loader.add_applyer('thetaz', lambda i, u: i['thetaz'])
    loader.add_applyer('thetaxy', lambda i, u: i['thetaxy'])


def save_hole_shape(inp, values, unit):
    nx = int(values['nx'])
    ny = int(values['ny'])
    zssurf = float(values['zssurf'])
    hole_xlen = float(values['hole_xlen'])
    hole_ylen = float(values['hole_ylen'])
    hole_depth = float(values['hole_depth'])
    hole_x_min = (nx - hole_xlen) / 2
    hole_x_max = (nx + hole_xlen) / 2
    hole_y_min = (ny - hole_ylen) / 2
    hole_y_max = (ny + hole_ylen) / 2

    inp['ptcond']['zssurf'] = zssurf
    inp['ptcond']['xlrechole'] = [hole_x_min] * 2
    inp['ptcond']['xurechole'] = [hole_x_max] * 2
    inp['ptcond']['ylrechole'] = [hole_y_min] * 2
    inp['ptcond']['yurechole'] = [hole_y_max] * 2
    inp['ptcond']['zlrechole'] = [zssurf-1.0, zssurf-hole_depth]
    inp['ptcond']['zurechole'] = [zssurf, zssurf-1.0]


def save_emission(inp, values, unit):
    nx = int(values['nx'])
    ny = int(values['ny'])
    zssurf = float(values['zssurf'])
    hole_xlen = float(values['hole_xlen'])
    hole_ylen = float(values['hole_ylen'])
    hole_depth = float(values['hole_depth'])
    hole_x_min = (nx - hole_xlen) / 2
    hole_x_max = (nx + hole_xlen) / 2
    hole_y_min = (ny - hole_ylen) / 2
    hole_y_max = (ny + hole_ylen) / 2
    hole_z_min = zssurf-hole_depth
    thetaz = float(values['thetaz'])
    thetaxy = float(values['thetaxy'])

    inp['emissn']['thetaz'] = thetaz
    inp['emissn']['thetaxy'] = thetaxy

    # 光電子発生範囲を設定する
    # 真上から太陽光が照射している場合
    if thetaz == 0:
        inp.setlist('emissn', 'nepl', 1, start_index=3)
        inp['emissn']['nemd'] = [3]
        inp['emissn']['xmine'] = [hole_x_min]
        inp['emissn']['xmaxe'] = [hole_x_max]
        inp['emissn']['ymine'] = [hole_y_min]
        inp['emissn']['ymaxe'] = [hole_y_max]
        inp['emissn']['zmine'] = [hole_z_min]
        inp['emissn']['zmaxe'] = [hole_z_min]
        return

    # ラジアンに変換
    theta = math.radians((thetaxy + 180) % 180)
    phi = math.radians((thetaz + 360) % 360)

    # 太陽光が照射される範囲を計算する
    if theta <= math.pi / 2 or math.pi * 3 / 2 <= theta:  # from +x
        x_min = hole_x_min
        x_max = hole_x_max - hole_depth * math.cos(theta) / math.tan(phi)
    else:  # from -x
        x_min = hole_x_min + hole_depth * math.cos(theta) / math.tan(phi)
        x_max = hole_x_max

    if theta <= math.pi:  # from +y
        y_min = hole_y_min
        y_max = hole_y_max - hole_depth * math.sin(theta) / math.tan(phi)
    else:  # from -y
        y_min = hole_y_min + hole_depth * math.sin(theta) / math.tan(phi)
        y_max = hole_y_max
    
    # 穴底面に入射しない場合放出面に関わるパラメータを削除する.
    if x_min > x_max or y_min > y_max:
        remove_emission(inp, values, unit)
        return

    inp.setlist('emissn', 'nepl', 1, start_index=3)
    inp['emissn']['nemd'] = [3]
    inp['emissn']['xmine'] = [x_min]
    inp['emissn']['xmaxe'] = [x_max]
    inp['emissn']['ymine'] = [y_min]
    inp['emissn']['ymaxe'] = [y_max]
    inp['emissn']['zmine'] = [hole_z_min]
    inp['emissn']['zmaxe'] = [hole_z_min]


def remove_hole(inp, values, unit):
    inp.remove('xlrechole')
    inp.remove('xurechole')
    inp.remove('ylrechole')
    inp.remove('yurechole')
    inp.remove('zlrechole')
    inp.remove('zurechole')


def remove_emission(inp, values, unit):
    inp.setlist('emissn', 'nepl', 0, start_index=3)
    inp.remove('nemd')
    inp.remove('xmine')
    inp.remove('xmaxe')
    inp.remove('ymine')
    inp.remove('ymaxe')
    inp.remove('zmine')
    inp.remove('zmaxe')