"""
OptimalStride.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 11/24/20

Description: Derived class of Stride that implements the perturbation function
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
    """
    Derived class of Stride seeking to jump to the VMPP at all times.
    """

    def __init__(self, minStride=0.01, VMPP=0.47282, error=0.05):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        minStride: float
            The minimum value of the stride, if applicable.
        VMPP: float
            Our estimation of the PVSource voltage at the maximum power point.
            Note that the default value is for a single cell and is an
            experimental estimate; according to Sunniva the cell VMPP is 0.621.
        error: float
            The minimum error percentage of V_best to serve as our minimum
            stride.
        """
        super(OptimalStride, self).__init__("Optimal", minStride)

        self.VMPP = VMPP
        self.k = error

    def getStride(self, arrVoltage, arrCurrent, irradiance, temperature):
        minStride = k * k / (2 * (1 - self.k)) * self.VMPP
        stride = abs(self.VMPP - arrVoltage)
        return stride + minStride
