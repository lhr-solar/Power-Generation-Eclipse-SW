"""
VoltageSweep.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 02/06/2021
Last Modified: 02/06/2021

Description: The Voltage Sweep class is a concrete class that provides the basis for how a global 
MPPT algorithm will perform a voltage sweep to find all of its local maxima. It enables us to find
lower and upper bounds of the global maximum

"""
#imports
from ArraySimulation.MPPT.GlobalMPPTAlgo.GlobalAlgorithm import GlobalAlgorithm
class VoltageSweep(GlobalAlgorithm):
    voltage_peaks = [0] #stores all the voltage values of the local maxima
    power_peaks = [0] #stores the power values of the local maxima
    increasing = True #checks to see if we were increasing before
    #TODO: Add stride argument to voltage sweep constructor
    def __init__(self, numCells = 1,MpptAlgoType = "Default",strideType = "Fixed"):
        """
        Sets up the inital source parameters

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
        super(VoltageSweep, self).__init__(numCells,MpptAlgoType,strideType)
        self._stride = 0.01
        self.vOld = 0.0
        self.iOld = 0.0
        self.tOld = 0.0
        self.irrOld = 0.0
        self.pOld = 0.0
    
    def getReferenceVoltage(self, arrVoltage,arrCurrent,irradiance, temperature):
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
        pIn = arrVoltage * arrCurrent
        vRef = arrVoltage
        print(arrVoltage,arrCurrent)
        if(arrVoltage >= 0.80):
            return 0.80
        if(pIn < self.pOld and self.increasing):
            self.voltage_peaks.append(self.vOld)
            self.power_peaks.append(self.pOld)
            self.increasing = False
        elif(pIn > self.pOld and not self.increasing):
            self.increasing = True
        vRef += self._stride
        self.iOld = arrCurrent
        self.vOld = arrVoltage
        self.pOld = arrCurrent * arrVoltage
        self.tOld = temperature
        self.irrOld = irradiance
        return vRef
    def getBounds(self):
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
        (leftBound,rightBound) = (maxVoltage - 0.1, maxVoltage + 0.1) #0.1 is a placeholder for now. Will probably have to be some factor of the max voltage
        return (leftBound, rightBound)
    def reset(self):
        self._stride = 0.01
        self.vOld = 0.0
        self.iOld = 0.0
        self.tOld = 0.0
        self.irrOld = 0.0
        self.pOld = 0.0
        self.increasing = True
        self.voltage_peaks = [0]
        self.power_peaks = [0]
        

