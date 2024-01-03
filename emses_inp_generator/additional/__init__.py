from .additional_parameter import AdditionalParameters
from .charge_acceleration import ChargeAccelerationParameters
from .simple_plasma import SimplePlasmaParameters
from .boundary import BoundaryParameters
from .photo_electron import PhotoParameters
from .pic import PICParameters
from .simple_hole import SimpleHoleParameters
from .file_io_parameter import FileIOParameters

def add_additional_parameter(config, window_creator, loader, saver):
    param_classes = [
        (SimplePlasmaParameters, 10),
        (PICParameters, 50),
        (PhotoParameters, 100),
        (BoundaryParameters, 150),
        (SimpleHoleParameters, 200),
        (FileIOParameters, 300),
        (ChargeAccelerationParameters, 800),
    ]

    param_classes.sort(key=lambda x: x[1])
    for param_class, _ in param_classes:
        if param_class.is_active(config):
            param_class().add_parameters(window_creator, loader, saver)
