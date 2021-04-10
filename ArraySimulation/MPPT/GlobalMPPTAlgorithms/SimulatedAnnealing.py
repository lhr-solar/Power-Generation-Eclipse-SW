"""
SimulatedAnnealing.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 02/06/2021
Last Modified: 02/27/2021

Description: Implementation of the GlobalMPPTAlgorithm class.
"""
# Library Imports.
import random
import math

# Custom Imports.
from ArraySimulation.MPPT.GlobalMPPTAlgorithms.GlobalMPPTAlgorithm import (
    GlobalMPPTAlgorithm,
)
from ArraySimulation.PVEnvironment.PVEnvironment import PVEnvironment
from ArraySimulation.PVSource.PVSource import PVSource

class SimulatedAnnealing(GlobalMPPTAlgorithm):
    ALPHA = 0.8
    MIN_TEMP = 0.3
    INIT_TEMP = 25
    k = 15

    def __init__(
        self,
        numCells=1,
        MPPTLocalAlgoType="Default",
        strideType="Fixed",
    ):
        super(SimulatedAnnealing,self).__init__(numCells,"Simulated Annealing", MPPTLocalAlgoType, strideType)
        #The 'temperature' tells us how likely we are to accept a change even if the power decreases
        
        self.temp = SimulatedAnnealing.INIT_TEMP
        self.cycle = 0
        self._PVEnv = PVEnvironment()
        self._PVSource = PVSource()
        self._PVEnv.setupModel(source = "TwoCellsWithDiode.json", maxCycles = 200)
        self._PVSource.setupModel(modelType = "Ideal")
        self.startLocal = True

    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        vRef = arrVoltage
        if self.temp > SimulatedAnnealing.MIN_TEMP:
            if self.cycle == 0:
                vRef = round(random.uniform(0,GlobalMPPTAlgorithm.MAX_VOLTAGE),2)
                self.cycle += 1
            else:
                arrPower = arrVoltage * arrCurrent
                sample = round(random.uniform(0,GlobalMPPTAlgorithm.MAX_VOLTAGE),2)
                modules = self._PVEnv.getSourceDefinition(sample)
                sourceCurrent = self._PVSource.getSourceCurrent(modules)
                power = sample * sourceCurrent
                if(power > arrPower):
                    vRef = sample
                else:
                    p_r = math.exp(SimulatedAnnealing.k*(power - arrPower)/self.temp)
                    diceRoll = random.random()
                    if(diceRoll < p_r):
                        vRef = sample
                    if self.cycle == 4:
                        self.temp = self.temp * SimulatedAnnealing.ALPHA
                        self.cycle = 0
                    self.cycle += 1
        else:
            if(self.startLocal):
                vRef = arrVoltage + 0.02
                self.startLocal = False
                self.vOld =arrVoltage
                self.pOld = arrCurrent * arrVoltage
                self._model._strideModel.vOld = arrVoltage
                self._model._strideModel.pOld = self.pOld
                self.iOld = arrCurrent
            else:
                print("Hello")
                print("arrVoltage: " + str(arrVoltage) )
                print("SELF.POLD: "+ str(self.pOld))
                vRef = self._model.getReferenceVoltage(
                    arrVoltage, arrCurrent, irradiance, temperature
                )
                if(len(self.runningHistory) == 10):
                    # previousAverage = sum(self.runningHistory)/len(self.runningHistory)
                    self.runningHistory.remove(self.runningHistory[0])
                    self.runningHistory.append(arrCurrent * arrVoltage)
                    if(len(self.pastHistories)==10):
                        pastAverage = self.pastHistories[0]
                        self.pastHistories.remove(self.pastHistories[0])
                        self.pastHistories.append(sum(self.runningHistory)/len(self.runningHistory))
                        if((self.pastHistories[len(self.pastHistories)-1] - pastAverage)/pastAverage <= -0.3):
                            vRef = 0
                            self.cycle = 0
                            self.temp = SimulatedAnnealing.INIT_TEMP
                            self.startLocal = True
                            self.runningHistory.clear()
                            self.pastHistories.clear()
                            return vRef
                    else:
                        self.pastHistories.append(sum(self.runningHistory)/len(self.runningHistory))
                # averageNow = sum(self.runningHistory)/len(self.runningHistory)
                # if((averageNow - previousAverage)/previousAverage <= -0.1):
                #     self.sweeping = True
                #     vRef = 0
                #     self.setup = True
                #     self.runningHistory.clear()
                #     return vRef

                else:
                    self.runningHistory.append(arrCurrent*arrVoltage)

        return vRef
        # print(self.cycle)
        # if self.temp >0.2:
        #     if self.cycle == 0:
        #         vRef = round(random.random()*GlobalMPPTAlgorithm.MAX_VOLTAGE,2)
        #         self.cycle+=1
        #         self.vOld = arrVoltage
        #         self.iOld = arrCurrent
        #         self.pOld = arrVoltage * arrCurrent
        #         self.irrOld = irradiance
        #         self.tOld = temperature
        #     else:
        #         arrPower = arrVoltage * arrCurrent
        #         print("Vold: "+ str(self.vOld) + " arrVoltage: " +str(arrVoltage))
        #         print("Array Power: " + str(arrPower) + " Old Power: "+ str(self.pOld))
        #         if arrPower > self.pOld:
        #             self.vOld = arrVoltage
        #             self.iOld = arrCurrent
        #             self.pOld = arrVoltage * arrCurrent
        #             self.irrOld = irradiance
        #             self.tOld = temperature
        #         else:
        #             p_r = math.exp(SimulatedAnnealing.k*(arrPower - self.pOld)/self.temp)
        #             print("Vold: "+ str(self.vOld) + " arrVoltage: " +str(arrVoltage))
        #             print("Array Power: " + str(arrPower) + " Old Power: "+ str(self.pOld) + " P_r: "+str(p_r))
        #             diceRoll = random.random()
        #             if(diceRoll < p_r):
        #                 self.vOld = arrVoltage
        #                 self.iOld = arrCurrent
        #                 self.pOld = arrVoltage * arrCurrent
        #                 self.irrOld = irradiance
        #                 self.tOld = temperature
        #         if self.cycle == 4:
        #             self.temp = self.temp * SimulatedAnnealing.ALPHA
        #             self.cycle = 0
        #         self.cycle+=1
        #         searchRange = GlobalMPPTAlgorithm.MAX_VOLTAGE * (self.temp/SimulatedAnnealing.INIT_TEMP)
        #         leftBound = max(self.vOld - (searchRange/2),0)
        #         rightBound = min(self.vOld + (searchRange/2), GlobalMPPTAlgorithm.MAX_VOLTAGE)
        #         vRef = round(random.uniform(leftBound, rightBound),2)
        # return vRef
            
    def reset(self):
        super(SimulatedAnnealing,self).reset()
        self.temp = 25

    

        

