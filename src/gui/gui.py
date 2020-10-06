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
