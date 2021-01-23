"""
FC.py
Author: Afnan Mir, Matthew Yu (2021).
Last Modified: 01/23/2021

Description: Implementation of the dp/dv feedback control.
"""
from ArraySimulation.MPPT.MPPTAlgorithms.MPPTAlgorithm import MPPTAlgorithm

class FC(MPPTAlgorithm):
    def __init__(self,numCells = 1, strideType = "Fixed"):
        super(FC, self).__init__(numCells,"FC", strideType)
        self.firstCycle = True
    
    def getReferenceVoltage(self, arrVoltage,arrCurrent,irradiance,temperature):
        print(arrVoltage, self.vOld)
        error = 0.05
        arrPower = arrCurrent * arrVoltage
        dP = arrPower - self.pOld
        dV = arrVoltage - self.vOld
        stride = self._strideModel.getStride(arrVoltage,arrCurrent, irradiance, temperature)
        vRef = arrVoltage
        if dV == 0:
            vRef+= 0.005
        elif(abs(dP/dV)<error):
            pass
        else:
            if(dP/dV>0):
                vRef += stride
            else:
                vRef -= stride
        self.vOld = arrVoltage
        self.iOld = arrCurrent
        self.pOld = arrVoltage*arrCurrent
        return vRef
