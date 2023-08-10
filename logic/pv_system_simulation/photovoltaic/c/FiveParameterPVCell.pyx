"""_summary_
$ python setup.py build_ext --inplace
"""

import math as m
from scipy import constants

cdef float k_b = constants.k
cdef float q = constants.e

def get_current(
    float g,
    float t,
    float v,
    float g_ref,
    float t_ref,
    float v_oc_ref,
    float i_sc_ref,
    float r_s_ref,
    float r_sh_ref,
    float n
):
    # Series and shunt resistance
    cdef float r_s = r_s_ref
    cdef float r_sh = r_sh_ref

    # Thermal voltage
    cdef float v_t = n * k_b * t / q  # 26mV

    # Short circuit current
    cdef float i_sc = i_sc_ref * g / g_ref

    # Open circuit voltage
    cdef float v_oc = v_oc_ref + v_t * m.log(g / g_ref + 1)

    # Photocurrent
    cdef float i_pv = i_sc

    # Dark/reverse saturation current
    cdef float i_0 = i_sc / (m.exp(v_oc / v_t) - 1)

    # Setup
    cdef float prediction = 0.0
    cdef float new_l1_loss = 0.0
    cdef float travel_speed = 0.01
    cdef float margin = 0.01

    # Calculate seed output
    # Dark/diode current
    cdef float i_d = i_0 * (m.exp((v + prediction * r_s) / v_t) - 1)

    # Shunt current
    cdef float i_sh = (v + prediction * r_s) / r_sh

    # Load current
    cdef float reality = i_pv - i_d - i_sh

    cdef float l1_loss = abs(reality - prediction)

    while True:
        # Make a new prediction.
        prediction += travel_speed

        # Dark/diode current
        i_d = i_0 * (m.exp((v + prediction * r_s) / v_t) - 1)

        # Shunt current
        i_sh = (v + prediction * r_s) / r_sh

        # Load current
        reality = i_pv - i_d - i_sh

        # Calculate new L1 loss and determine whether to continue.
        new_l1_loss = abs(reality - prediction)
        is_stable = True
        if new_l1_loss + margin < l1_loss:
            # If we're going in the right direction, keep going.
            l1_loss = new_l1_loss
            is_stable = False
        elif new_l1_loss > l1_loss + margin:
            # If we're going in the wrong direction, back up.
            travel_speed = -travel_speed
            is_stable = False
        else:
            # If we're stagnant, give up.
            travel_speed = 0.0

        if is_stable:
            break

    return prediction
