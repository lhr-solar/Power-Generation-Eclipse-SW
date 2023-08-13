"""
PVCell.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 11/24/20

Description: The PVCell (Photovoltaic Cell) class is a concrete base class that
provides a common API for derived classes to use. The PVCell class enables users
to retrieve information of the PVCell model, such as IV curves, maximum power
points, and so on given a set of input conditions.
"""
# Library Imports.
import numpy as np

# Custom Imports.


class PVCell:
    """
    The PVCell (Photovoltaic Cell) class is a concrete base class that provides
    a common API for derived classes to use. The PVCell class enables users to
    retrieve information of the PVCell model, such as IV curves, maximum power
    points, and so on given a set of input conditions.
    """

    # The upper voltage bound that should be tested by any model. We expect the
    # cell to always be at open circuit voltage at this point.
    MAX_CELL_VOLTAGE = 0.8

    # Minimum allowed resolution step for voltage.
    MIN_RESOLUTION = 0.001

    # Reference values for the models.
    refIrrad = 1000  # Reference Cell Irradiance (W/M^2).
    refTemp = 25 + 273.15  # Reference Cell Temperature (Celsius -> Kelvin).
    refSCCurrent = 6.15  # Reference Short Circuit Current (A).
    refOCVoltage = 0.721  # Reference Open Circuit Voltage (V).
    k = 1.381e-23  # Boltzmann's constant (J/K).
    q = 1.602e-19  # Electron charge (C).

    def __init__(self, useLookup=True):
        """
        Sets up the initial cell parameters.
        """
        # Note that these two are experimental value and depend on irradiance, ergo
        # should actually be a lookup table in the future.
        self.rSeries = 0.032  # Predicted Cell series resistance (Ohms).
        self.rShunt = 36.1  # Predicted Cell shunt resistance (Ohms).

        # Controls whether each cell in a model calculates its current using a
        # lookup table or not.
        self._useLookup = useLookup

    def getCurrent(self, numCells=1, voltage=0, irradiance=0.001, temperature=0):
        """
        Calculates and returns the cell model current given various
        environmental parameters.

        Parameters
        ----------
        numCells: int
            Number of cells in the model.
        voltage: float
            Voltage across the cell. Restricted to MAX_VOLTAGE.
        irradiance: float
            Irradiance on the cell. In W/M^2.
        temperature: float
            Cell surface temperature. In degrees Celsius.

        Returns
        -------
        float: current of the cell model.
        """
        return -1

    def getCurrentLookup(self, numCells=1, voltage=0, irradiance=0.001, temperature=0):
        """
        Looks up the cell model current given various environmental parameters.
        Guaranteed blazing fast speed. Requires a minimum resolution for various
        parameters, depending on the model. Anything smaller will have its
        resolution truncated.

        Parameters
        ----------
        numCells: int
            Number of cells in the model.
        voltage: float
            Voltage across the cell. Restricted to MAX_VOLTAGE.
        irradiance: float
            Irradiance on the cell. In W/M^2.
        temperature: float
            Cell surface temperature. In degrees Celsius.

        Returns
        -------
        float: current of the cell model.
        """
        return self.getCurrent(numCells, voltage, irradiance, temperature)

    def getCellIV(self, numCells=1, resolution=0.01, irradiance=0.001, temperature=0):
        """
        Calculates the entire cell model current voltage plot given various
        environmental parameters.

        Parameters
        ----------
        numCells: int
            Number of cells in the model.
        resolution: float
            Voltage stride across the cell. Occurs within the bounds of [0,
            MAX_VOLTAGE], inclusive.
        irradiance: float
            Irradiance on the cell. In W/M^2.
        temperature: float
            Cell surface temperature. In degrees Celsius.

        Returns
        -------
        list: [(voltage:float, current:float), ...]
            A list of paired voltage|current tuples across the cell IV curve.
        Throws an exception for undefined cell models or negative current
            outputs.

        Assumptions
        -----------
        The IV curve of the cell has a short circuit current of 0A by MAX_VOLTAGE.
        """
        model = []
        if resolution <= 0:
            resolution = self.MIN_RESOLUTION

        for voltage in np.arange(
            0.0, self.MAX_CELL_VOLTAGE * numCells + resolution, resolution
        ):
            current = 0
            if self._useLookup:
                current = self.getCurrentLookup(
                    numCells, voltage, irradiance, temperature
                )
            else:
                current = self.getCurrent(numCells, voltage, irradiance, temperature)
            if current >= 0.0:
                model.append(
                    (round(voltage, 2), round(current, 3))
                )  # TODO: this rounding should be a function of resolution
            else:
                raise Exception("Negative current output from the model: ", current)

        return model

    def getCellEdgeCharacteristics(
        self, numCells=1, resolution=0.001, irradiance=0.001, temperature=0
    ):
        """
        Calculates the cell model edge characteristics given various
        environmental parameters.

        Parameters
        ----------
        numCells: int
            Number of cells in the model.
        resolution: float
            Voltage stride across the cell. Occurs within the bounds of [0,
            MAX_VOLTAGE], inclusive.
        irradiance: float
            Irradiance on the cell. In W/M^2.
        temperature: float
            Cell surface temperature. In degrees Celsius.

        Returns
        -------
        tuple: (V_OC:float, I_SC:float, (V_MPP:float, I_MPP:float)):
            A tuple of tuples indicating the open circuit voltage, the short
            circuit current, and the maximum power point (MPP) voltage and current.
        Throws an exception for undefined cell models or negative current
            outputs.

        Assumptions
        -----------
        We assume that a single solar cell is always a unimodal function and
        thus only return a single tuple. In the case of a multi module model, we
        cannot assume this (due to shading creating local MPPs), but that is
        handled in the PVSource class.
        """
        mpp = (0, 0)  # voltage, current list
        OCVoltage = 0.0

        if resolution <= 0:
            resolution = self.MIN_RESOLUTION

        model = self.getCellIV(numCells, resolution, irradiance, temperature)

        if model != []:
            SCCurrent = model[0][1]  # Current in first entry

            for (voltage, current) in model:
                if mpp[0] * mpp[1] < voltage * current:
                    mpp = (voltage, current)
                if OCVoltage != 0.0 and current == 0:
                    OCVoltage = voltage

            return (OCVoltage, SCCurrent, mpp)
        else:
            return (0, 0, (0, 0))

    def getModelType(self):
        """
        Returns the name of the model.

        Returns
        -------
        string: Model name.
        """
        return "Default"
