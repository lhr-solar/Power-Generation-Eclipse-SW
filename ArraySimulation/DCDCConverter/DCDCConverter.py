"""
DCDCConverter.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 02/27/21

Description: Implementation of the DCDCConverter class.

In a more advanced model, we might tinker with this class to not do 1-1 conversion,
and investigate the sampling timing required in a real system. Doing so will
allow us to develop feedback loop algorithms for the real DC-DC Converter to
push the source to the correct VRef prior to the MPPT step (which assumes our
voltage has reached the correct place and is at steady state).

This class is still useful, however, since it provides a base template for
translation into C/C++ embedded code for the actual MPPT.
"""
# Library Imports.


# Custom Imports.


class DCDCConverter:
    """
    The DCDCConverter class is a concrete base class that translate
    MPPT Reference voltages into a roughly equivalent pulse width. This class
    mainly is a pass through component of the simulator, since we assume our
    MPPT VRef equates to a pulse width that applies exactly the MPPT VRef across
    the source.
    """

    def __init__(self):
        # Pulse width of the converter.
        self.pulseWidth = 0

        # Current array voltage. We want this to be as close to VMPP at all times.
        self.arrayVoltage = 0

        # Current load voltage. The DCDCConverter converts the array voltage to
        # a voltage strictly higher than the load voltage. The closer to it, the
        # more power that can be transmitted without being lost as heat.
        self.loadVoltage = 0

    def setup(self, arrayVoltage=0.0, loadVoltage=0.6):
        """
        Sets up initial values for the DC-DC converter.

        Parameters
        ----------
        arrayVoltage: float
            Expected array output voltage.
        loadVoltage: float
            Initial load voltage. This is the battery in the case of the solar
            array.

        Returns:
            - None
        """
        self.arrayVoltage = arrayVoltage
        self.loadVoltage = loadVoltage
        self.pulseWidth = 0

    def setPulseWidth(self, MPPTTargetVoltage):
        """
        Generates a pulse width from an expected target voltage based on the
        load voltage.

        Parameters
        ----------
        MPPTTargetVoltage: float
            Expected array output voltage after inputting a specific pulse width.
        """
        if MPPTTargetVoltage > 0.0:
            self.pulseWidth = 1 - self.loadVoltage / MPPTTargetVoltage
            self.arrayVoltage = MPPTTargetVoltage

    def getPulseWidth(self):
        """
        Gets the current pulse width as a fraction from [0, 1].

        Return
        ------
        float: pulse width
        """
        return self.pulseWidth

    def setLoadVoltage(self, loadVoltage):
        """
        Updates the load voltage for DC-DC converter calculation.
        Typically static in the current model.

        Parameters
        ----------
        loadVoltage: float
            New load voltage constraint.
        """
        self.loadVoltage = loadVoltage

    def getVoltageOut(self):
        """
        Gets the expected array voltage given the current pulse width.
        Reverse of set_pulse_width - this is what we expect the dc-dc converter
        to return.

        Return
        ------
        float: expected array voltage
        """
        return self.array_voltage

    def reset(self):
        """
        Resets any internal variables set by the DC-DC Converter during operation.
        """
        self.pulseWidth = 0
        self.arrayVoltage = 0
        self.loadVoltage = 0
