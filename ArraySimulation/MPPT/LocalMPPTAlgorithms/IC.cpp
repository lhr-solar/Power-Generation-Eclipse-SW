/*
 * Author: Praneel Murali, Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/21/20
Last Modified: 2/27/21
Description: Implementation of the Incremental Conductance algorithm.

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
 */

#include "IC.h"

IC::IC(int numCells, string strideType) {
    LocalMPPTAlgorithm(numCells, "IC", strideType);
}

float IC::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float dI = arrCurrent - iOld;
    float dV = arrVoltage - vOld;
    float stride = strideModel.getStride(arrVoltage, arrCurrent, irradiance, temperature);
    float vRef = arrVoltage;
    if ((abs(dI * arrVoltage + arrCurrent * dV)) < error){

    }else if(dI * arrVoltage + arrCurrent * dV > error){
        vRef += stride;
    }else if(dI * arrVoltage + arrCurrent * dV < -error){
        vRef -= stride;
    }else{
        throw runtime_error("[IC][getReferenceVoltage] Invalid region of interest.");
    }
    iOld = arrCurrent;
    vOld = arrVoltage;
    return vRef;
}
