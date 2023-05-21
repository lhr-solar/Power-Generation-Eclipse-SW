"""_summary_
@file       ModifiedFiveParameterPVCell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Concrete class modeling the complete single diode model with modifications.
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
from c.ModifiedFiveParameterPVCell import get_current


class ModifiedFiveParameterPVCell(PVCell):
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
        alpha = self.parameters["isc_thermal_coeff"]
        beta = self.parameters["voc_thermal_coeff"]
        gamma = self.parameters["vt_modifier_coeff"]

        theta = self.parameters["rs_thermal_coeff"]
        tau = self.parameters["rs_irrad_coeff"]
        omega = self.parameters["rsh_thermal_coeff"]
        zeta = self.parameters["rsh_irrad_coeff"]

        if n == 0.0:
            raise Exception("Cell ideality factor is too low!")

        # # Series resistance
        # r_s = r_s_ref * m.exp(theta * (t_ref - t)) * (1 + tau * (g_ref - g))

        # # Shunt resistance
        # r_sh = r_sh_ref * m.exp(omega * (t_ref - t)) * (1 + zeta * (g_ref - g))

        # # Thermal voltage
        # v_t = n * PVCell.k_b * t / PVCell.q  # 26mV

        # # Short circuit current
        # i_sc = i_sc_ref * g / g_ref * (1 - alpha * (t_ref - t))

        # # Open circuit voltage
        # v_t_mod = n * PVCell.k_b * (t_ref + t / gamma) / PVCell.q
        # v_oc = v_oc_ref * (1 - beta * (t_ref - t)) + v_t_mod * m.log(g / g_ref)

        # # Photocurrent
        # i_pv = i_sc * (r_s + r_sh) / r_sh

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
            g,
            t,
            v,
            g_ref,
            t_ref,
            v_oc_ref,
            i_sc_ref,
            r_s_ref,
            r_sh_ref,
            n,
            alpha,
            beta,
            gamma,
            theta,
            tau,
            omega,
            zeta,
        )

    def visualize_sweep(
        self,
        ref=None,
        ideality_range=None,
        isc_therm_coeff_range=None,
        voc_therm_coeff_range=None,
        vt_mod_coeff_range=None,
        rs_therm_coeff_range=None,
        rs_irrad_coeff_range=None,
        rsh_therm_coeff_range=None,
        rsh_irrad_coeff_range=None,
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
            },
            "isc_thermal_coeff": {
                "title": "I_SC Thermal Coeff Sweep (%/K)",
                "widget": None,
                "range": [-0.1, 0.1, 0.001],
                "cur_val": 0.0,
                "position": [1, 1],
            },
            "voc_thermal_coeff": {
                "title": "V_OC Thermal Coeff Sweep (%/K)",
                "widget": None,
                "range": [-0.1, 0.1, 0.001],
                "cur_val": 0.0,
                "position": [2, 0],
            },
            "vt_modifier_coeff": {
                "title": "V_t Coeff Sweep",
                "widget": None,
                "range": [1.0, 100.0, 0.1],
                "cur_val": 1.0,
                "position": [2, 1],
            },
            "rs_thermal_coeff": {
                "title": "R_S Thermal Coeff Sweep",
                "widget": None,
                "range": [-0.1, 0.1, 0.001],
                "cur_val": 0.0,
                "position": [3, 0],
            },
            "rs_irrad_coeff": {
                "title": "R_S Irradiance Coeff Sweep",
                "widget": None,
                "range": [-0.1, 0.1, 0.001],
                "cur_val": 0.0,
                "position": [3, 1],
            },
            "rsh_thermal_coeff": {
                "title": "R_SH Thermal Coeff Sweep",
                "widget": None,
                "range": [-0.1, 0.1, 0.001],
                "cur_val": 0.0,
                "position": [4, 0],
            },
            "rsh_irrad_coeff": {
                "title": "R_SH Irradiance Coeff Sweep",
                "widget": None,
                "range": [-0.1, 0.1, 0.001],
                "cur_val": 0.0,
                "position": [4, 1],
            },
        }

        if ideality_range is not None:
            graphs["ideality_factor"]["range"] = ideality_range
        if isc_therm_coeff_range is not None:
            graphs["isc_thermal_coeff"]["range"] = isc_therm_coeff_range
        if voc_therm_coeff_range is not None:
            graphs["voc_thermal_coeff"]["range"] = voc_therm_coeff_range
        if vt_mod_coeff_range is not None:
            graphs["vt_modifier_coeff"]["range"] = vt_mod_coeff_range
        if rs_therm_coeff_range is not None:
            graphs["rs_thermal_coeff"]["range"] = rs_therm_coeff_range
        if rs_irrad_coeff_range is not None:
            graphs["rs_irrad_coeff"]["range"] = rs_irrad_coeff_range
        if rsh_therm_coeff_range is not None:
            graphs["rsh_thermal_coeff"]["range"] = rsh_therm_coeff_range
        if rsh_irrad_coeff_range is not None:
            graphs["rsh_irrad_coeff"]["range"] = rsh_irrad_coeff_range

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
        "isc_thermal_coeff": 0,
        "voc_thermal_coeff": 0,
        "vt_modifier_coeff": 100,
        "rs_thermal_coeff": 0,
        "rs_irrad_coeff": 0,
        "rsh_thermal_coeff": 0,
        "rsh_irrad_coeff": 0,
    }

    # Instantiate a new Cell under this model.
    cell = ModifiedFiveParameterPVCell(
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
    cell.visualize_sweep(
        ref=ref,
    )
