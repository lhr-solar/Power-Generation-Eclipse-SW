"""
OptimalStride.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 02/27/21
Description: Implementation of the Optimal Stride perturbation function.

The OptimalStride class implements the perturbation function
discussed in the following paper:

    Optimized Adaptive Perturb and Observe Maximum Power Point Tracking  
    Control for Photovoltaic Generation (Piegari et al.)

    Section 3, Adaptive Pertubation Function for P&O Algorithm

    We can define any stride function as follow:
        stride = f(V_best - V) + dV_min
    
    Optimally, 
        f(V_best - V) = |V_best - V| 
    
    where V_best is an estimate of the MPP of the solar cell.

    Since V_best is unlikely to match physical conditions, we need
    to add an error estimation constant, dV_min.

    We can define an inequality for dV_min:
        dV_min > k^2 / (2 * (1 - k)) * V_best
    
    where k is the percent error. In our implementation, we set this 
    to .05 for 5% error.
"""
# Library Imports.


# Custom Imports.
from ArraySimulation.MPPT.MPPTComponents.Stride import Stride


class OptimalStride(Stride):
    def __init__(self, minStride=0.01, VMPP=0.621, error=0.05):
        super(OptimalStride, self).__init__("Optimal", minStride, VMPP, error)

    def getStride(self, arrVoltage, arrCurrent, irradiance, temperature):
        minStride = self.error * self.error * self.VMPP / (2 * (1 - self.error))
        stride = abs(self.VMPP - arrVoltage)
        return stride + minStride
