"""
MPPT.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/18/20
Last Modified: 10/18/20

Description: The MPPT (Maximum Power Point Tracker) class is a concrete class
that manages the data flow and operation of MPPT Algorithms. More properly, it
is a wrapper class that allows the main program to swap between MPPT Algorithms
and Stride models (see MPPTComponents) on demand.
"""
# Library Imports.


# Custom Imports.
from ArraySimulation.MPPT.MPPTAlgorithms.MPPTAlgorithm import MPPTAlgorithm
from ArraySimulation.MPPT.MPPTAlgorithms.PandO import PandO


class MPPT:
    """
    The MPPT (Maximum Power Point Tracker) class is a concrete class
    that manages the data flow and operation of MPPT Algorithms. More properly,
    it is a wrapper class that allows the main program to swap between MPPT
    Algorithms and Stride models (see MPPTComponents) on demand.
    """

    def __init__(self):
        self._model = None

    def setupModel(self, numCells=1, modelType="Default", strideType="Fixed"):
        """
        Initializes an internal model object for reference.
        This is called whenever the user wants to switch models or stride
        models.

        Parameters
        ----------
        numCells: int
            Number of cells expected by the MPPT model.
        modelType: String
            Specifier for the type of model to be used in the MPPT.
        strideType: String
            Specifier for the type of stride model to be used in the MPPT.
        """
        # Reset any model if there are any already defined.
        if self._model is not None:
            self.reset()

        # Select and rebuild a new model.
        if modelType == "PandO":
            self._model = PandO(numCells, strideType)
        elif modelType == "Default":
            self._model = MPPTAlgorithm(numCells, modelType, strideType)
        else:
            self._model = MPPTAlgorithm(numCells, modelType, strideType)

    def reset(self):
        """
        Resets the internally set MPPT and its relevant Stride Model.
        """
        if self._model is not None:
            self._model.reset()

    def getReferenceVoltage(
        self, arrVoltage, arrCurrent, irradiance, temperature
    ):
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
