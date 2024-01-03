import PySimpleGUI as sg
from emout import UnitConversionKey, Units

from ..gui import conversion


def create_conversion_window(location=None):
    layout = [
        [conversion('Mass [kg]', key='conv_m')],
        [conversion('Time [s]', key='conv_t')],
        [conversion('Frequency [Hz]', key='conv_f')],
        [conversion('Velocity [m/s]', key='conv_v')],
        [conversion('Number density [m^-3]', key='conv_n')],
        [conversion('Flux [m^-2s^-1]', key='conv_N')],
        [conversion('Force [N]', key='conv_F')],
        [conversion('Power [W]', key='conv_P')],
        [conversion('Energy [J]', key='conv_W')],
        [conversion('Energy density [Jm^-3]', key='conv_w')],
        [conversion('Permittivity [Fm-1]', key='conv_eps')],
        [conversion('Charge [C]', key='conv_q')],
        [conversion('Charge density [Cm-3]', key='conv_rho')],
        [conversion('Charge-to-mass ratio [Ckg-1]', key='conv_q_m')],
        [conversion('Current [A]', key='conv_I')],
        [conversion('Current density [Am-2]', key='conv_J')],
        [conversion('Potential [V]', key='conv_phi')],
        [conversion('Electric field [Vm-1]', key='conv_E')],
        [conversion('Capacitance [F]', key='conv_C')],
        [conversion('Resistance [Ω]', key='conv_R')],
        [conversion('Conductance [S]', key='conv_G')],
        [conversion('Permiability [Hm-1]', key='conv_mu')],
        [conversion('Magnetic flux density [T]', key='conv_B')],
        [conversion('Inductance [H]', key='conv_L')],
        [conversion('Temperature [K]', key='conv_T')],
        [conversion('Acceleration [m/s^2]', key='conv_a')],
        [sg.Button('To Physical Unit'),
         sg.Button('To EMSES Unit')]
    ]
    return sg.Window('変換: Physical unit <=> EMSES unit', layout=layout, location=location)


convs = [
    ('conv_m', lambda u: u.m),
    ('conv_t', lambda u: u.t),
    ('conv_f', lambda u: u.f),
    ('conv_v', lambda u: u.v),
    ('conv_n', lambda u: u.n),
    ('conv_N', lambda u: u.N),
    ('conv_F', lambda u: u.F),
    ('conv_P', lambda u: u.P),
    ('conv_W', lambda u: u.W),
    ('conv_w', lambda u: u.w),
    ('conv_eps', lambda u: u.eps),
    ('conv_q', lambda u: u.q),
    ('conv_rho', lambda u: u.rho),
    ('conv_q_m', lambda u: u.q_m),
    ('conv_I', lambda u: u.i),
    ('conv_J', lambda u: u.J),
    ('conv_phi', lambda u: u.phi),
    ('conv_E', lambda u: u.E),
    ('conv_C', lambda u: u.C),
    ('conv_R', lambda u: u.R),
    ('conv_G', lambda u: u.G),
    ('conv_mu', lambda u: u.mu),
    ('conv_B', lambda u: u.B),
    ('conv_L', lambda u: u.L),
    ('conv_T', lambda u: u.T),
    ('conv_a', lambda u: u.a),
]


def to_emses_unit(window, values, dx, to_c):
    unit = Units(dx=dx, to_c=to_c)
    for key, conv in convs:
        em_key = 'em_{}'.format(key)

        physical_val = float(values[key])
        value = conv(unit).trans(physical_val)

        window[em_key].Update(value=value)


def to_physical_unit(window, values, dx, to_c):
    unit = Units(dx=dx, to_c=to_c)
    for key, conv in convs:
        em_key = 'em_{}'.format(key)

        em_val = float(values[em_key])
        value = conv(unit).reverse(em_val)

        window[key].Update(value=value)
