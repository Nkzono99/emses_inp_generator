"""PICのパラメータを管理する.

管理するパラメータ:
    &intp
        npin(1:2)

GUIのキー:
    np_per_grid: Number of super particles per grid
"""
import PySimpleGUI as sg
from ..gui import parameter, radio_box

from . import AdditionalParameters


class ChargeAccelerationParameters(AdditionalParameters):
    @classmethod
    def is_active(cls, config):
        return config['Control'].getboolean('ControlChargeAccelerationParameter')

    def create_tab(self):
        layout = [
            parameter('Acceleration coefficient', 1.0, key='grad_coef'),
            parameter('Smoothing coefficient', 1.0, key='smooth_coef'),
        ]
        return sg.Tab('帯電加速', layout)

    def add_applyers(self, loader):
        loader.add_applyer('grad_coef', lambda i, u: i['grad_coef'])
        loader.add_applyer('smooth_coef', lambda i, u: i['smooth_coef'])

    def add_savers(self, saver):
        saver.add_saver(self._save)

    def _save(self, inp, values, unit):
        inp['gradema']['grad_coef'] = float(values['grad_coef'])
        inp['gradema']['smooth_coef'] = float(values['smooth_coef'])
