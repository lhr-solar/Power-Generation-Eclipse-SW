"""
Stride.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/19/20
Last Modified: 10/19/20

Description: The Stride class is a concrete base class that provides a common 
API for derived classes to use. The Stride class has roughly one function: to
calculate the stride (change of VREF) for various MPPT algorithms.
"""
# Library Imports.


# Custom Imports.


class Stride:
    """
    The Stride class is a concrete base class that provides a common
    API for derived classes to use. The Stride class has roughly one function:
    to calculate the stride (change of VREF) for various MPPT algorithms.
    """

    def __init__(self, strideType="Fixed", minStride=0.01):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        strideType: String
            The name of the stride type.
        minStride: float
            The minimum value of the stride, if applicable.
        """
        self._strideType = strideType
        self._minStride = minStride
        self.vOld = 0.0
        self.iOld = 0.0
        self.pOld = 0.0
        self.irrOld = 0.0
        self.tOld = 0.0

    def getStride(self, arrVoltage, arrCurrent, irradiance, temperature):
        """
        Calculates the voltage stride for the given PVSource output.
        May use prior history.

        By default, we output a fixed stride.

        Parameters
        ----------
        arrVoltage: float
            Array voltage in V.
        arrCurrent: float
            Array current in A.
        irradiance: float
            Irradiance in W/M^2 (G)
        temperature: float
            Cell Temperature in C.

        Return
        ------
        float The change in voltage that should be applied to the array in the
        next cycle.

        Assumptions
        -----------
        This method is called sequentially in increasing cycle order. The
        arrVoltage and arrCurrent are expected to have stabilized to the
        reference voltage applied in the last cycle, if any.

        Note that the second assumption doesn't hold true in reality, as large
        changes in reference voltage may mean the array does not converge to
        steady state behavior by the next MPPT cycle. This should always be
        considered in the algorithms.
        """
        return self._minStride

    def reset(self):
        """
        Resets any internal variables set by the MPPT algorithm during operation.
        """
        self.vOld = 0.0
        self.iOld = 0.0
        self.pOld = 0.0
        self.irrOld = 0.0
        self.tOld = 0.0

    def getStrideType(self):
        """
        Returns the Stride model type used for the simulation.

        Return
        ------
        String: Stride type name.
        """
        return self._strideType
