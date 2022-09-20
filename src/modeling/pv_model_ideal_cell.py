"""_summary_
@file       pv_model_ideal_cell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Modelling an ideal solar cell.
@version    0.0.0
@date       2022-09-17
"""

from math import e
import numpy as np


class PVModelIdealCell:
    q = 1.602 * (10**-19)  # Coulombs
    k = 1.381 * (10**-23)  # J/K

    def __init__(self, v_oc, i_sc, area):
        """_summary_

        Args:
            v_oc (float): mV
            i_sc (float): mA
            area (float): cm^2
        """
        self.v_oc = v_oc
        self.i_sc = i_sc
        self.area = area

    def model_name():
        return "Ideal Solar Cell Model"

    def solve_model_conditions(self, voltage, irradiance, temperature):
        V = voltage
        G = irradiance
        # Convert temperature from Celsius into Kelvin.
        T = temperature + 273.15

        # Modify v_oc relative to temperature and irradiance.
        # We assume that there is no change to v_oc due to temp and irrad.
        v_oc = self.v_oc

        # Modify i_sc relative to temperature and irradiance.
        # We assume that there is no change to i_sc due to temp and irrad.
        i_sc = self.i_sc

        # J(V) = J_PV - J_D(V)
        # Assume J_PV = J_SC.

        # Short circuit current density.
        # J_SC (mA/cm^2) = I_SC (mA) / area (cm^2)
        j_sc = self.i_sc / self.area

        # Dark saturation current density.
        # J_0 = J_SC / (e^(qV_oc/kT) - 1) (mA/cm^2)
        j_0 = j_sc / (
            e ** ((PVModelIdealCell.q * self.v_oc) / (PVModelIdealCell.k * T)) - 1
        )

        # Dark current density.
        # J_D(V) = J_0 (e^(qV/kT) - 1) (mA/cm^2)
        j_d = j_0 * (e ** ((PVModelIdealCell.q * V) / (PVModelIdealCell.k * T)) - 1)

        # Current density.
        j = j_sc - j_d

        # Current.
        # i (mA) = j (mA/cm^2) * area (cm^2)
        i = j * self.area

        return i

    def generate_model(self):
        entries = ["Voltage (V)", "Irrad (G)", "Temp (C)", "Current (A)"]
        for voltage in np.arange(0, self.v_oc + 0.01, 0.01):
            for irradiance in np.arange(0, 1501, 100):
                for temperature in np.arange(0, 51, 5):
                    entries.append(
                        [
                            voltage,
                            irradiance,
                            temperature,
                            self.solve_model_conditions(
                                voltage, irradiance, temperature
                            ),
                        ]
                    )
        for entry in entries:
            print(entry)
        return entries

    def save_model(self, model):
        pass
