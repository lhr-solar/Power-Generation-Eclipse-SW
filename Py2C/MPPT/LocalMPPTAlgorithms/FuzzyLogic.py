"""
FuzzyLogic.py

Author: Matthew Yu.
Contact: matthewjkyu@gmail.com
Created: 5/14/22
Last Modified: 5/14/22

Description: Implementation of the Fuzzy Logic algorithm.
"""
# Library Imports.


# Custom Imports.
from ArraySimulation.MPPT.LocalMPPTAlgorithms.LocalMPPTAlgorithm import (
    LocalMPPTAlgorithm,
)


class FuzzyLogic(LocalMPPTAlgorithm):
    """
    The Fuzzy Logic class is a derived class of LocalMPPTAlgorithm. 
    This particular verstion attempts to replicate Takun et al and has two input variables:
    - change in power
    - change in current

    
    These two input variables are classified by their respective membership
    functions (MFs).
    
    The power membership function defines 5 terms
    - NB - Negative Big     | [, -10%]
    - NS - Negative Small   | (-10%, -3%]
    - ZE - Zero             | (-3%, 3%)
    - PS - Positive Small   | [3%, 10%)
    - PB - Positive Big     | [10%, ]
    
    And the current membership function defines 3 terms:
    - N - Negative          | [, -1%]
    - Z - Zero              | (-1%, 1%)
    - P - Positive          | [1%, ]
    
    The rule table for the juxtaposition of both MFs is as follows, and is
    strictly arbitrary. The output term is the change in the reference voltage.
    
    Fuzzy Rule         dP/dV
                  NB | NS | ZE | PS | PB
            N   | NB | NS | PS | PS | PB
    dI/dV   Z   | PB | PS | ZE | NS | NB
            P   | PB | PS | NS | NS | NB
    
    Where the output set corresponds to the following values:
    - NB - Negative Big     | -5%
    - NS - Negative Small   | -1%
    - ZE - Zero             | 0%
    - PS - Positive Small   | 1%
    - PB - Positive Big     | 5%
    
    Beyond the current scope of this validation and proof of concept paper are
    following additions:

    - The input variable set can be further expanded to include:
        - change in voltage
        - change in temperature
        - change in irradiance
    - The membership functions can have a wider set size, perhaps 5 rules per
      input.
    - The membership function shapes can also be varies (triangular, trapezoial,
      sigmoidal, etc).
    - The rule table values can be optimized using brute force automation
      testing and/or machine learning approaches.
      
    Fuzzy Logic utilizes the rule table to defuzzify the inputs and generate an
    output. This can be considered a form of adaptive hill climbing algorithm in
    that the  .

    , utilizing the change of power and change of voltage over
    time to determine the direction of movement and stride of the next reference
    voltage. It belongs to the classification of hill climbing algorithms.
    """

    def __init__(self, numCells=1, strideType="Fixed"):
        super(FuzzyLogic, self).__init__(numCells, "Fuzzy Logic", strideType)
        print("HI")
        self._minVoltage = 0.05
        self._maxVoltage = numCells*0.721
        self._maxPower = numCells*3.63
        self._maxCurrent = 6.15
        self._start = True
        self._ruleset = {
            "dP": [(-100, -10), (-10, -3), (-3, 3), (3, 10), (10, 100)],
            "dI": [(-100, -1), (-1, 1), (1, 100)],
            "ruleset": [
                #NB NS ZE PS PB
                [1, 1, 1, 3, 4], # N # add field: if current drop is small, go big
                [3, 3, 2, 3, 4], # Z
                [4, 3, 3, 1, 1]  # P
            ],
            "dV": [-.04, -.02, 0.01, .02, .04]
        }

    def getReferenceVoltage(self, arrVoltage, arrCurrent, irradiance, temperature):
        # Compute secondary values.
        pIn = arrVoltage * arrCurrent
        dV = arrVoltage - self.vOld
        dI = arrCurrent - self.iOld
        dP = pIn - self.pOld
        
        print(f"\nV:{arrVoltage}, I:{arrCurrent}, P:{arrVoltage*arrCurrent}")

        vRef = arrVoltage
        if self._start is True:
            self._start = False
            vRef = self._minVoltage
        else:
            # Default is no change.
            dPTerm = 2
            dITerm = 1
            # Determine fuzzy rule from input MFs.
            dPPercentage = dP * 100 / self._maxPower
            dIPercentage = dI * 100 / self._maxCurrent
            for idx, term in enumerate(self._ruleset["dP"]):
                if dPPercentage > term[0] and dPPercentage <= term[1]:
                    dPTerm = idx
                    break
            
            for idx, term in enumerate(self._ruleset["dI"]):
                if dIPercentage > term[0] and dIPercentage <= term[1]:
                    dITerm = idx
                    break
                
            print(f"Change in power: {dV} | {dV / 100 * self._maxVoltage}")
            print(f"Change in current: {dI} | {dIPercentage}")
            print(f"Change in power: {dP} | {dPPercentage}")
            
            val = self._ruleset["dP"][dPTerm]
            print(f"dP Rule: {val}")
            val = self._ruleset["dI"][dITerm]
            print(f"dI Rule: {val}")
            rulesetIdx = self._ruleset["ruleset"][dITerm][dPTerm]
            vRefShift = self._ruleset["dV"][rulesetIdx]# / 100 * self._maxVoltage
            # val = self._ruleset["dV"][rulesetIdx]
            print(f"Voltage shift: {vRefShift} | {rulesetIdx}")
            vRef += vRefShift
            print(f"New VREF {vRef}")

        # Update dependent values.
        self.vOld = arrVoltage
        self.iOld = arrCurrent
        self.pOld = pIn

        if vRef >= self._maxVoltage:
            vRef = self._maxVoltage-0.01
        return vRef
