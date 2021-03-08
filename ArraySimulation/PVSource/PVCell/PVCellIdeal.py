"""
PVCellIdeal.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 11/26/20

Description: Derived class of PVCell that implements an ideal model tuned to
the Sunpower Maxeon III Bin Le1 solar cells.
"""
# Library Imports.
from math import exp, pow, e
from numpy import log as ln

# Custom Imports.
from ArraySimulation.PVSource.PVCell.PVCell import PVCell


class PVCellIdeal(PVCell):
    """
    Derived class of PVCell that implements an ideal model tuned to the Sunpower
    Maxeon III Bin Le1 solar cells.
    """

    def __init__(self, useLookup=True):
        super(PVCellIdeal, self).__init__(useLookup)

    def getCurrent(self, numCells=1, voltage=0, irradiance=0.001, temperature=0):
        # TODO: numCells here may be abused and should be revised.

        # Ideal single diode model.
        cellTemperature = temperature + 273.15  # Convert cell temperature into kelvin.

        # Suppres divide by 0s from voltage and irradiance.
        if voltage == 0.0:
            voltage = 0.001
        if irradiance == 0.0:
            irradiance = 0.001

        # Short circuit current.
        SCCurrent = (
            irradiance
            / self.refIrrad
            * self.refSCCurrent
            * (1 + 6e-4 * (cellTemperature - self.refTemp))
        )

        # Open circuit voltage.
        OCVoltage = (
            self.refOCVoltage
            - 2.2e-3 * (cellTemperature - self.refTemp)
            + numCells
            * self.k
            * cellTemperature
            / self.q
            * ln(irradiance / self.refIrrad)
        )

        # Photovoltatic current.
        PVCurrent = SCCurrent

        # Reverse saturation current, or dark saturation current.
        revSatCurrent = exp(
            ln(SCCurrent) - self.q * OCVoltage / (self.k * cellTemperature)
        )

        # Diode current.
        diodeCurrent = PVCurrent
        if voltage <= numCells * OCVoltage:
            diodeCurrent = revSatCurrent * (
                exp(self.q * voltage / (numCells * self.k * cellTemperature)) - 1
            )

        # Output current.
        current = PVCurrent - diodeCurrent

        return current

    def getModelType(self):
        return "Ideal"
