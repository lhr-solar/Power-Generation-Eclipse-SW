/*
 * Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 02/27/21

Description: Implementation of the PandO hill climbing algorithm.

 The PandO (Perturb and Observe) class is a derived class of
    LocalMPPTAlgorithm, utilizing the change of power and change of voltage over
    time to determine the direction of movement and stride of the next reference
    voltage. It belongs to the classification of hill climbing algorithms.
 */

#include "PandO.h"

PandO::PandO(int numCells, string strideType) {
    LocalMPPTAlgorithm(numCells, "PandO", strideType);
    minVoltage = 0.05;
}

float PandO::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float pIn = arrCurrent * arrVoltage;
    float dV = arrVoltage - vOld;
    float dP = pIn - pOld;
    float dPr = dP * 1000;
    float dVr = dV * 1000;
    float stride = strideModel.getStride(arrVoltage, arrCurrent, irradiance, temperature);
    float vRef = arrVoltage;
    float vRefr = vRef * 1000;
    if(dP > 0){
        if(dV > 0){
            vRef += stride;
            cout << "Right dp = " << (round(dPr) / 1000) << " dV = " << (round(dVr) / 1000);
        }else if(dV < 0){
            vRef -= stride;
            cout << "Left dp = " << (round(dPr) / 1000) << " dV = " << (round(dVr) / 1000);
        }
    }else{
        if(dV > 0){
            vRef -= stride;
            cout << "Left dp = " << (round(dPr) / 1000) << " dV = " << (round(dVr) / 1000);
        }else if(dV < 0){
            vRef += stride;
            cout << "Right dp = " << (round(dPr) / 1000) << " dV = " << (round(dVr) / 1000);
        }
    }
    cout << " to " << (round(vRefr) / 1000) << endl;

    vOld = arrVoltage;
    pOld = pIn;
    return vRef;
}

PandO::~PandO() {

}