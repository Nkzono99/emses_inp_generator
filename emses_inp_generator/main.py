"""Plasma.inpのパラメータを管理する.

以下に示されているもの以外はadditionalパッケージで追加管理する.

デフォルトで管理するパラーメータ:
    &esorem
        emflag
    &jobcon
        jobnum(1:)
        nstep
    &plasma
        cv
    &tmgrid
        dt
        nx
        ny
        nz
    &system
        nspec
    &mpi
        nodes(1:3)

デフォルトのGUIのキー:
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
import math
import os
from argparse import ArgumentParser
from configparser import ConfigParser

import PySimpleGUI as sg

from .additional import add_additional_parameter
from .default import (
    WindowCreator,
    create_conversion_window,
    create_default_loader,
    create_default_saver,
    to_emses_unit,
    to_physical_unit,
)
from .default.config_manager import create_config_window, reset_config, update_config
from emout import InpFile, UnitConversionKey, Units

from pathlib import Path


ROOT_DIR = Path(__file__).parent


def debye(values):
    # Since the conversion function is not used, dx and to_c are filled with meaningless values.
    unit = Units(dx=0.001, to_c=10000)
    qe = unit.qe.from_unit
    e0 = unit.e0.from_unit
    n0 = float(values["n0"]) * 1e6
    Te = float(values["Te"])
    return math.sqrt(e0 * qe * Te / (n0 * qe * qe))


def egyro(values):
    # Since the conversion function is not used, dx and to_c are filled with meaningless values.
    unit = Units(dx=0.001, to_c=10000)
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    Te = float(values["Te"])
    B = float(values["B"]) * 1e-9
    if B == 0:
        return -1
    return math.sqrt(me * qe * Te) / (qe * B)


def igyro(values):
    # Since the conversion function is not used, dx and to_c are filled with meaningless values.
    unit = Units(dx=0.001, to_c=10000)
    qe = unit.qe.from_unit
    mi = unit.me.from_unit * float(values["mi2me"])
    Ti = float(values["Ti"])
    B = float(values["B"]) * 1e-9
    if B == 0:
        return -1
    return math.sqrt(mi * qe * Ti) / (qe * B)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("inppath", nargs="?", default=None)
    parser.add_argument(
        "--config", default=str((ROOT_DIR / "config.ini").resolve()), help="Config file"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    config = ConfigParser()
    config.read(args.config)

    wc = WindowCreator(theme=config["Default"]["ColorTheme"])
    loader = create_default_loader(
        use_physical_dt=config["Control"].getboolean("UsePhysicalDt")
    )
    saver = create_default_saver(
        use_physical_dt=config["Control"].getboolean("UsePhysicalDt")
    )

    add_additional_parameter(config, wc, loader, saver)

    main_window = wc.create_window(
        use_physical_dt=config["Control"].getboolean("UsePhysicalDt")
    )
    conv_window = None
    config_window = None

    inppath = args.inppath or ROOT_DIR / config["Default"]["DefaultInpPath"]
    inp = loader.load(inppath, main_window)
    if inp is None:
        inp = InpFile()

    while True:
        window, event, values = sg.read_all_windows()

        if window == sg.WIN_CLOSED:
            break
        if event == sg.WIN_CLOSED:
            if window == main_window:
                break
            if window == conv_window:
                conv_window.close()
                conv_window = None

            if window == config_window:
                config_window.close()
                config_window = None

        if event == "Save":
            filename = sg.popup_get_file(
                "保存するファイル名を指定してください",
                save_as=True,
                default_path="plasma.inp",
                default_extension="inp",
                no_window=True,
                file_types=(("Input Files", ".inp"), ("ALL Files", "*")),
            )
            if filename is None or len(filename) == 0:
                continue
            saver.save(filename, inp, values)

        if event == "Load":
            filename = sg.popup_get_file(
                "読み込むファイル名を指定してください",
                default_path="plasma.inp",
                default_extension="inp",
                no_window=True,
                file_types=(("Input Files", ".inp"), ("ALL Files", "*")),
                initial_folder=ROOT_DIR / "template",
            )
            if filename is None or len(filename) == 0:
                continue
            res = loader.load(filename, main_window)
            if res is not None:
                inp = res

        if event == "Apply Template" or event == "template_file_double_clicked":
            if len(values["template_file"]) == 0:
                continue

            filename = values["template_file"][0]
            filepath = str((ROOT_DIR / "template" / filename).resolve())

            res = loader.load(filepath, main_window)
            if res is not None:
                inp = res

        if event == "Save Template":
            filename = sg.popup_get_file(
                "保存するファイル名を指定してください",
                save_as=True,
                default_path="template.inp",
                default_extension="inp",
                initial_folder=ROOT_DIR / "template",
                no_window=True,
                file_types=(("Input Files", ".inp"), ("ALL Files", "*")),
            )
            if filename is None or len(filename) == 0:
                continue
            saver.save(filename, inp, values)

        if event == "Check":
            main_window["debye"].Update(value=debye(values))
            main_window["egyro"].Update(value=egyro(values))
            main_window["igyro"].Update(value=igyro(values))

        if event == "Open Conversion":
            if conv_window is not None:
                conv_window.close()
            offset_x = float(config["Default"]["ConversionWindowOffsetX"])
            offset_y = float(config["Default"]["ConversionWindowOffsetY"])
            move_x = int(main_window.current_location()[0] + offset_x)
            move_y = max(int(main_window.current_location()[1] + offset_y), 0)
            conv_window = create_conversion_window(location=(move_x, move_y))
            conv_window.finalize()

        if event == "To EMSES Unit":
            dx = float(main_window["dx"].get())
            to_c = float(main_window["em_c"].get())
            to_emses_unit(conv_window, values, dx=dx, to_c=to_c)

        if event == "To Physical Unit":
            dx = float(main_window["dx"].get())
            to_c = float(main_window["em_c"].get())
            to_physical_unit(conv_window, values, dx=dx, to_c=to_c)

        if event == "Restart Window":
            res = sg.popup_ok_cancel("Can I just restart this window?")
            if res == "OK":
                main_window.close()
                if conv_window is not None:
                    conv_window.close()
                main()
                return

        if event == "Open Config":
            if config_window is not None:
                config_window.close()
            offset_x = float(config["Default"]["ConfigWindowOffsetX"])
            offset_y = float(config["Default"]["ConfigWidowOffsetY"])
            move_x = int(main_window.current_location()[0] + offset_x)
            move_y = max(int(main_window.current_location()[1] + offset_y), 0)
            config_window = create_config_window(config, location=(move_x, move_y))
            config_window.finalize()

        if event == "Reset Config":
            reset_config(config, values)

        if event == "Save Config":
            update_config(config, values)
            with open("config.ini", "w", encoding="utf-8") as f:
                config.write(f)

    main_window.close()


if __name__ == "__main__":
    main()
