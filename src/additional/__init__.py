from additional.simple_hole import add_simple_hole_parameter


def add_additional_parameter(config, window_creator, loader, saver):
    if config['Verbose'].getboolean('UseHole'):
        add_simple_hole_parameter(window_creator, loader, saver)
