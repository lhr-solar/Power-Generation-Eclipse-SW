# Custom Imports: GlobalAlgorithm is the base class for the Global PandO, and Voltage Sweep
# is used by the algorithm
"""
GlobalPandO.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 02/06/2021
Last Modified: 02/08/2021

Description: The GlobalPandO algorithm
"""

from ArraySimulation.MPPT.GlobalMPPTAlgo.GlobalAlgorithm import GlobalAlgorithm
from ArraySimulation.MPPT.GlobalMPPTAlgo.VoltageSweep import VoltageSweep


class GlobalPando(GlobalAlgorithm):
    """"""

    def __init__(self, numCells=1, MPPTLocalAlgoType="Default", strideType="Fixed"):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        numCells: int
            The number of cells that should be accounted for in the MPPT
            algorithm.
        MPPTLocalAlgoType: String
            The name of the local MPPT algorithm type.
        strideType: String
            The name of the stride model type.
        """
        super(GlobalPando, self).__init__(numCells, "PandO", strideType)
        self._sweep = VoltageSweep(numCells, MpptAlgoType, strideType)
        self.sweeping = True

    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        vRef = arrVoltage
        if arrVoltage < self.MAX_VOLTAGE and self.sweeping:
            vRef = self._sweep.getReferenceVoltage(
                arrVoltage, arrCurrent, irradiance, temperature
            )
        else:
            self.sweeping = False
            (lBound, rBound) = self._sweep.getBounds()
            if arrVoltage >= self.MAX_VOLTAGE:
                vRef = lBound
            elif arrVoltage == lBound:
                vRef = lBound + 0.02
            else:
                vRef = self._model.getReferenceVoltage(
                    arrVoltage, arrCurrent, irradiance, temperature
                )
        return vRef

    def reset(self):
        self._strideModel.reset()
        self.sweeping = True
        self._sweep.reset()
