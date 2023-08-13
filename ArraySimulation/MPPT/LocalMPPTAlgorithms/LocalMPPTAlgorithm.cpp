/*
 * LocalMPPTAlgorithm.py

Author: Praneel Murali, Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 02/27/22
Description: Implementation of the LocalMPPTAlgorithm class.
 */

#include "LocalMPPTAlgorithm.h"

LocalMPPTAlgorithm::LocalMPPTAlgorithm(int numCells, string MPPTLocalAlgoType, string strideType) {
    /*
     * Sets up the initial source parameters.

        Parameters
        ----------
        numCells: int
            The number of cells that should be accounted for in the MPPT
            algorithm.
        MPPTLocalAlgoType: String
            The name of the local MPPT algorithm type.
        strideType: String
            The name of the stride algorithm type.
     */
    MAX_VOLTAGE = numCells * MAX_VOLTAGE_PER_CELL;
    this->MPPTLocalAlgoType = MPPTLocalAlgoType;
    if(strideType == "Adaptive"){
        strideModel = AdaptiveStride();
    }else if(strideType == "Bisection"){
        strideModel = BisectionStride();
    }else if(strideType == "Optimal"){
        strideModel = OptimalStride();
    }else{
        strideModel = Stride();
    }

    vOld = 0.0;
    iOld = 0.0;
    pOld = 0.0;
    irrOld = 0.0;
    tOld = 0.0;
    leftBound = 0;
    rightBound = MAX_VOLTAGE;
}

void LocalMPPTAlgorithm::setup(float VMPP, float leftBound, float rightBound) {
    /*
     * Reinitializes the predicted parameters for the local MPPT algorithms context.

        Parameters
        ----------
        VMPP: float
            The voltage of the Maximum Power Point.
     */
    this->leftBound = leftBound;
    this->rightBound = rightBound;
    strideModel.setup(VMPP);
}

float LocalMPPTAlgorithm::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    /*
     * Calculates the reference voltage output for the given PVSource input.
        May use prior history.

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
        float: The reference voltage that should be applied to the array in the
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
    return 0.0;
}

void LocalMPPTAlgorithm::reset() {
    //Resets any internal variables set by the MPPT algorithm during operation.
    strideModel.reset();
    vOld = 0.0;
    iOld = 0.0;
    pOld = 0.0;
    irrOld = 0.0;
    tOld = 0.0;
    leftBound = 0;
    rightBound = MAX_VOLTAGE;
}

string LocalMPPTAlgorithm::getLocalMPPTType() {
    /*
     * Returns the Local MPPT algorithm type used for the simulation.

        Return
        ------
        String: Model type name.
     */
    return this->MPPTLocalAlgoType;
}

string LocalMPPTAlgorithm::getStrideType() {
    /*
     * Returns the Stride model type used for the simulation.

        Return
        ------
        String: Model type name.
     */
    return strideModel.getStrideType();
}

LocalMPPTAlgorithm::~LocalMPPTAlgorithm() {

}


