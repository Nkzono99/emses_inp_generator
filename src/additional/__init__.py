from additional.additional_parameter import AdditionalParameters
from additional.simple_plasma import SimplePlasmaParameters
from additional.boundary import BoundaryParameters
from additional.photo_electron import PhotoParameters
from additional.pic import PICParameters
from additional.simple_hole import SimpleHoleParameters
from additional.file_io_parameter import FileIOParameters

def add_additional_parameter(config, window_creator, loader, saver):
    SimplePlasmaParameters().add_parameters(window_creator, loader, saver)
    PICParameters().add_parameters(window_creator, loader, saver)

    if config['Control'].getboolean('ControlPhotoelectronParameter'):
        PhotoParameters().add_parameters(window_creator, loader, saver)

    if config['Control'].getboolean('ControlBoundaryParameter'):
        BoundaryParameters().add_parameters(window_creator, loader, saver)
    
    if config['Control'].getboolean('ControlSimpleHoleParameter'):
        SimpleHoleParameters().add_parameters(window_creator, loader, saver)
    
    if config['Control'].getboolean('ControlFileIOParameter'):
        FileIOParameters().add_parameters(window_creator, loader, saver)
