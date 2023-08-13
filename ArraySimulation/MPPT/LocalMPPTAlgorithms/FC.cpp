/*
 * Author: Praneel Murali, Afnan Mir, Matthew Yu (2021).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 02/27/2021

Description: Implementation of the dP/dV feedback control D&C algorithm.
 */
#include "FC.h"

FC::FC(int numCells, string strideType) {
    LocalMPPTAlgorithm(numCells, "FC", strideType);
    error = 0.05;
}

float FC::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float arrPower = arrCurrent * arrVoltage;
    float dP = arrPower - pOld;
    float dV = arrVoltage - vOld;
    float stride = strideModel.getStride(arrVoltage, arrCurrent, irradiance, temperature);
    float vRef = arrVoltage;
    if(dV == 0){
        vRef += 0.005;
    } else if(abs(dP/dV) < error){

    }else{
        if(dP / dV > 0){
            vRef += stride;
        }else{
            vRef -= stride;
        }
        vOld = arrVoltage;
        iOld = arrCurrent;
        pOld = arrVoltage * arrCurrent;
        return vRef;
    }
}

FC::~FC() {

}