/*
 * Author: Praneel Murali, Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 02/27/21
Description: Implementation of the Golden Section Search algorithm.

The implementation of this algorithm is based on the wikipedia page for the
Golden Section Search: https://en.wikipedia.org/wiki/Golden-section_search

    The Golden Section search seeks to find the min/max of a unimodal
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

    Cycle 0: Determine our first reference voltage.
        l1 = right - (right - left) * phi
        VREF = l1
        GOTO Cycle 1

    Cycle 1: Determine our second reference voltage.
        powerL1 = ArrVoltage * ArrCurrent
        l2 = (right - left) * phi + left
        VREF = l2
        GOTO Cycle X

    Cycle X:
        powerL2 = ArrVoltage * ArrCurrent

    Cycle X + 1:
        powerL1 = ArrVoltage * ArrCurrent

    Cycle X, X + 1:
        if powerL1 > powerL2:                   # Move right goalpost.
            right = l2                          # Cut the right bound to the right goalpost.
            l2 = l1                             # Set right goalpost voltage, power to the left goalpost's.
            powerL2 = powerL1

            l1 = right - (right - left) * phi   # Set left goalpost to a new spot.
            VREF = l1
            GOTO Cycle X + 1
        else:                                   # Move left goalpost
            left = l1                           # Cut the left bound to the left goalpost.
            l1 = l2                             # Set left goalpost voltage, power to the right goalpost's.
            powerL1 = powerL2

            l2 = (right - left) * phi + left    # Set right goalpost to a new spot.
            VREF = l2
            GOTO Cycle X

    As this algorithm standalone can only support unimodal functions,
    it is a subcomponent for a larger, global MPPT algorithm.

    Note that this method needs two starting cycles to begin convergence.
    Unlike Ternary Search, it can converge every cycle rather than every
    other cycles.
 */

#include "Golden.h"

Golden::Golden(int numCells, string strideType) {
    LocalMPPTAlgorithm(numCells, "Golden", strideType);
    cycle = 0;
    l1 = leftBound;
    l2 = rightBound;
    powerL1 = 0;
    powerL2 = 0;
}

float Golden::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float vRef = 0;
    if(cycle == 0){
        l1 = rightBound - (rightBound - leftBound) * phi;
        vRef = l1;
    }else if(cycle == 1){
        powerL1 = arrCurrent * arrVoltage;
        l2 = (rightBound - leftBound) * phi + leftBound;
        vRef = l2;
        cycle = 2;
    }else{
        if(cycle == 2){
            powerL2 = arrVoltage * arrCurrent;
        }else if(cycle == 3){
            powerL1 = arrVoltage * arrCurrent;
        }else{
            throw runtime_error("cycle is not 2 or 3: " + to_string(cycle));
        }

        if(powerL1 > powerL2){
            rightBound = l2;
            l2 = l1;
            powerL2 = powerL1;
            l1 = (rightBound - (rightBound - leftBound) * phi);
            vRef = l1;
            cycle = 3;
        }else{
            leftBound = l1;
            l1 = l2;
            powerL1 = powerL2;
            l2 = (rightBound - leftBound) * phi + leftBound;
            vRef = l2;
            cycle = 2;
        }
    }
    return vRef;
}

void Golden::reset() {
    reset();
    cycle = 0;
    l1 = leftBound;
    l2 = rightBound;
    powerL1 = 0;
    powerL2 = 0;
}

Golden::~Golden() {

}
