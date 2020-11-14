"""
IC.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/21/20
Last Modified: 10/21/20

Description: The IC (Incremental Conductance) class is a derived class that
determines a VREF to apply over PSource to maximize the power generated. IC
compares the incremental conductance to the instantaneous conductance. It
belongs to the set of hill climbing algorithms.

The implementation of this algorithm is based on the folowing paper:

    Incremental Conductance Based Maximum Power Point Tracking (MPPT)
    for Photovoltaic System (Bhaskar et Lokanadham.)

    Section 5, Incremental Conductance MPPT

    Given a P-V curve of the solar cell, we can identify three region
    of interest given its incremental versus instantaneous conductance:

        dI/dV = - I/V   At MPP
        dI/dV > - I/V   Left of MPP
        dI/dV < - I/V   Right of MPP

    The algorithm is then fairly straightforward. Identify which region
    of interest we are in, and move to the direction of the MPP using a
    stride function.
"""
# Library Imports.


# Custom Imports.
from ArraySimulation.MPPT.MPPTAlgorithms import MPPTAlgorithm


class IC(MPPTAlgorithm):
    """
    The IC (Incremental Conductance) class is a derived class that
    determines a VREF to apply over PSource to maximize the power generated. IC
    compares the incremental conductance to the instantaneous conductance. It
    belongs to the set of hill climbing algorithms.
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
        super(IC, self).__init__(numCells, "IC", strideType)

    def getReferenceVoltage(
        self, arrVoltage, arrCurrent, irradiance, temperature
    ):
        # Compute secondary values.
        dI = arrCurrent - self.iOld
        dV = arrVoltage - self.vOld

        # Determine the stride.
        stride = self._strideModel.getStride(
            arrVoltage, arrCurrent, irradiance, temperature
        )

        # Determine the direction of movement and VREF.
        vRef = arrVoltage
        if abs(dI * arrVoltage + arrCurrent * dV) < 0.1:  # At MPP.
            pass
        elif dI * arrVoltage + arrCurrent * dV > 0.1:  # Left of MPP.
            vRef += stride
        elif dI * arrVoltage + arrCurrent * dV < -0.1:  # Right o MPP.
            vRef -= stride
        else:
            raise Exception(
                "[IC][getReferenceVoltage] Invalid region of interest."
            )

        # Update dependent values.
        self.iOld = arrCurrent
        self.vOld = arrVoltage

        return vRef
