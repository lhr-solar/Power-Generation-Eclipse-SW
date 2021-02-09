"""
VoltageSweep.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 02/06/2021
Last Modified: 02/08/2021

Description: The Voltage Sweep class is a derived concrete class of
GlobalAlgorithm implementing the Voltage Sweep algorithm. It increments through
the range of all possible voltage values (the "sweep"), finding all local maxima
of the P-V curve. It then identifies the global maxima using a LocalMPPTAlgorithm.
"""
# Library Imports.


# Custom Imports.
from ArraySimulation.MPPT.GlobalMPPTAlgorithms.GlobalMPPTAlgorithm import (
    GlobalMPPTAlgorithm,
)


class VoltageSweep(GlobalMPPTAlgorithm):
    """
    The Voltage Sweep class is a derived concrete class of GlobalAlgorithm
    implementing the Voltage Sweep algorithm. It increments through the range of
    all possible voltage values (the "sweep"), finding all local maxima of the
    P-V curve. It then identifies the global maxima using a LocalMPPTAlgorithm.
    """

    def __init__(self, numCells=1, MPPTLocalAlgoType="Default", strideType="Fixed"):
        super(VoltageSweep, self).__init__(
            numCells, "Voltage Sweep", MPPTLocalAlgoType, strideType
        )

        # Stores all the voltage values of the local maxima.
        self.voltage_peaks = [0]

        # Stores the power values of the local maxima.
        self.power_peaks = [0]

        # Whether we are in sweeping mode or not.
        self.sweeping = True

        # Checks to see if we were increasing before.
        self.increasing = True

        self.stride = 0.01
        self.vOld = 0.0
        self.iOld = 0.0
        self.tOld = 0.0
        self.irrOld = 0.0
        self.pOld = 0.0

    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        vRef = arrVoltage
        if arrVoltage < self.MAX_VOLTAGE and self.sweeping:
            vRef = self._sweep(arrVoltage, arrCurrent, irradiance, temperature)
        else:
            self.sweeping = False
            (lBound, rBound) = self._getBounds()
            if arrVoltage >= self.MAX_VOLTAGE:
                vRef = lBound
            elif arrVoltage == lBound:
                vRef = lBound + 0.02
            else:
                vRef = self._model.getReferenceVoltage(
                    arrVoltage, arrCurrent, irradiance, temperature
                )
        return vRef

    def _sweep(self, arrVoltage, arrCurrent, irradiance, temperature):
        """
        Calculates the reference voltage output for the given PVSource input.
        May use prior history.

        Parameters
        ----------
        arrVoltage: float
            Array voltage in V.
        arrCurrent: float
            Array current in A.
        irradiance: float
            Irradiance in W/M^2 (G)
        temperature: float
            Cell Temperature in C.

        Return
        ------
        float: The reference voltage that should be applied to the array in the
        next cycle.
        """
        pIn = arrVoltage * arrCurrent
        vRef = arrVoltage
        if arrVoltage >= 0.80:
            return 0.80
        if pIn < self.pOld and self.increasing:
            self.voltage_peaks.append(self.vOld)
            self.power_peaks.append(self.pOld)
            self.increasing = False
        elif pIn > self.pOld and not self.increasing:
            self.increasing = True
        vRef += self.stride
        self.iOld = arrCurrent
        self.vOld = arrVoltage
        self.pOld = arrCurrent * arrVoltage
        self.tOld = temperature
        self.irrOld = irradiance
        return vRef

    def _getBounds(self):
        """
        Finds left and right bounds for the global maximum of the P-V curve.

        Parameters
        ----------
        None

        Return
        ------
        The left and right bounds for the global maximum of the P-V curve.
        """
        maxPower = max(self.power_peaks)
        maxVoltage = self.voltage_peaks[self.power_peaks.index(maxPower)]
        (leftBound, rightBound) = (
            maxVoltage - 0.1,
            maxVoltage + 0.1,
        )  # 0.1 is a placeholder for now. Will probably have to be some factor of the max voltage
        return (leftBound, rightBound)

    def reset(self):
        super(VoltageSweep, self).reset()
        self.stride = 0.01
        self.voltage_peaks = [0]
        self.power_peaks = [0]
        self.sweeping = True
        self.increasing = True
