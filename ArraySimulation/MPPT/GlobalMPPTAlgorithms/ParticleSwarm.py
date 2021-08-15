"""
ParticleSwarm.py

Author: Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 08/08/2021
Last Modified: 08/08/2021

Description: Implementation of Particle Swarm Optimization GlobalMPPTAlgortihm.
"""

#library imports
from hashlib import new
import random
import math

#custom imports
from ArraySimulation.MPPT.GlobalMPPTAlgorithms.GlobalMPPTAlgorithm import (
    GlobalMPPTAlgorithm,
)

class Particle():
    def __init__(self, xPos, vel):
        self.personalBest = 0.0
        self.personalBestVolt = 0.0
        self.xPos = xPos
        self.vel = vel
    
    def changeXPos(self,vel):
        self.xPos += vel
    
    def changeVel(self, newVel):
        self.vel = newVel
    
    def getPBest(self):
        return self.personalBest

    def getVoltBest(self):
        return self.personalBestVolt

    def getXPos(self):
        return self.xPos
    
    def getVel(self):
        return self.vel

    def changePBest(self, newBest, newBestVolt):
        self.personalBest = newBest
        self.personalBestVolt = newBestVolt
    def __str__(self):
        return f"Position: {self.xPos}\n Velocity: {self.vel}\nPersonal Best: {self.personalBestVolt}"


class ParticleSwarm(GlobalMPPTAlgorithm):
    """
    Class to implement the Particle Swarm Optimization Algorithm for Maximium Power Point Tracking
    (https://www.ieeexplore-ieee-org.ezproxy.lib.texas.edu/document/7233061)
    """
    NUM_AGENTS = 4
    C1 = 0.02
    C2 = 0.5
    W = 0.4

    def __init__(self, 
        numCells=1, 
        MPPTLocalAlgoType="Default",
        strideType="Fixed"):
        """
        Constructor for the Particle Swarm Optimization algorithm

        Parameters
        ----------
        numCells : int
            number of cells
        MPPTLocalAlgoType : str
            the local algorithm to use
        strideType : str
            Stride to use for perturb and observe

        Returns
        -------
        None
        """
        super(ParticleSwarm, self).__init__(numCells, "Particle Swarm", MPPTLocalAlgoType, strideType)
        self.gBest = 0.0
        self.gBestVolt = 0.0
        self.agents = []
        self.goForward = True
        self._setup = True
        self.startLocal = True
        self.kick = True
        self.totalCycle = 0
        interval = GlobalMPPTAlgorithm.MAX_VOLTAGE/5
        for i in range(ParticleSwarm.NUM_AGENTS):
            self.agents.append(Particle((random.random()*interval)+(interval*i), 0.0))
        self.cycle = -1
        for i in self.agents:
            print(i.getXPos())


    def getVelocityVector(self, agent):
        """
        Returns the new velocity for the agent given the agents personal best position, the global best position, and the current velocity based
        on the equation
        V_{k+1} = w*V_{k} + c1*r1*(p_{i_best} - x_{k}) + c2*r2*(g_best - x_{k})
        V_k = current velocity
        c1 and c2: constants
        r1 and r2: normalized random number between 0 and 1.
        p_{i_best} = current best position the agent has been to
        g_best = global best position
        w = constant

        Parameters
        ----------
        agent : Particle
            The particle that is being updated

        Returns
        -------
        newVel : int
            the new velocity vector for the agent.
        """
        r1 = random.random()
        r2 = random.random()
        newVel = ParticleSwarm.W*agent.getVel() + ParticleSwarm.C1*r1*(agent.getVoltBest() - agent.getXPos()) + ParticleSwarm.C2*r2*(self.gBestVolt - agent.getXPos())
        # print(newVel)
        return newVel

    def setUp(self, arrVoltage, arrCurrent, irradiance, temperature):
        """
        Method takes care of the first 4 cycles to put each agent in its starting point and
        determines the personal bests and global best position(s).

        Parameters
        ----------
        arrVoltage : float
            Array voltage of the current cycle
        arrCurrent : float
            Array current of the current cycle
        irradiance : float
            Irradiance of the current cycle
        temperature : float
            Temperature of the current cycle

        Returns
        -------
        vRef : float
            next array voltage to output
        """
        agentPower = arrVoltage * arrCurrent
        if(self.cycle == -1):
            self.cycle = 0
            self.totalCycle += 1
            vRef =  self.agents[0].getXPos()
        elif(self.cycle == 0 and self._setup):
            if(agentPower > self.agents[0].getPBest()):
                self.agents[0].changePBest(agentPower, arrVoltage)
            if(agentPower > self.gBest):
                self.gBest = agentPower
                self.gBestVolt = arrVoltage
            self.cycle += 1
            self.totalCycle += 1
            vRef = self.agents[1].getXPos()
        elif(self.cycle == 1 and self._setup):
            if(agentPower > self.agents[1].getPBest()):
                self.agents[1].changePBest(agentPower, arrVoltage)
            if(agentPower > self.gBest):
                self.gBest = agentPower
                self.gBestVolt = arrVoltage
            self.totalCycle += 1
            self.cycle += 1
            vRef = self.agents[2].getXPos()
        elif(self.cycle == 2 and self._setup):
            if(agentPower > self.agents[2].getPBest()):
                self.agents[2].changePBest(agentPower, arrVoltage)
            if(agentPower > self.gBest):
                self.gBest = agentPower
                self.gBestVolt = arrVoltage
            self.cycle += 1
            self.totalCycle += 1
            vRef = self.agents[3].getXPos()
        elif(self.cycle == 3 and self._setup):
            if(agentPower > self.agents[3].getPBest()):
                self.agents[3].changePBest(agentPower, arrVoltage)
            if(agentPower > self.gBest):
                self.gBest = agentPower
                self.gBestVolt = arrVoltage
            self.totalCycle += 1
            self.cycle = 2
            self._setup = False
            self.goForward = False
            vRef = self.agents[2].getXPos()
        return vRef
    def agentUpdate(self, arrVoltage, arrCurrent, irradiance, temperature):
        """
        Method that updates the current state of the particles on the curve.

        Parameters
        ----------
        arrVoltage : float
            Array voltage of the current cycle
        arrCurrent : float
            Array current of the current cycle
        irradiance : float
            Irradiance of the current cycle
        temperature : float
            Temperature of the current cycle

        Returns
        -------
        vRef : float
            array voltage to output
        """
        vRef = arrVoltage
        if(self._setup):
            vRef = self.setUp(arrVoltage, arrCurrent, irradiance, temperature)
        else:
            vRef = arrVoltage
            agentPower = arrVoltage * arrCurrent
            if(self.cycle == 0):
                if(agentPower > self.agents[0].getPBest()):
                    self.agents[0].changePBest(agentPower, arrVoltage)
                if(agentPower > self.gBest):
                    self.gBest = agentPower
                    self.gBestVolt = arrVoltage
                newVel = self.getVelocityVector(self.agents[0])
                self.agents[0].changeXPos(newVel)
                self.agents[0].changeVel(newVel)
                self.goForward = True
                self.cycle = 1
                self.totalCycle += 1
                vRef = self.agents[1].getXPos()
            elif(self.cycle % 4 == 1):
                if(agentPower > self.agents[1].getPBest()):
                    self.agents[1].changePBest(agentPower, arrVoltage)
                if(agentPower > self.gBest):
                    self.gBest = agentPower
                    self.gBestVolt = arrVoltage
                newVel = self.getVelocityVector(self.agents[1])
                self.agents[1].changeXPos(newVel)
                self.agents[1].changeVel(newVel)
                if(self.goForward):
                    vRef = self.agents[2].getXPos()
                    self.cycle = 2
                else:
                    vRef = self.agents[0].getXPos()
                    self.cycle = 0
                self.totalCycle += 1
            elif(self.cycle % 4 == 2):
                if(agentPower > self.agents[2].getPBest()):
                    self.agents[2].changePBest(agentPower, arrVoltage)
                if(agentPower > self.gBest):
                    self.gBest = agentPower
                    self.gBestVolt = arrVoltage
                newVel = self.getVelocityVector(self.agents[2])
                self.agents[2].changeXPos(newVel)
                self.agents[2].changeVel(newVel)
                if(self.goForward):
                    vRef = self.agents[3].getXPos()
                    self.cycle = 3
                else:
                    vRef = self.agents[1].getXPos()
                    self.cycle = 1
                self.totalCycle += 1
            elif(self.cycle % 4 == 3):
                if(agentPower > self.agents[3].getPBest()):
                    self.agents[3].changePBest(agentPower, arrVoltage)
                if(agentPower > self.gBest):
                    self.gBest = agentPower
                    self.gBestVolt = arrVoltage
                newVel = self.getVelocityVector(self.agents[3])
                self.agents[3].changeXPos(newVel)
                self.agents[3].changeVel(newVel)
                vRef = self.agents[2].getXPos()
                self.cycle = 2
                self.totalCycle += 1
                self.goForward = False
        return vRef

    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        """
        Method that updates output voltage of the array.

        Parameters
        ----------
        arrVoltage : float
            Array voltage of the current cycle
        arrCurrent : float
            Array current of the current cycle
        irradiance : float
            Irradiance of the current cycle
        temperature : float
            Temperature of the current cycle

        Returns
        -------
        vRef : float
            array voltage to output
        """
        if(self.totalCycle <= 45):
            vRef =  self.agentUpdate(arrVoltage,arrVoltage, irradiance, temperature)
            print(f"Cycle {self.totalCycle}")
            for i in range(len(self.agents)):
                print("Particle" + str(i))
                print(self.agents[i])
        else:
            if(self.startLocal):
                vRef = self.gBestVolt
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
            self.totalCycle += 1
            return vRef
        return vRef
    def reset(self):
        """
        Method to reset the pipeline

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        self.gBest = 0.0
        self.gBestVolt = 0.0
        # self.agents = []
        self.goForward = True
        self._setup = True
        self.startLocal = True
        self.kick = True
        self.totalCycle = 0
        interval = GlobalMPPTAlgorithm.MAX_VOLTAGE/5
        for i in range(ParticleSwarm.NUM_AGENTS):
            self.agents.append(Particle((random.random()*interval)+(interval*i), 0.0))
        self.cycle = -1
        for i in self.agents:
            print(i.getXPos())
        

