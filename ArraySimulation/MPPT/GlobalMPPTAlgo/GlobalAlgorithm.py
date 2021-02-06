"""
GlobalAlgorithm.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 02/06/2021
Last Modified: 02/06/2021

Description: The Global MPPTAlgorithm (Maximum Power Point Tracker) class is a concrete
base class that provides a common API for derived classes to use. The
GlobalAlgorithm class enables users to calculate or predict voltage setpoints that
would maximize the output power of the PVSource given a set of input conditions.
"""
from ArraySimulation.MPPT.MPPTAlgorithms.MPPTAlgorithm import MPPTAlgorithm
from ArraySimulation.MPPT.MPPTAlgorithms.PandO import PandO
from ArraySimulation.MPPT.MPPTAlgorithms.IC import IC
from ArraySimulation.MPPT.MPPTAlgorithms.FC import FC
from ArraySimulation.MPPT.MPPTAlgorithms.Ternary import Ternary
from ArraySimulation.MPPT.MPPTAlgorithms.Golden import Golden
from ArraySimulation.MPPT.MPPTAlgorithms.Bisection import Bisection

class GlobalAlgorithm:
    MAX_VOLTAGE = 100

    MAX_VOLTAGE_PER_CELL = 0.8


    def __init__(self, numCells = 1, MpptAlgoType = "Default", strideType = "Fixed"):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        numCells: int
            The number of cells that should be accounted for in the MPPT
            algorithm.
        MpptAlgoType: String
            The name of the model type.
        strideType: String
            The name of the stride model type.
        """
        self.MAX_VOLTAGE = self.MAX_VOLTAGE_PER_CELL*numCells
        self._MpptAlgoType = MpptAlgoType
        
        
        if MpptAlgoType == "PandO":
            self._model = PandO(numCells, strideType)
        elif MpptAlgoType == "IC":
            self._model = IC(numCells, strideType)
        elif MpptAlgoType == "Ternary":
            self._model = Ternary(numCells, strideType)
        elif MpptAlgoType == "Golden":
            self._model = Golden(numCells, strideType)
        elif MpptAlgoType == "IC":
            self._model = IC(numCells, strideType)
        elif MpptAlgoType == "Bisection":
            self._model = Bisection(numCells, strideType)
        elif MpptAlgoType == "FC":
            self._model = FC(numCells, strideType)
            print("Hello")
        elif MpptAlgoType == "Default":
            self._model = MPPTAlgorithm(numCells, MpptAlgoType, strideType)
        else:
            self._model = MPPTAlgorithm(numCells, MpptAlgoType, strideType)
        
        self.vOld = 0.0
        self.iOld = 0.0
        self.tOld = 0.0
        self.irrOld = 0.0
        self.pOld = 0.0
    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        """
        Calculates the reference voltage output for the given PVSource output.
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
        float The reference voltage that should be applied to the array in the
        next cycle.

        Assumptions
        -----------
        This method is called sequentially in increasing cycle order. The
        arrVoltage and arrCurrent are expected to have stabilized to the
        reference voltage applied in the last cycle, if any.

        Note that the second assumption doesn't hold true in reality, as large
        changes in reference voltage may mean the array does not converge to
        steady state behavior by the next MPPT cycle. This should always be
        considered in the algorithms.
        """
        return self._model.getReferenceVoltage(arrVoltage,arrCurrent,irradiance,temperature)

    def reset(self):
        """
        Resets any internal variables set by the MPPT algorithm during operation.
        """
        self._model.reset()
        self.vOld = 0.0
        self.iOld = 0.0
        self.pOld = 0.0
        self.irrOld = 0.0
        self.tOld = 0.0

    def getMPPTType(self):
        """
        Returns the MPPT type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._MpptAlgoType 



