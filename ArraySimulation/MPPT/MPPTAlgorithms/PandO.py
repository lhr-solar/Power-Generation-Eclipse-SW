"""
PandO.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 11/24/20

Description: The PandO (Perturb and Observe) class is a derived class that
determines a VREF to apply over PSource to maximize the power generated. PandO
utilizes the change of power and change of voltage over time to determine the
direction of movement and stride. It belongs to the set of hill climbing
algorithms.
"""
# Library Imports.


# Custom Imports.
from ArraySimulation.MPPT.MPPTAlgorithms.MPPTAlgorithm import MPPTAlgorithm


class PandO(MPPTAlgorithm):
    """
    The PandO (Perturb and Observe) class is a derived class that
    determines a VREF to apply over PSource to maximize the power generated.
    PandO utilizes the change of power and change of voltage over time to
    determine the direction of movement and stride. It belongs to the set of
    hill climbing algorithms.
    """

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
        super(PandO, self).__init__(numCells, "PandO", strideType)

    def getReferenceVoltage(
        self, arrVoltage, arrCurrent, irradiance, temperature
    ):
        # Compute secondary values.
        pIn = arrVoltage * arrCurrent
        dV = arrVoltage - self.vOld
        dP = pIn - self.pOld

        # Determine the stride.
        stride = self._strideModel.getStride(
            arrVoltage, arrCurrent, irradiance, temperature
        )

        # Determine the direction of movement and VREF.
        vRef = arrVoltage
        if dP > 0:
            if dV > 0:  # Increase vRef.
                vRef += stride
            else:  # Decrease vRef.
                vRef -= stride
        else:
            if dV > 0:  # Decrease vRef.
                vRef -= stride
            else:  # Increase vRef.
                vRef += stride

        # Update dependent values.
        self.vOld = arrVoltage
        self.pOld = pIn

        return vRef
