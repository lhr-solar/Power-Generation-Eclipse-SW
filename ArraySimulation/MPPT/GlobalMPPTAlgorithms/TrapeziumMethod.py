"""
TrapeziumMethod.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 10/16/2021
Last Modified: 10/16/2021

Description: Implementation of Trapezoidal Sum Optimization GlobalMPPTAlgortihm.
"""

# library imports
from hashlib import new
import random
import math

# custom imports
from ArraySimulation.MPPT.GlobalMPPTAlgorithms.GlobalMPPTAlgorithm import (
    GlobalMPPTAlgorithm,
)


class TrapeziumMethod(GlobalMPPTAlgorithm):
    
    DV = .05
    def __init__(self, numCells=1, MPPTLocalAlgoType="Default", strideType="Variable"):
        super(TrapeziumMethod, self).__init__(
            numCells, "Trapezium Method ", MPPTLocalAlgoType, strideType
        )  

        self.pref = 0
        self.aref = 0
        self.vref = 0
        self.aold = 0
        self.findingtrapezoids = True
        self.startLocal = True
        self.kick = True
    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        vref = arrVoltage
        arrpower = arrVoltage * arrCurrent
        if (self.findingtrapezoids == True):
            currentarea = (DV * 0.5)*(arrPower +  self.pOld) 
            DA = currentarea - self.aold
            DP = arrPower - self.pOld
            if (DA >= 0):
                self.aref = currentarea
                self.pref = self.pOld
                self.vref = self.vOld
                if (currentarea >= self.aref and arrPower >= self.pref):
                    self.pref = arrPower
                    self.vref = arrVoltage
            else:
                if (currentarea >= self.aref and arrPower >= self.pref):
                    self.pref = arrPower
                    self.vref = arrVoltage
            vref = vref + TrapeziumMethod.DV
            self.vOld = arrVoltage
            self.pOld = arrPower
            self.aold = currentarea
            if(vref > GlobalMPPTAlgorithm.MAX_VOLTAGE):
                findingtrapezoids = False
                return self.vref
            return vref
        else:
            if self.startLocal:
                vref = self.vOld
                self.startLocal = False  # start converging to global maximum
                self._model.setup(self.vOld, 0, GlobalMPPTAlgorithm.MAX_VOLTAGE)
            elif self.kick:  # start local mppt algorithm.
                vref = arrVoltage + 0.02
                self.kick = False
                self.vOld = arrVoltage
                self.pOld = arrCurrent * arrVoltage
                self._model._strideModel.vOld = arrVoltage
                self._model._strideModel.pOld = self.pOld
                self.iOld = arrCurrent
            else:
                vref = self._model.getReferenceVoltage(arrVoltage,arrCurrent,irradiance,temperature)
            return vref
            
     def reset(self):
        super(TrapeziumMethod, self).reset()
        self.pref = 0
        self.aref = 0
        self.vref = 0
        self.aold = 0
        self.findingtrapezoids = True
        self.startLocal = True
        self.kick = True