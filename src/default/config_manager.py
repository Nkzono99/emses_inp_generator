import PySimpleGUI as sg
from gui.basic_components import parameter
from utils import UnitConversionKey, Units


def create_config_window(config, location=None):
    tabs = []
    for key_section, section in config.items():
        layout = [
            parameter(key, value, key=f'config_{key_section}_{key}') \
                for key, value in section.items()
        ]
        if len(layout) == 0:
            continue
        tab = sg.Tab(key_section, layout)
        tabs.append(tab)

    window_layout = [
        [sg.TabGroup([tabs])],
        [sg.Button('Reset Config'), sg.Button('Save Config')],
    ]
    return sg.Window('Config設定', layout=window_layout, location=location)


def reset_config(config, values):
    for key_section, section in config.items():
        for key, value in section.items():
            values[f'config_{key_section}_{key}'] = value


def update_config(config, values):
    for key_section, section in config.items():
        for key, value in section.items():
            section[key] = values[f'config_{key_section}_{key}']
