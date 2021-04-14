"""
ImprovedSA.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 04/10/2021
Last Modified: 04/10/2021

Description: Implementation of an improved simulated annealing algorithm as an extension of GlobalMPPTAlgortihm
"""

#library imports
import random
import math

#custom imports
from ArraySimulation.MPPT.GlobalMPPTAlgorithms.GlobalMPPTAlgorithm import (
    GlobalMPPTAlgorithm,
)

class ImprovedSA(GlobalMPPTAlgorithm):
    ALPHA = 0.8
    INIT_TEMP = 25
    MIN_TEMP = 0.2
    N_S = 6
    INIT_STEP = 0.8
    N_T = 3
    def __init__(self, 
        numCells=1, 
        MPPTLocalAlgoType="Default",
        strideType="Fixed"):
        super(ImprovedSA,self).__init__(numCells,"Improved SA",MPPTLocalAlgoType,strideType)
        self.temp = ImprovedSA.INIT_TEMP
        self.step = ImprovedSA.INIT_STEP
        self.no_accept = 0
        self.no_perturb = 0
        self.power_max = 0
        self.cycle = 0
        self.no_step = 0

    def getReferenceVoltage(self,arrVoltage,arrCurrent,irradiance, temperature):
        print(self.cycle)
        if self.temp >0.2:
            if self.cycle == 0:
                vRef = round(random.random()*GlobalMPPTAlgorithm.MAX_VOLTAGE,2)
                self.cycle+=1
                self.vOld = arrVoltage
                self.iOld = arrCurrent
                self.pOld = arrVoltage * arrCurrent
                self.irrOld = irradiance
                self.tOld = temperature
            else:
                arrPower = arrVoltage * arrCurrent
                print("Vold: "+ str(self.vOld) + " arrVoltage: " +str(arrVoltage))
                print("Array Power: " + str(arrPower) + " Old Power: "+ str(self.pOld))
                if arrPower > self.pOld:
                    self.vOld = arrVoltage
                    self.iOld = arrCurrent
                    self.pOld = arrVoltage * arrCurrent
                    self.irrOld = irradiance
                    self.tOld = temperature
                else:
                    p_r = math.exp(SimulatedAnnealing.k*(arrPower - self.pOld)/self.temp)
                    print("Vold: "+ str(self.vOld) + " arrVoltage: " +str(arrVoltage))
                    print("Array Power: " + str(arrPower) + " Old Power: "+ str(self.pOld) + " P_r: "+str(p_r))
                    diceRoll = random.random()
                    if(diceRoll < p_r):
                        self.vOld = arrVoltage
                        self.iOld = arrCurrent
                        self.pOld = arrVoltage * arrCurrent
                        self.irrOld = irradiance
                        self.tOld = temperature
                if self.cycle == 4:
                    self.temp = self.temp * SimulatedAnnealing.ALPHA
                    self.cycle = 0
                self.cycle+=1
                searchRange = GlobalMPPTAlgorithm.MAX_VOLTAGE * (self.temp/SimulatedAnnealing.INIT_TEMP)
                leftBound = max(self.vOld - (searchRange/2),0)
                rightBound = min(self.vOld + (searchRange/2), GlobalMPPTAlgorithm.MAX_VOLTAGE)
                vRef = round(random.uniform(leftBound, rightBound),2)
        return vRef
                

    
    def reset(self):
        super(ImprovedSA,self).reset()
        self.temp = ImprovedSA.INIT_TEMP
        self.step = ImprovedSA.INIT_STEP
        self.no_accept = 0
        self.no_perturb = 0
        self.power_max = 0
        self.cycle = 0