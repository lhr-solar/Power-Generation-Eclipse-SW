"""
MPPT.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 02/27/21

Description: Implementation of the MPPT class.
"""
# Library Imports.


# Custom Imports.
from ArraySimulation.MPPT.GlobalMPPTAlgorithms.GlobalMPPTAlgorithm import (
    GlobalMPPTAlgorithm,
)
from ArraySimulation.MPPT.GlobalMPPTAlgorithms.VoltageSweep import VoltageSweep


class MPPT:
    """
    The MPPT (Maximum Power Point Tracker) class is a concrete class
    that manages the data flow and operation of MPPT Algorithms. More properly,
    it is a wrapper class that allows the main program to swap between Global
    and Local MPPT Algorithms and Stride models (see MPPTComponents) on demand.
    """

    def __init__(self):
        self._model = None

    def setupModel(
        self,
        numCells=1,
        MPPTGlobalAlgoType="Default",
        MPPTLocalAlgoType="Default",
        strideType="Fixed",
    ):
        """
        Initializes an internal model object for reference.
        This is called whenever the user wants to switch models or stride
        models.

        Parameters
        ----------
        numCells: int
            Number of cells expected by the MPPT model.
        MPPTGlobalAlgoType: String
            The name of the global MPPT algorithm type.
        MPPTLocalAlgoType: String
            The name of the local MPPT algorithm type.
        strideType: String
            The name of the stride algorithm type.
        """
        # Reset any model if there are any already defined.
        if self._model is not None:
            self.reset()

        if MPPTGlobalAlgoType == "Voltage Sweep":
            self._model = VoltageSweep(numCells, MPPTLocalAlgoType, strideType)
        elif MPPTGlobalAlgoType == "Default":
            self._model = GlobalMPPTAlgorithm(
                numCells, MPPTGlobalAlgoType, MPPTLocalAlgoType, strideType
            )
        else:
            self._model = GlobalMPPTAlgorithm(
                numCells, MPPTGlobalAlgoType, MPPTLocalAlgoType, strideType
            )

    def reset(self):
        """
        Resets the internally set MPPT and its relevant Stride Model.
        """
        if self._model is not None:
            self._model.reset()

    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        return self._model.getReferenceVoltage(
            arrVoltage, arrCurrent, irradiance, temperature
        )

    def getGlobalMPPTType(self):
        """
        Returns the Global MPPT type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._model.getGlobalMPPTType()

    def getLocalMPPTType(self):
        """
        Returns the Local MPPT type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._model.getLocalMPPTType()

    def getStrideType(self):
        """
        Returns the Stride model type used for the simulation.

        Return
        ------
        String: Stride type name.
        """
        return self._model.getStrideType()
