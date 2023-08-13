/*
 * Author: Praneel Murali, Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/24/20
Last Modified: 02/27/21
Description: Implementation of the Ternary Search algorithm.

The implementation of this algorithm is based on the wikipedia page for the
Ternary Search: https://en.wikipedia.org/wiki/Ternary_search

    The Ternary search seeks to find the min/max of a unimodal
    function. In this case,

    f(x) = P-V Curve, which is max at VMPP.

    This algorithm does not require an initial guess, but assumes that
    the initial voltage bound is [0, MAX_VOLTAGE].

    This algorithm has been serialized into the following steps:

    At initialization:
        [left, right] = [0, MAX_VOLTAGE]        # Bounds
        [l1, l2] = [left, right]                # Goalposts
        powerL1 = 0
        powerL2 = 0
        cycle = 0

    Cycle 0: Set the left third goalpost.
        powerL2 = ArrVoltage * ArrCurrent
        if powerL1 > powerL2:                   # Restrict the goalpost
            right = l2
        else:
            left = l1
        l1 = (right - left) / 3 + left
        VREF = l1
        GOTO Cycle 1

    Cycle 1: Set the right third goalpost.
        powerL1 = ArrVoltage * ArrCurrent
        l2 = right - (right - left) / 3
        VREF = l2
        GOTO Cycle 0

    As this algorithm standalone can only support unimodal functions,
    it is a subcomponent for a larger, global MPPT algorithm.

    Note that this method always needs at least two cycles to perform one
    convergence iteration.
 */

#include "Ternary.h"

Ternary::Ternary(int numCells, string strideType) {
    LocalMPPTAlgorithm(numCells, "Ternary", strideType);
    cycle = 0;
    l1 = leftBound;
    l2 = rightBound;
    powerL1 = 0;
    powerL2 = 0;
}

float Ternary::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float vRef = 0;
    if(cycle == 0){
        powerL2 = arrVoltage * arrCurrent;
        if (powerL1 > powerL2){
            rightBound = l2;
        }else{
            leftBound = l1;
        }
        l1 = (rightBound - leftBound) * q + leftBound;
        vRef = l1;
        cycle = 1;
    }else if(cycle == 1){
        powerL1 = arrCurrent * arrVoltage;
        l2 = rightBound - (rightBound - leftBound) * q;
        vRef = l2;
        cycle = 0;
    }else{
        throw runtime_error("cycle is not 0 or 1: " + to_string(cycle));
    }
    return vRef;
}

void Ternary::reset() {
    this->reset();
    cycle = 0;
    l1 = leftBound;
    l2 = rightBound;
    powerL1 = 0;
    powerL2 = 0;
}

Ternary::~Ternary() {

}