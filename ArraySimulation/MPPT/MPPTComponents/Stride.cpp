//
//Author: Praneel Murali, Matthew Yu, Array Lead (2020).
//Contact: matthewjkyu@gmail.com
//Created: 11/19/20
//Last Modified: 04/27/23
//Description: Implementation of the Stride class.
//

#include "Stride.h"

/*
 * The Stride class provides the base API for derived classes to
    calculate the stride (change of VREF) for various MPPT algorithms.

    By default, the stride function implemented by the concrete base class is a
    fixed stride.
 */

Stride::Stride(string strideType, float minStride, float VMPP, float error) {
    /*
     * Sets up the initial source parameters.

        Parameters
        ----------
        strideType: String
            The name of the stride type.
        minStride: float
            The minimum value of the stride, if applicable.
        VMPP: float
            Our estimation of the PVSource voltage at the maximum power point.
            Note that the default value is for a single cell and is an
            experimental estimate; according to Sunniva the cell VMPP is 0.621.
        error: float
            The minimum error percentage of V_best to serve as our minimum
            stride.
     */
    this->strideType = strideType;
    this->minStride = minStride;
    this->VMPP = VMPP;
    this->error = error;
    vOld = 0.0;
    iOld = 0.0;
    pOld = 0.0;
    irrOld = 0.0;
    tOld = 0.0;
}

void Stride::setup(float VMPP, float error) {
    /*
     * Reinitializes the predicted parameters for the local MPPT algorithms context.

        Parameters
        ----------
        VMPP: float
            Our estimation of the PVSource voltage at the maximum power point.
            Note that the default value is for a single cell and is an
            experimental estimate; according to Sunniva the cell VMPP is 0.621.
        error: float
            The minimum error percentage of V_best to serve as our minimum stride.
     */
    this->VMPP = VMPP;
    this->error = error;
}

float Stride::getStride(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    /*
     * Calculates the voltage stride for the given PVSource output.
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
     */
    return minStride;
}

void Stride::reset() {
    //Resets any internal variables set by the MPPT algorithm during operation.
    vOld = 0.0;
    iOld = 0.0;
    pOld = 0.0;
    irrOld = 0.0;
    tOld = 0.0;
}

string Stride::getStrideType() {
    /*
     * Returns the Stride model type used for the simulation.

        Return
        ------
        String: Stride type name.
     */
    return strideType;
}

Stride::~Stride(){

}

