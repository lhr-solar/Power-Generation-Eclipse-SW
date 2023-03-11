"""
PVCellNonideal.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 11/26/20

Description: Derived class of PVCell that implements an nonideal model tuned to
the Sunpower Maxeon III Bin Le1 solar cells.

TODO: Implement number of cells in output.
"""
# Library Imports.
from math import exp, pow, e
from numpy import log as ln
import numpy as np


# Custom Imports.
from ArraySimulation.PVSource.PVCell.PVCell import PVCell
from ArraySimulation.PVSource.PVCell.Lookup import Lookup


class PVCellNonideal(PVCell):
    """
    Derived class of PVCell that implements an nonideal model tuned to the Sunpower
    Maxeon III Bin Le1 solar cells.
    """

    def __init__(self, useLookup=True):
        super(PVCellNonideal, self).__init__(useLookup)

        # Lookup object built from the provided file name sourced from
        # /External.
        self._lookup = Lookup(fileName="NonidealCellLookup.csv")
        self._lookup.readFile()

    def getCurrent(self, numCells=1, voltage=0, irradiance=0.001, temperature=0):
        # TODO: numCells here may be abused and should be revised.

        # Nonideal single diode model.
        cellTemperature = temperature + 273.15  # Convert cell temperature into kelvin.

        # Short circuit current.
        SCCurrent = (
            irradiance
            / PVCell.refIrrad
            * PVCell.refSCCurrent
            * (1 + 6e-4 * (cellTemperature - PVCell.refTemp))
        )

        # Open circuit voltage.
        OCVoltage = (
            PVCell.refOCVoltage
            - 2.2e-3 * (cellTemperature - PVCell.refTemp)
            + PVCell.k * cellTemperature / PVCell.q * ln(irradiance / PVCell.refIrrad)
        )

        # Photovoltatic current.
        PVCurrent = SCCurrent

        # Reverse saturation current, or dark saturation current.
        revSatCurrent = exp(
            ln(SCCurrent) - PVCell.q * OCVoltage / (PVCell.k * cellTemperature)
        )

        # Iteratively solve for the implicit parameter.
        currentPrediction = 0
        left = currentPrediction

        # Diode current.
        diodeCurrent = (
            revSatCurrent
            * (
                exp(
                    PVCell.q
                    * (voltage + currentPrediction * self.rSeries)
                    / (PVCell.k * cellTemperature)
                )
                - 1
            )
            - (voltage + currentPrediction * self.rSeries) / self.rShunt
        )
        right = PVCurrent - diodeCurrent

        difference = (left - right) ** 2
        decreasing = True

        while decreasing:
            currentPrediction += 0.001
            left = currentPrediction

            diodeCurrent = (
                revSatCurrent
                * (
                    exp(
                        PVCell.q
                        * (voltage + currentPrediction * self.rSeries)
                        / (PVCell.k * cellTemperature)
                    )
                    - 1
                )
                - (voltage + currentPrediction * self.rSeries) / self.rShunt
            )
            right = PVCurrent - diodeCurrent

            # If my difference change has flipped signs, I'm done.
            if (difference - (left - right) ** 2) <= 0.0:
                decreasing = False
            difference = (left - right) ** 2

        return currentPrediction

    def getCurrentLookup(self, numCells=1, voltage=0, irradiance=0.001, temperature=0):
        """
        Guaranteed to be at least a dozen times faster than getCurrent. However,
        we need to be able to generate the lookup table from the original, which
        means if you decide to use this method, at some point you'll need to
        spend a cozy 5-10 minutes building the massive lookup table.
        """
        return self._lookup.lookup([voltage, irradiance, temperature])[0]

    def buildCurrentLookup(
        self,
        fileName="NonidealCellLookup2.csv",
        voltageRes=0.01,
        irradianceRes=50,
        temperatureRes=0.5,
    ):
        """
        Using our model and a specified resolution, we'll build up the lookup
        table. Note that the defaults are recommended (<3 min) and shrinking the
        resolutions further nonlinearly increases the process time.

        Also, make sure that the resolutions are in .1, .2, or .5 increments.

        Parameters
        ----------
        voltageRes: float
            Voltage resolution step.
        irradianceRes: float
            Irradiance resolution step.
        temperatureRes: float
            Temperature resolution step.
        """
        lookup = Lookup(fileName=fileName)
        for voltage in np.arange(0.00, 0.80 + voltageRes, voltageRes):
            for irradiance in np.arange(0.00, 1000 + irradianceRes, irradianceRes):
                for temperature in np.arange(0.00, 80 + temperatureRes, temperatureRes):
                    # TODO: test to see if irrad, temp = 0 breaks the model.
                    current = self.getCurrent(1, voltage, irradiance, temperature)
                    lookup.addLine(
                        [
                            round(voltage, 3),
                            round(irradiance, 3),
                            round(temperature, 3),
                            round(current, 3),
                        ]
                    )

        lookup.writeFile()
        lookup.readFile()
        self._lookup = lookup

    def getModelType(self):
        return "Nonideal"
