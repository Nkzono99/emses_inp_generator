import math

from emsesinp import UnitConversionKey
from units import Units


def wpe(values, unit):
    ne = float(values['n0']) * 1e6  # /cc to /m^3
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    e0 = unit.e0.from_unit
    wpe_phisic = math.sqrt(ne * qe * qe / me / e0)
    return unit.f.trans(wpe_phisic)


def wpi(values, unit):
    ni = float(values['n0']) * 1e6
    qe = unit.qe.from_unit
    mi = unit.me.from_unit * float(values['mi2me'])
    e0 = unit.e0.from_unit
    wpi_phisic = math.sqrt(ni * qe * qe / mi / e0)
    return unit.f.trans(wpi_phisic)


def wc(values, unit):
    B = float(values['B']) * 1e-9
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    wc_phisic = qe * B / me
    return unit.f.trans(wc_phisic)


def pathe(values, unit):
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    Te = float(values['Te'])
    pathe_phisic = math.sqrt(qe * Te / me)
    return unit.v.trans(pathe_phisic)


def pathi(values, unit):
    qe = unit.qe.from_unit
    mi = unit.me.from_unit * float(values['mi2me'])
    Ti = float(values['Ti'])
    pathi_phisic = math.sqrt(qe * Ti / mi)
    return unit.v.trans(pathi_phisic)


def pathp(values, unit):
    qe = unit.qe.from_unit
    me = unit.me.from_unit
    Tp = float(values['Tp'])
    pathp_phisic = math.sqrt(qe * Tp / me)
    return unit.v.trans(pathp_phisic)


def vdrie(values, unit):
    return unit.v.trans(float(values['vdrie']))


def vdrii(values, unit):
    return unit.v.trans(float(values['vdrii']))


def curf(values, unit):
    return unit.J.trans(float(values['Jp']) * 1e-6)


def selectIndex(values, name):
    for key, value in values.items():
        if key.startswith(name) and value == True:
            return int(key.replace(name, ''))
    return None


def save(inp, filename, values):
    dx = float(values['dx'])
    to_c = float(values['em_c'])
    unit = Units(dx=dx, to_c=to_c)

    convkey = UnitConversionKey(dx=dx, to_c=to_c)

    nx = int(values['nx'])
    ny = int(values['ny'])
    nz = int(values['nz'])

    # set inp
    inp['esorem']['emflag'] = 1 if values['use_em'] else 0

    inp['jobcon']['jobnum'] = list(map(int, values['jobnum'].split(' ')))
    inp['jobcon']['nstep'] = int(values['nstep'])

    inp['plasma']['wp'] = [wpe(values, unit), wpi(values, unit)]
    inp['plasma']['wc'] = wc(values, unit)
    inp['plasma']['cv'] = to_c

    inp['tmgrid']['dt'] = unit.t.trans(float(values['dt']))
    inp['tmgrid']['nx'] = nx
    inp['tmgrid']['ny'] = ny
    inp['tmgrid']['nz'] = nz

    nspec = 3 if values['use_pe'] else 2
    inp['system']['nspec'] = nspec
    inp['system']['nfbnd'] = [selectIndex(values, 'nfbndx'),
                              selectIndex(values, 'nfbndy'),
                              selectIndex(values, 'nfbndz')]
    inp['system']['npbnd'] = [selectIndex(values, 'npbndx'),
                              selectIndex(values, 'npbndy'),
                              selectIndex(values, 'npbndz')] * nspec

    inp['intp']['qm'] = [-1.0, 1.0/float(values['mi2me'])]
    inp['intp']['npin'] = [int(values['np_per_grid']) * nx * ny * nz] * 2
    inp['intp']['path'] = [pathe(values, unit), pathi(values, unit)]
    inp['intp']['peth'] = [pathe(values, unit), pathi(values, unit)]
    inp['intp']['vdri'] = [vdrie(values, unit), vdrii(values, unit)]

    inp['mpi']['nodes'] = [int(values['nodesx']),
                           int(values['nodesy']),
                           int(values['nodesz'])]

    # 光電子の設定を追加
    if values['use_pe']:
        inp['plasma']['wp'].append(wpe(values, unit))

        inp['intp']['qm'].append(-1.0)
        inp['intp']['path'].append(pathp(values, unit))
        inp['intp']['peth'].append(pathp(values, unit))
        inp['intp']['npin'].append(0)
        inp['intp'].start_index['np'] = [3]
        inp['intp']['np'] = [int(values['np_per_grid']) * nx * ny * nz]

        inp['emissn'].start_index['curf'] = [3]
        inp['emissn']['curf'] = [curf(values, unit)]
        inp['emissn']['nflag_emit'] = [0, 0, 2]
        inp['emissn'].start_index['dnsf'] = [3]
        inp['emissn']['dnsf'] = [int(values['dnsfp'])]

    inp.save(filename, convkey=convkey)
