"""_summary_
@file       ModifiedThreeParameterPVCell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Concrete class modeling the single diode model with modifications.
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

sys.path.extend([".."])

from common.graph import Graph


class ModifiedThreeParameterPVCell(PVCell):
    def __init__(self, geometry, parameters, cell_data_fp=None) -> None:
        super().__init__(geometry, parameters, cell_data_fp=cell_data_fp)

    def get_current(self, voltage, irradiance, temperature):
        if voltage == 0.0:
            raise Exception("Load voltage is too low!")
        if irradiance == 0.0:
            raise Exception("Incident irradiance is too low!")
        if temperature == 0.0:
            raise Exception("Cell temperature is too low!")

        # Reference parameters
        g_ref = self.parameters["reference_irrad"]
        t_ref = self.parameters["reference_temp"]
        v_oc_ref = self.parameters["reference_voc"]
        i_sc_ref = self.parameters["reference_isc"]

        # Curve Fitting parameters
        n = self.parameters["ideality_factor"]
        alpha = self.parameters["isc_thermal_coeff"]
        beta = self.parameters["voc_thermal_coeff"]
        gamma = self.parameters["vt_modifier_coeff"]

        if n == 0.0:
            raise Exception("Cell ideality factor is too low!")

        g = irradiance
        t = temperature
        v = voltage

        # Thermal voltage
        v_t = n * PVCell.k_b * t / PVCell.q  # 26mV

        # Short circuit current
        i_sc = i_sc_ref * g / g_ref * (1 - alpha * (t_ref - t))

        # Open circuit voltage
        v_t_mod = n * PVCell.k_b * (t_ref + t / gamma) / PVCell.q
        v_oc = v_oc_ref * (1 - beta * (t_ref - t)) + v_t_mod * m.log(g / g_ref)

        # Dark/reverse saturation current
        i_0 = i_sc / (m.exp(v_oc / v_t) - 1)

        # Dark/diode current
        i_d = i_0 * (m.exp(v / v_t) - 1)

        # Photocurrent
        i_pv = i_sc

        # Load current
        i_l = i_pv - i_d

        return i_l

    def visualize_sweep(
        self,
        ref=None,
        ideality_range=None,
        isc_therm_coeff_range=None,
        voc_therm_coeff_range=None,
        vt_mod_coeff_range=None,
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
        }

        if ideality_range is not None:
            graphs["ideality_factor"]["range"] = ideality_range
        if isc_therm_coeff_range is not None:
            graphs["isc_thermal_coeff"]["range"] = isc_therm_coeff_range
        if voc_therm_coeff_range is not None:
            graphs["voc_thermal_coeff"]["range"] = voc_therm_coeff_range
        if vt_mod_coeff_range is not None:
            graphs["vt_modifier_coeff"]["range"] = vt_mod_coeff_range

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
        "reference_voc": 0.587,  # Volts
        "reference_isc": 6.15,  # Amps
        "ideality_factor": 2.00,
        "isc_thermal_coeff": 0,
        "voc_thermal_coeff": 0,
        "vt_modifier_coeff": 100,
    }

    # Instantiate a new Cell under this model.
    cell = ModifiedThreeParameterPVCell(
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
