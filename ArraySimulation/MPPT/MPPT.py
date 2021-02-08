"""
MPPT.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 2/8/21

Description: The MPPT (Maximum Power Point Tracker) class is a concrete class
that manages the data flow and operation of MPPT Algorithms. More properly, it
is a wrapper class that allows the main program to swap between MPPT Algorithms
and Stride models (see MPPTComponents) on demand.
"""
# Library Imports.


# Custom Imports.
from ArraySimulation.MPPT.LocalMPPTAlgorithms.LocalMPPTAlgorithm import (
    LocalMPPTAlgorithm,
)
from ArraySimulation.MPPT.LocalMPPTAlgorithms.PandO import PandO
from ArraySimulation.MPPT.LocalMPPTAlgorithms.IC import IC
from ArraySimulation.MPPT.LocalMPPTAlgorithms.FC import FC
from ArraySimulation.MPPT.LocalMPPTAlgorithms.Ternary import Ternary
from ArraySimulation.MPPT.LocalMPPTAlgorithms.Golden import Golden
from ArraySimulation.MPPT.LocalMPPTAlgorithms.Bisection import Bisection


class MPPT:
    """
    The MPPT (Maximum Power Point Tracker) class is a concrete class
    that manages the data flow and operation of MPPT Algorithms. More properly,
    it is a wrapper class that allows the main program to swap between MPPT
    Algorithms and Stride models (see MPPTComponents) on demand.
    """

    def __init__(self):
        self._model = None

    def setupModel(self, numCells=1, MPPTLocalAlgoType="Default", strideType="Fixed"):
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

        if MPPTLocalAlgoType == "PandO":
            self._model = PandO(numCells, strideType)
        elif MPPTLocalAlgoType == "IC":
            self._model = IC(numCells, strideType)
        elif MPPTLocalAlgoType == "Ternary":
            self._model = Ternary(numCells, strideType)
        elif MPPTLocalAlgoType == "Golden":
            self._model = Golden(numCells, strideType)
        elif MPPTLocalAlgoType == "IC":
            self._model = IC(numCells, strideType)
        elif MPPTLocalAlgoType == "Bisection":
            self._model = Bisection(numCells, strideType)
        elif MPPTLocalAlgoType == "FC":
            self._model = FC(numCells, strideType)
        elif MPPTLocalAlgoType == "Default":
            self._model = MPPTAlgorithm(numCells, MPPTLocalAlgoType, strideType)
        else:
            self._model = MPPTAlgorithm(numCells, MPPTLocalAlgoType, strideType)

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

    def getMPPTType(self):
        """
        Returns the MPPT type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._model.getMPPTType()

    def getStrideType(self):
        """
        Returns the Stride model type used for the simulation.

        Return
        ------
        String: Stride type name.
        """
        return self._model.getStrideType()
