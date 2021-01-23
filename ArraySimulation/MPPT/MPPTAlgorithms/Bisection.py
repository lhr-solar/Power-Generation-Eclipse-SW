"""
Bisection.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 11/24/20
TODO: Needs update and checking.
Description: The Bisection class is a derived class that determines a VREF to 
apply over PSource to maximize the power generated. The Bisection Method looks
for the root of a unimodal function. In this application, it is the derivative
of the P-V function. It belongs to the set of divide and conquer algorithms.

The implementation of this algorithm is based on the wikipedia page for the
Bisection Method: https://en.wikipedia.org/wiki/Bisection_method

    The Bisection Method seeks to find the min/max of a unimodal
    function. In this case,

    f(x) = P-V Curve, which is max at VMPP.

    It does this by using the derivative of f(x), f'(x), and converges
    towards the x such that the sign of f'(x) flips.

    This algorithm has been serialized into the following steps:

    At initialization:
        [left, right] = [0, MAX_VOLTAGE]        # Bounds
        pNew = 0
        vNew = 0
        pOld = 0
        vOld = 0
        cycle = 0
        K = 0.01

    Cycle 0: Determine our first reference voltage.
        vNew = (left + right) / 2
        VREF = vNew
        GOTO Cycle 1

    Cycle 1: Determine our second reference voltage.
        pNew = ArrVoltage * ArrCurrent
        dP/dV = (pNew - pOld) / (vNew - vOld)

        if dP/dV <= K:                          # Within tolerance. No movement.
            VREF = vOld = vNew
        elif dP/dV > 0:                         # Positive slope. Go right.
            left = vNew
            VREF = vOld = vNew = (left + right) / 2 # TODO: this is not yet right.
            pOld = pNew
        else:                                   # Negtive slop. Go left.
            right = vNew
            VREF = vOld = vNew = (left + right) / 2
            pOld = pNew

    As this algorithm standalone can only support unimodal functions,
    it is a subcomponent for a larger, global MPPT algorithm.

    Note that this method requires an assumption
"""
# Library Imports.
from math import sqrt

# Custom Imports.
from ArraySimulation.MPPT.MPPTAlgorithms.MPPTAlgorithm import MPPTAlgorithm


class Bisection(MPPTAlgorithm):
    """
    The Bisection class is a derived class that determines a VREF to
    apply over PSource to maximize the power generated. The Bisection Method
    looks for the root of a unimodal function. In this application, it is the
    derivative of the P-V function. It belongs to the set of divide and conquer
    algorithms.
    """

    K = 0.01

    def __init__(self, numCells=1, strideType="Fixed"):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        numCells: int
            The number of cells that should be accounted for in the MPPT
            algorithm.
        strideType: String
            The name of the stride model type.
        """
        super(Bisection, self).__init__(numCells, "Bisection", strideType)
        self.left = 0
        self.right = self.MAX_VOLTAGE
        self.l1 = self.left
        self.l2 = self.right
        self.powerL1 = 0
        self.powerL2 = 0
        self.cycle = 0

    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        vRef = 0
        if self.cycle == 0:
            vRef = (self.left + self.right) / 2
            self.cycle = 1
        elif self.cycle == 1:
            self.powerL1 = arrVoltage * arrCurrent

            dP_dV = 0
            if arrVoltage - self.vOld != 0:  # Prevent divide by 0 issues.
                dP_dV = self.powerL1 / (arrVoltage - self.vOld)

            if abs(dP_dV) <= self.K:
                vRef = self.vOld
            # TODO: fix this.
            elif dP_dV > 0:
                pass
            else:
                pass
        else:
            raise Exception("self.cycle is not 0 or 1: " + self.cycle)

        # Update dependent values.
        self.vOld = arrVoltage
        self.pOld = arrVoltage * arrCurrent

        return vRef

    def reset(self):
        super(Bisection, self).reset()
        self.left = 0
        self.right = self.MAX_VOLTAGE
        self.l1 = self.left
        self.l2 = self.right
        self.powerL1 = 0
        self.powerL2 = 0
        self.cycle = 0
