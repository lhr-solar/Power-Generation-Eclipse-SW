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
    # The upper voltage bound that should be predicted by any model. We expect
    # the PV to always be at open circuit voltage at this point. Adjustable
    # based on the number of cells determined from the initialization.
    MAX_VOLTAGE = 100

    # The upper voltage bound for a single cell that should be predicted by any
    # model. We expect the PV to always be at open circuit voltage at this
    # point. The reference value was determined from experimentation from the
    # Maxeon Gen III Bin Le1 solar cells, which have a rated voltage of .721V at
    # standard conditions.
    MAX_VOLTAGE_PER_CELL = 0.8

    def __init__(self, numCells = 1, MPPTAlgoType = "Default", strideType = "Fixed"):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        numCells: int
            The number of cells that should be accounted for in the MPPT
            algorithm.
        MPPTAlgoType: String
            The name of the model type.
        strideType: String
            The name of the stride model type.
        """
        self.MAX_VOLTAGE = self.MAX_VOLTAGE_PER_CELL*numCells
        self._MPPTAlgoType = MPPTAlgoType
        
        if MPPTAlgoType == "PandO":
            self._model = PandO(numCells, strideType)
        elif MPPTAlgoType == "IC":
            self._model = IC(numCells, strideType)
        elif MPPTAlgoType == "Ternary":
            self._model = Ternary(numCells, strideType)
        elif MPPTAlgoType == "Golden":
            self._model = Golden(numCells, strideType)
        elif MPPTAlgoType == "IC":
            self._model = IC(numCells, strideType)
        elif MPPTAlgoType == "Bisection":
            self._model = Bisection(numCells, strideType)
        elif MPPTAlgoType == "FC":
            self._model = FC(numCells, strideType)
        elif MPPTAlgoType == "Default":
            self._model = MPPTAlgorithm(numCells, MPPTAlgoType, strideType)
        else:
            self._model = MPPTAlgorithm(numCells, MPPTAlgoType, strideType)
        
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

    def getGlobalMPPTType(self):
        """
        Returns the MPPT type used for the simulation.

        Return
        ------
        String: Model type name.
        """
        return self._MPPTAlgoType 



