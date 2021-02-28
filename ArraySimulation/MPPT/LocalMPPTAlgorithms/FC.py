"""
FC.py

Author: Afnan Mir, Matthew Yu (2021).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 02/27/2021

Description: Implementation of the dP/dV feedback control D&C algorithm.
"""
from ArraySimulation.MPPT.LocalMPPTAlgorithms.LocalMPPTAlgorithm import (
    LocalMPPTAlgorithm,
)


class FC(LocalMPPTAlgorithm):
    """
    The FC class is a derived class of LocalMPPTAlgorithm, utilizing the change
    of power and change of voltage over time to determine the direction of
    movement and stride of the next reference voltage. It belongs to the
    classification of hill climbing algorithms.
    """

    # Error tuning parameter.
    error = 0.05

    def __init__(self, numCells=1, strideType="Fixed"):
        super(FC, self).__init__(numCells, "FC", strideType)

    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        arrPower = arrCurrent * arrVoltage
        dP = arrPower - self.pOld
        dV = arrVoltage - self.vOld
        stride = self._strideModel.getStride(
            arrVoltage, arrCurrent, irradiance, temperature
        )
        vRef = arrVoltage
        if dV == 0:  # Prevent divide by 0 issues.
            vRef += 0.005
        elif abs(dP / dV) < FC.error:
            pass
        else:
            if dP / dV > 0:
                vRef += stride
            else:
                vRef -= stride
        self.vOld = arrVoltage
        self.iOld = arrCurrent
        self.pOld = arrVoltage * arrCurrent
        return vRef
