from additional.simple_plasma import add_simple_plasma_parameter
from additional.boundary import add_boundary_parameter
from additional.photo_electron import add_photo_parameter
from additional.pic import add_pic_parameter
from additional.simple_hole import add_simple_hole_parameter


def add_additional_parameter(config, window_creator, loader, saver):
    add_simple_plasma_parameter(window_creator, loader, saver)
    add_pic_parameter(window_creator, loader, saver)

    if config['Control'].getboolean('ControlPhotoelectronParameter'):
        add_photo_parameter(window_creator, loader, saver)

    if config['Control'].getboolean('ControlBoundaryParameter'):
        add_boundary_parameter(window_creator, loader, saver)
    
    if config['Control'].getboolean('ControlSimpleHoleParameter'):
        add_simple_hole_parameter(window_creator, loader, saver)
