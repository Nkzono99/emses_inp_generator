"""シンプルな形状の方形孔のパラメータを管理する.

管理するパラメータ:
    &ptcond
        zssurf
        xlrechole(1:2)
        ylrechole(1:2)
        yurechole(1:2)
        zlrechole(1:2)
        zurechole(1:2)
    &emissn
        nemd(1)
        xmine(1)
        xmaxe(1)
        ymine(1)
        ymaxe(1)
        zmine(1)
        zmaxe(1)

GUIのキー:
    zssurf : Surface height [grid]
    nemd : Direction of Sunlight (0: x, 1: y, 2: z)
    use_hole : Use hole
    hole_xlen : Hole X side length [grid]
    hole_ylen : Hole Y side length [grid]
    hole_depth : Hole depth [grid]
    thetaz : Sunlight incident angle z [dig]
    thetaxy : Sunlight incident angle xy [dig]
"""
import math
from typing import List

import PySimpleGUI as sg
from gui import parameter, radio_box

from additional import AdditionalParameters
from dataclasses import dataclass
from utils.emsesinp import Plasmainp


@dataclass
class EmissionSurface:
    nemd: int
    curf: float
    xmin: float
    xmax: float
    ymin: float
    ymax: float
    zmin: float
    zmax: float

    def saveinp(self, inp: Plasmainp, index: int):
        inp.setlist('emissn', 'nemd', self.nemd, start_index=index)
        inp.setlist('emissn', 'curfs', self.curf, start_index=index)
        inp.setlist('emissn', 'xmine', self.xmin, start_index=index)
        inp.setlist('emissn', 'xmaxe', self.xmax, start_index=index)
        inp.setlist('emissn', 'ymine', self.ymin, start_index=index)
        inp.setlist('emissn', 'ymaxe', self.ymax, start_index=index)
        inp.setlist('emissn', 'zmine', self.zmin, start_index=index)
        inp.setlist('emissn', 'zmaxe', self.zmax, start_index=index)


class SimpleHoleParameters(AdditionalParameters):
    @classmethod
    def is_active(cls, config):
        return config['Control'].getboolean('ControlSimpleHoleParameter')

    def create_tab(self):
        frame_layout = [
            [sg.Checkbox('Use hole', default=False, key='use_hole')],
            parameter('X side length [grid]', 10, key='hole_xlen'),
            parameter('Y side length [grid]', 10, key='hole_ylen'),
            parameter('depth [grid]', 10, key='hole_depth')
        ]
        hole_frame = sg.Frame('Hole', layout=frame_layout)

        tab_layout = [
            parameter('Surface hight [grid]', 10, key='zssurf'),
            [hole_frame],
            parameter('Sunlight zenith angle [dig]', 0.0, key='zenith'),
        ]
        return sg.Tab('穴パラメータ', layout=tab_layout)

    def add_applyers(self, loader):
        loader.add_applyer('zssurf', lambda i, u: i['zssurf'])

        def use_hole(i, u): return 'xlrechole' in i['ptcond'].keys()
        def hole_xlen(i, u): return i['xurechole'][0] - i['xlrechole'][0]
        def hole_ylen(i, u): return i['yurechole'][0] - i['ylrechole'][0]
        def hole_depth(i, u): return i['zurechole'][0] - i['zlrechole'][1]
        loader.add_applyer('use_hole', use_hole)
        loader.add_applyer('hole_xlen', hole_xlen, exceptor=use_hole)
        loader.add_applyer('hole_ylen', hole_ylen, exceptor=use_hole)
        loader.add_applyer('hole_depth', hole_depth, exceptor=use_hole)

        def use_emit(i, u): return 'curfs' in i
        def calc_zenith(i, j): return math.degrees(math.acos(abs(i['curfs'][0] / i['curf'][-1])))
        loader.add_applyer('zenith', calc_zenith, exceptor=use_emit)

    def add_savers(self, saver):
        saver.add_saver(self._save_hole_shape, lambda i, v, u: v['use_hole'])
        saver.add_saver(self._remove_hole, lambda i, v, u: not v['use_hole'])

        saver.add_saver(self._save_emission, lambda i, v, u: v['use_pe'])
        saver.add_saver(self._remove_emission,
                        lambda i, v, u: not v['use_pe'] or not v['use_hole'])

    def _save_hole_shape(self, inp, values, unit):
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
        inp.setlist('ptcond', 'xlrechole', [hole_x_min] * 2)
        inp.setlist('ptcond', 'xurechole', [hole_x_max] * 2)
        inp.setlist('ptcond', 'ylrechole', [hole_y_min] * 2)
        inp.setlist('ptcond', 'yurechole', [hole_y_max] * 2)
        inp.setlist('ptcond', 'zlrechole', [zssurf-1.0, zssurf-hole_depth])
        inp.setlist('ptcond', 'zurechole', [zssurf, zssurf-1.0])

    def _save_emission(self, inp: Plasmainp, values, unit):
        nx = int(values['nx'])
        ny = int(values['ny'])
        zssurf = float(values['zssurf'])

        # 垂直に太陽光が照射される場合の光電子電流
        curf = unit.J.trans(float(values['Jp']) * 1e-6)

        # 照射角を取得
        zenith_deg = float(values['zenith'])
        zenith_rad = math.radians((zenith_deg + 360) % 360)

        # 光電子電流を計算
        curf_horizon = curf * abs(math.cos(zenith_rad))
        curf_vertical = curf * abs(math.sin(zenith_rad))

        esurfs: List[EmissionSurface] = []
        if values['use_hole']:
            hole_xlen = float(values['hole_xlen'])
            hole_ylen = float(values['hole_ylen'])
            hole_depth = float(values['hole_depth'])
            hole_x_min = (nx - hole_xlen) / 2
            hole_x_max = (nx + hole_xlen) / 2
            hole_y_min = (ny - hole_ylen) / 2
            hole_y_max = (ny + hole_ylen) / 2
            hole_z_min = zssurf-hole_depth

            emit_x_min = hole_x_min + hole_depth * math.tan(zenith_rad)
            if zenith_rad == 0:
                emit_z_min = math.inf
            else:
                emit_z_min = zssurf - hole_xlen / math.tan(zenith_rad)

            # 光電子発生面を設定する
            esurfs.append(EmissionSurface(3, curf_horizon,
                                          0, hole_x_min, 0, ny, zssurf, zssurf))
            esurfs.append(EmissionSurface(3, curf_horizon,
                                          hole_x_min, hole_x_max, 0, hole_y_min, zssurf, zssurf))
            esurfs.append(EmissionSurface(3, curf_horizon,
                                          hole_x_max, nx, 0, ny, zssurf, zssurf))
            esurfs.append(EmissionSurface(3, curf_horizon,
                                          hole_x_min, hole_x_max, hole_y_max, ny, zssurf, zssurf))
            if emit_x_min < hole_x_max:
                esurfs.append(EmissionSurface(3, curf_horizon,
                                              emit_x_min, hole_x_max, hole_y_min, hole_y_max, hole_z_min, hole_z_min))
            if emit_z_min < zssurf:
                esurfs.append(EmissionSurface(-1, curf_vertical,
                                              hole_x_max, hole_x_max, hole_y_min, hole_y_max, emit_z_min, zssurf))
        else:
            esurfs.append(EmissionSurface(3, curf_horizon,
                                          0, nx, 0, ny, zssurf, zssurf))

        # 光電子面数を設定
        nepl = len(esurfs)
        inp.setlist('emissn', 'nepl', nepl, start_index=3)

        for i, esurf in enumerate(esurfs):
            esurf.saveinp(inp, index=i+1)

        # 不要な放出面に関わるパラメータを削除する.
        self._remove_emission(inp, values, unit)

    def _remove_hole(self, inp, values, unit):
        for index in (1, 2):
            inp.remove('xlrechole', index=index)
            inp.remove('xurechole', index=index)
            inp.remove('ylrechole', index=index)
            inp.remove('yurechole', index=index)
            inp.remove('zlrechole', index=index)
            inp.remove('zurechole', index=index)

    def _remove_emission(self, inp: Plasmainp, values, unit):
        nepl = nemd = 0
        if 'nepl' in inp:
            nepl = inp['nepl'][-1]
        if 'nemd' in inp:
            nemd = len(inp['nemd'])
        for i in range(nepl, nemd):
            inp.remove('nemd', index=nepl)
            inp.remove('xmine', index=nepl)
            inp.remove('xmaxe', index=nepl)
            inp.remove('ymine', index=nepl)
            inp.remove('ymaxe', index=nepl)
            inp.remove('zmine', index=nepl)
            inp.remove('zmaxe', index=nepl)
