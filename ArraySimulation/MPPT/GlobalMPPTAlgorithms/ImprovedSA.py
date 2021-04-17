"""
ImprovedSA.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 04/10/2021
Last Modified: 04/10/2021

Description: Implementation of an improved simulated annealing algorithm as an extension of GlobalMPPTAlgortihm that is more practical for real world use.
"""

#library imports
import random
import math

#custom imports
from ArraySimulation.MPPT.GlobalMPPTAlgorithms.GlobalMPPTAlgorithm import (
    GlobalMPPTAlgorithm,
)

class ImprovedSA(GlobalMPPTAlgorithm):
    """
    The Simulated Annealing class is a derived concrete class of GlobalAlgorithm
    implementing the Simulated Annealing algorithm. It randomly samples values from
    the range of voltages and chooses the operating point of the voltage either if the power
    at the sampled point is greater than the power of the current operating point, or based
    on a calculated probability. It then identifies the global maxima using a LocalMPPTAlgorithm.
    """
    ALPHA = 0.75 #geometric cooling constant. What you multiply the temperature by to decrease the temperature.
    INIT_TEMP = 25 #Initial value of the temperature
    MIN_TEMP = 0.4 #the temperature when we stop searching
    N_S = 6
    INIT_STEP = 0.8
    N_T = 3
    k = 15
    def __init__(self, 
        numCells=1, 
        MPPTLocalAlgoType="Default",
        strideType="Fixed"):
        super(ImprovedSA,self).__init__(numCells,"Improved SA",MPPTLocalAlgoType,strideType)
        self.temp = ImprovedSA.INIT_TEMP
        # self.step = ImprovedSA.INIT_STEP
        # self.no_accept = 0
        # self.no_perturb = 0
        # self.power_max = 0
        self.cycle = 0
        # self.no_step = 0
        # self.flag = False #if the flag is true, then you will compare the vOld with the arrVoltage. If the flag is false then you will simply return a random value
        # self.searchRange = GlobalMPPTAlgorithm.MAX_VOLTAGE
        # self._leftBound = 0
        # self._rightBound = GlobalMPPTAlgorithm.MAX_VOLTAGE
        self.startLocal = True #If true, the global search just ended, and you go to the operating point stored in vOld
        self.kick = True #kickstart the local algorithm if true

    def getReferenceVoltage(self,arrVoltage,arrCurrent,irradiance, temperature):
        vRef = arrVoltage
        if self.temp >0.2:
            if self.cycle == 0:
                vRef = round(random.random()*GlobalMPPTAlgorithm.MAX_VOLTAGE,2) #choose random value for vRef
                self.cycle+=1
                self.vOld = arrVoltage
                self.iOld = arrCurrent
                self.pOld = arrVoltage * arrCurrent
                self.irrOld = irradiance
                self.tOld = temperature
            elif(self.cycle == 1): #make random value chosed in cycle 0 the operating point stored in vOld
                self.vOld = arrVoltage
                self.iOld = arrCurrent
                self.irrOld = irradiance
                self.tOld = temperature
                self.cycle+=1
            else:
                # if(not self.flag):
                #     vRef = round(random.random()*GlobalMPPTAlgorithm.MAX_VOLTAGE,2)
                #     self.flag = not self.flag
                #     return vRef
                # else:
                arrPower = arrVoltage * arrCurrent
                if(arrPower > self.pOld): #if sampled operating point has greater power than current, make that the new operating point
                    self.vOld = arrVoltage
                    self.pOld = arrPower
                    self.iOld = arrCurrent
                    vRef = arrVoltage
                else: #if the sampled operating point has less power than current, accept the new operating point based on a calculated probability
                    p_r = math.exp((arrPower - self.pOld)/self.temp)
                    print("POld: "+ str(self.pOld) + " arrPower: "+ str(arrPower) + "temp: " +str(self.temp))
                    print(p_r)
                    diceRoll = random.random()
                    if(diceRoll < p_r):
                        self.vOld = arrVoltage
                        self.pOld = arrPower
                        self.iOld = arrCurrent
                        vRef = arrVoltage
                if(self.cycle % 4 == 0): #decrease temperature after every 4 cycles
                    self.temp = self.temp * ImprovedSA.ALPHA
                    print("Temp: " + str(self.temp))
                    # self.searchRange = GlobalMPPTAlgorithm.MAX_VOLTAGE*(self.temp/ImprovedSA.INIT_TEMP)
                self.cycle+=1
                vRef = round(random.random()*GlobalMPPTAlgorithm.MAX_VOLTAGE,2) #get a new random sample
                # self.flag = not self.flag
        else:
            if(self.startLocal):
                vRef = self.vOld
                self.startLocal = False #start converging to global maximum
            elif(self.kick): #start local mppt algorithm.
                vRef = arrVoltage + 0.02
                self.kick = False
                self.vOld =arrVoltage
                self.pOld = arrCurrent * arrVoltage
                self._model._strideModel.vOld = arrVoltage
                self._model._strideModel.pOld = self.pOld
                self.iOld = arrCurrent
            else:
                vRef = self._model.getReferenceVoltage(
                    arrVoltage, arrCurrent, irradiance, temperature
                )
                if(len(self.runningHistory) == 10): #running average sample to check if we have had a drastic change in the power output
                    # previousAverage = sum(self.runningHistory)/len(self.runningHistory)
                    self.runningHistory.remove(self.runningHistory[0]) #pop the oldest value out and add the new value in
                    self.runningHistory.append(arrCurrent * arrVoltage)
                    if(len(self.pastHistories)==10):
                        pastAverage = self.pastHistories[0]
                        self.pastHistories.remove(self.pastHistories[0])
                        self.pastHistories.append(sum(self.runningHistory)/len(self.runningHistory)) #all past averages
                        if((self.pastHistories[len(self.pastHistories)-1] - pastAverage)/pastAverage <= -0.3): #if drastic change in power output, then reinitialize the simulated annealing
                            vRef = 0
                            self.cycle = 0
                            self.temp = ImprovedSA.INIT_TEMP
                            self.startLocal = True
                            self.kick = True
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
            # else:
            #     arrPower = arrVoltage * arrCurrent
            #     print("Vold: "+ str(self.vOld) + " arrVoltage: " +str(arrVoltage))
            #     print("Array Power: " + str(arrPower) + " Old Power: "+ str(self.pOld))
            #     if arrPower > self.pOld:
            #         self.vOld = arrVoltage
            #         self.iOld = arrCurrent
            #         self.pOld = arrVoltage * arrCurrent
            #         self.irrOld = irradiance
            #         self.tOld = temperature
            #     else:
            #         p_r = math.exp(SimulatedAnnealing.k*(arrPower - self.pOld)/self.temp)
            #         print("Vold: "+ str(self.vOld) + " arrVoltage: " +str(arrVoltage))
            #         print("Array Power: " + str(arrPower) + " Old Power: "+ str(self.pOld) + " P_r: "+str(p_r))
            #         diceRoll = random.random()
            #         if(diceRoll < p_r):
            #             self.vOld = arrVoltage
            #             self.iOld = arrCurrent
            #             self.pOld = arrVoltage * arrCurrent
            #             self.irrOld = irradiance
            #             self.tOld = temperature
            #     if self.cycle == 4:
            #         self.temp = self.temp * SimulatedAnnealing.ALPHA
            #         self.cycle = 0
            #     self.cycle+=1
            #     searchRange = GlobalMPPTAlgorithm.MAX_VOLTAGE * (self.temp/SimulatedAnnealing.INIT_TEMP)
            #     leftBound = max(self.vOld - (searchRange/2),0)
            #     rightBound = min(self.vOld + (searchRange/2), GlobalMPPTAlgorithm.MAX_VOLTAGE)
            #     vRef = round(random.uniform(leftBound, rightBound),2)
        return vRef
                

    
    def reset(self):
        super(ImprovedSA,self).reset()
        self.temp = ImprovedSA.INIT_TEMP
        self.step = ImprovedSA.INIT_STEP
        self.no_accept = 0
        self.no_perturb = 0
        self.power_max = 0
        self.cycle = 0
        self.startLocal = True
        self.kick = True