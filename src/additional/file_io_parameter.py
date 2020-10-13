"""ファイルIOに関わるパラメータを管理する.

管理するパラメータ:
    &digcon
        hdfdigstart
        ifdiag
        ijdiag
        ifxyz(1:7)
        ijxyz(1:3)
        ipahdf(nspec)
        ipadig(nspec)
        ipaxyz(6, nspec)

GUIのキー:
    hdfdigstart : Steps to start output [step]
    output_field_interval : Output field step interval [step]
    output_particles_interval : Output particles step interval [step]
    output_potential : Output charge density and potential
    efxyz[0-2] : Output electric field xyz
    mfxyz[0-2] : Output magnetic field xyz
    ijxyz[0-2] : Output current density xyz
    ipadig : Number of output particles
    pxxyz[0-2] : Output particle position xyz
    pvxyz[0-2] : Ouptput particle velocity xyz
"""
import PySimpleGUI as sg
from gui import parameter, checkboxes

from additional import AdditionalParameters


class FileIOParameters(AdditionalParameters):
    def create_tab(self):
        field_layout = [
            parameter('Output field step interval [step]', 10000,
                      key='output_field_interval'),
            [checkboxes('Output charge density and potential', '',
                        base_key='output_potential',
                        defaults=True)],
            [checkboxes('Output electric field', 'x', 'y', 'z',
                        base_key='efxyz',
                        defaults=True)],
            [checkboxes('Output magnetic field', 'x', 'y', 'z',
                        base_key='mfxyz',
                        defaults=True)],
            [checkboxes('Output current density', 'x', 'y', 'z',
                        base_key='ijxyz',
                        defaults=True)]
        ]
        field_frame = sg.Frame('Field', field_layout)

        particle_layout = [
            parameter('Output particles step interval [step]', 0,
                      key='output_particles_interval'),
            parameter('Number of output particles', 1024,
                      key='ipadig'),
            [checkboxes('Output particle position', 'x', 'y', 'z',
                        base_key='pxxyz',
                        defaults=False)],
            [checkboxes('Ouptput particle velocity', 'x', 'y', 'z',
                        base_key='pvxyz',
                        defaults=False)]
        ]
        particle_frame = sg.Frame('Particles', particle_layout)
        layout = [
            parameter('Steps to start output [step]', 0,
                      key='hdfdigstart'),
            [field_frame],
            [particle_frame]
        ]
        return sg.Tab('ファイル出力', layout)

    def add_applyers(self, loader):
        loader.add_applyer('hdfdigstart', lambda i, u: i['hdfdigstart'])

        loader.add_applyer('output_field_interval', lambda i, u: i['ifdiag'])
        loader.add_applyer('output_particles_interval',
                           lambda i, u: i['ipahdf'][0])
        loader.add_applyer('ipadig', lambda i, u: i['ipadig'][0])

        loader.add_applyer('output_potential0',
                           lambda i, u: i['ifxyz'][6] == 1)

        loader.add_applyer('efxyz0', lambda i, u: i['ifxyz'][0] == 1)
        loader.add_applyer('efxyz1', lambda i, u: i['ifxyz'][1] == 1)
        loader.add_applyer('efxyz2', lambda i, u: i['ifxyz'][2] == 1)

        loader.add_applyer('mfxyz0', lambda i, u: i['ifxyz'][3] == 1)
        loader.add_applyer('mfxyz1', lambda i, u: i['ifxyz'][4] == 1)
        loader.add_applyer('mfxyz2', lambda i, u: i['ifxyz'][5] == 1)

        loader.add_applyer('ijxyz0', lambda i, u: i['ijxyz'][0] == 1)
        loader.add_applyer('ijxyz1', lambda i, u: i['ijxyz'][1] == 1)
        loader.add_applyer('ijxyz2', lambda i, u: i['ijxyz'][2] == 1)

        loader.add_applyer('pxxyz0', lambda i, u: i['ipaxyz'][0] == 1)
        loader.add_applyer('pxxyz1', lambda i, u: i['ipaxyz'][1] == 1)
        loader.add_applyer('pxxyz2', lambda i, u: i['ipaxyz'][2] == 1)
        loader.add_applyer('pvxyz0', lambda i, u: i['ipaxyz'][3] == 1)
        loader.add_applyer('pvxyz1', lambda i, u: i['ipaxyz'][4] == 1)
        loader.add_applyer('pvxyz2', lambda i, u: i['ipaxyz'][5] == 1)

    def add_savers(self, saver):
        saver.add_saver(self._save_steps)
        saver.add_saver(self._save_ifjxyz)
        saver.add_saver(self._save_ipaxyz)

    def _save_steps(self, inp, values, unit):
        nspec = 3 if values['use_pe'] else 2

        inp['digcon']['hdfdigstart'] = int(values['hdfdigstart'])
        inp['digcon']['ifdiag'] = int(values['output_field_interval'])
        inp['digcon']['ijdiag'] = int(values['output_field_interval'])

        inp.setlist('digcon', 'ipahdf', [
                    int(values['output_particles_interval'])] * nspec)
        inp.setlist('digcon', 'ipadig', [int(values['ipadig'])] * nspec)

    def _save_ifjxyz(self, inp, values, unit):
        efxyzs = [int(values['efxyz{}'.format(i)]) for i in range(3)]
        mfxyzs = [int(values['mfxyz{}'.format(i)]) for i in range(3)]
        output_potential = int(values['output_potential0'])
        inp.setlist('digcon', 'ifxyz', [*efxyzs, *mfxyzs, output_potential])

        ijxyzs = [int(values['ijxyz{}'.format(i)]) for i in range(3)]
        inp.setlist('digcon', 'ijxyz', ijxyzs)

    def _save_ipaxyz(self, inp, values, unit):
        nspec = 3 if values['use_pe'] else 2
        pxxyzs = [int(values['pxxyz{}'.format(i)]) for i in range(3)]
        pvxyzs = [int(values['pvxyz{}'.format(i)]) for i in range(3)]
        inp['digcon']['ipaxyz'] = [*pxxyzs, *pvxyzs] * nspec
