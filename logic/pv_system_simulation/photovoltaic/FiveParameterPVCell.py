"""_summary_
@file       FiveParameterPVCell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Concrete class modeling the complete single diode model.
@version    0.4.0
@date       2023-05-17
"""
import math as m
import sys

import numpy as np
import pandas as pd
import pyqtgraph as pg
import similaritymeasures
from PVCell import PVCell
from PySide6 import QtWidgets

sys.path.extend([".s"])

from common.graph import Graph
from c.FiveParameterPVCell import get_current


class FiveParameterPVCell(PVCell):
    def __init__(self, geometry, parameters, cell_data_fp=None) -> None:
        super().__init__(geometry, parameters, cell_data_fp=cell_data_fp)

    def get_current(self, voltage, irradiance, temperature):
        if voltage == 0.0:
            raise Exception("Load voltage is too low!")
        if irradiance == 0.0:
            raise Exception("Incident irradiance is too low!")
        if temperature == 0.0:
            raise Exception("Cell temperature is too low!")

        g = irradiance
        t = temperature
        v = voltage

        # Reference parameters
        g_ref = self.parameters["reference_irrad"]
        t_ref = self.parameters["reference_temp"]
        v_oc_ref = self.parameters["reference_voc"]
        i_sc_ref = self.parameters["reference_isc"]
        r_s_ref = self.parameters["reference_rs"]
        r_sh_ref = self.parameters["reference_rsh"]

        # Curve Fitting parameters
        n = self.parameters["ideality_factor"]

        if n == 0.0:
            raise Exception("Cell ideality factor is too low!")

        # # Series resistance
        # r_s = r_s_ref

        # # Shunt resistance
        # r_sh = r_sh_ref

        # # Thermal voltage
        # v_t = n * PVCell.k_b * t / PVCell.q  # 26mV

        # # Short circuit current
        # i_sc = i_sc_ref * g / g_ref

        # # Open circuit voltage
        # v_oc = v_oc_ref + v_t * m.log(g / g_ref + 1)

        # # Photocurrent
        # i_pv = i_sc

        # # Dark/reverse saturation current
        # i_0 = i_sc / (m.exp(v_oc / v_t) - 1)

        # def get_i_l(i_l):
        #     try:
        #         # Dark/diode current
        #         i_d = i_0 * (m.exp((v + i_l * r_s) / v_t) - 1)

        #         # Shunt current
        #         i_sh = (v + i_l * r_s) / r_sh

        #         # Load current
        #         i_l = i_pv - i_d - i_sh
        #     except:
        #         print(i_l)
        #         print(v + i_l * r_s)
        #         print(v_t)
        #         print(m.exp((v + i_l * r_s) / v_t))
        #         sys.exit(0)

        #     return i_l

        # travel_speed = 0.01
        # margin = 0.01

        # prediction = 0.01
        # reality = get_i_l(prediction)
        # l1_loss = abs(reality - prediction)
        # while True:
        #     # 8. Make a new prediction.
        #     prediction += travel_speed
        #     reality = get_i_l(prediction)

        #     # 9. Calculate new L1 loss and determine whether to continue.
        #     new_l1_loss = abs(reality - prediction)
        #     is_stable = True
        #     if new_l1_loss + margin < l1_loss:
        #         # If we're going in the right direction, keep going.
        #         l1_loss = new_l1_loss
        #         is_stable = False
        #     elif new_l1_loss > l1_loss + margin:
        #         # If we're going in the wrong direction, back up.
        #         travel_speed = -travel_speed
        #         is_stable = False
        #     else:
        #         # If we're stagnant, give up.
        #         travel_speed = 0.0

        #     if is_stable:
        #         break

        # return prediction

        return get_current(
            g, t, v, g_ref, t_ref, v_oc_ref, i_sc_ref, r_s_ref, r_sh_ref, n
        )

    def visualize_sweep(
        self,
        ref=None,
        ideality_range=None,
        irradiance_range=None,
        temperature_range=None,
        return_widget=False,
    ):
        graphs = {
            "ideality_factor": {
                "title": "Ideality Factor Sweep",
                "widget": None,
                "range": [1.0, 2.0, 0.01],
                "cur_val": 1.0,
                "position": [1, 0],
            }
        }

        if ideality_range is not None:
            graphs["ideality_factor"]["range"] = ideality_range

        return super().visualize_sweep(
            graphs=graphs,
            ref=ref,
            irradiance_range=irradiance_range,
            temperature_range=temperature_range,
            return_widget=return_widget,
        )


if __name__ == "__main__":
    geometry = {
        "cell_width": 0.125,  # Meters
        "cell_length": 0.125,  # Meters
        "cell_area": 0.0153,  # Meters ^ 2
    }

    parameters = {
        "reference_irrad": 1000,  # Watts per Meters ^ 2
        "reference_temp": 298.15,  # Kelvin
        "reference_voc": 0.605,  # Volts
        "reference_isc": 6.15,  # Amps
        "reference_rs": 0.022,  # Ohms
        "reference_rsh": 15,  # Ohms
        "ideality_factor": 1.60,
    }

    # Instantiate a new Cell under this model.
    cell = FiveParameterPVCell(
        geometry, parameters, cell_data_fp="photovoltaic/rp_test.log"
    )
    cell.visualize_cell(367.5, 298.15)

    ref = {
        "v_mpp": 0.621,
        "i_mpp": 5.84,
        "p_mpp": 3.63,
        "v_range": [0, 0.721],
        "i_range": [0, 6.15],
        "p_range": [0, 3.63],
    }
    cell.visualize_sweep(ref=ref)
