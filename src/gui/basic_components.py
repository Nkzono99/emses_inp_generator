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


def selectIndex(values, name):
    for key, value in values.items():
        if key.startswith(name) and value == True:
            return int(key.replace(name, ''))
    return None


def conversion(name, key, default=0, em_default=0):
    name_text = sg.Text(name, size=name_size)
    physical_unit = sg.InputText(str(default), size=value_size, key=key)
    emses_unit = sg.InputText(str(em_default),
                              size=value_size,
                              key='em_{}'.format(key))
    return sg.Column([[name_text, physical_unit, sg.Text('<=>'), emses_unit]])
