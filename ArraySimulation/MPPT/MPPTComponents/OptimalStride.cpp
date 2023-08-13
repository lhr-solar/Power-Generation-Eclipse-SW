/*
 * Author: Praneel Murali, Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 04/27/23
Description: Implementation of the Optimal Stride perturbation function.

The OptimalStride class implements the perturbation function
discussed in the following paper:

    Optimized Adaptive Perturb and Observe Maximum Power Point Tracking
    Control for Photovoltaic Generation (Piegari et al.)

    Section 3, Adaptive Pertubation Function for P&O Algorithm

    We can define any stride function as follow:
        stride = f(V_best - V) + dV_min

    Optimally,
        f(V_best - V) = |V_best - V|

    where V_best is an estimate of the MPP of the solar cell.

    Since V_best is unlikely to match physical conditions, we need
    to add an error estimation constant, dV_min.

    We can define an inequality for dV_min:
        dV_min > k^2 / (2 * (1 - k)) * V_best

    where k is the percent error. In our implementation, we set this
    to .05 for 5% error.
 */
#include "OptimalStride.h"

OptimalStride::OptimalStride(float minStride, float VMPP, float error) {
    Stride("Optimal", minStride, VMPP, error);
}

float OptimalStride::getStride(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    minStride = error * error * VMPP / (2 * (1 - error));
    float stride = abs(VMPP - arrVoltage);
    return stride + minStride;
}

OptimalStride::~OptimalStride() {

}