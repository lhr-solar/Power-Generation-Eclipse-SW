/*
 * Author: Praneel Murali, Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 02/27/21
Description: Implementation of the Bisection method algorithm.

The implementation of this algorithm is based on the wikipedia page for the
Bisection Method: https://en.wikipedia.org/wiki/Bisection_method

    The Bisection Method seeks to find the min/max of a unimodal
    function. In this case,

    f(x) = P-V Curve, which is max at VMPP.

    It does this by using the derivative of f(x), f'(x), and converges
    towards the x such that the sign of f'(x) flips.

    This algorithm has been serialized into the following steps:

    At initialization:
        [left, right] = [0, MAX_VOLTAGE]        # Bounds
        pNew = 0
        pOld = 0
        vOld = 0
        cycle = 0
        K = 0.01

    Cycle 0: Determine our first reference voltage.
        VREF = (left + right) / 2
        vOld = left
        pOld = ArrVoltage * ArrCurrent
        GOTO Cycle 1

    Cycle 1: Determine our second reference voltage.
        pNew = ArrVoltage * ArrCurrent
        dP/dV = (pNew - pOld) / (ArrVoltage - vOld)

        if dP/dV <= K:                          # Within tolerance. No movement.
            VREF = ArrVoltage
        elif dP/dV > 0:                         # Positive slope. Go right.
            left = ArrVoltage
            VREF = (left + right) / 2
        else:                                   # Negative slope. Go left.
            right = ArrVoltage
            VREF = (left + right) / 2

        vOld = ArrVoltage
        pOld = pNew

    As this algorithm standalone can only support unimodal functions,
    it is a subcomponent for a larger, global MPPT algorithm.
 */

#include "Bisection.h"

Bisection::Bisection(int numCells, string strideType) {
    LocalMPPTAlgorithm(numCells, "Bisection", strideType);
    cycle = 0;
    error = 0.01;
}

float Bisection::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float vRef = 0;
    if(cycle == 0){
        vRef = (leftBound + rightBound)/2;
        cycle = 1;
        vOld = leftBound;
        pOld = arrCurrent * arrVoltage;
    }else if(cycle == 1){
        float pNew = arrVoltage * arrCurrent;
        float dP_dV = 0;
        if(arrVoltage - vOld != 0){
            if(abs(dP_dV) <= error){
                vRef = arrVoltage;
            }else if(dP_dV > 0){
                leftBound = arrVoltage;
                vRef = (leftBound + rightBound) / 2;
            }else{
                rightBound = arrVoltage;
                vRef = (leftBound + rightBound) / 2;
            }
        }
        vOld = arrVoltage;
        pOld = pNew;
    }else{
        throw runtime_error("cycle is not 0 or 1: " + to_string(cycle));
    }
    return vRef;
}

void Bisection::reset() {
    reset();
    cycle = 0;
}

Bisection::~Bisection() {

}