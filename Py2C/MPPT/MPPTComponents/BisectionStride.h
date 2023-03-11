/*
BisectionStride.py

Author: Afnan Mir, Praneel Murali, and Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/19/20
Last Modified: 02/25/23
Description: Implementation of the Bisection Stride perturbation function.

The BisectionStride class implements the perturbation function
discussed in the following paper:

    Bisection Method Based Modified Perturb and Observe MPPT
    Algorithm for a PV Generation System with an Interleaved,
    Isolated DC-DC Converter (T. Anuradha et al.)

    Section 4, Proposed Modified P&O Algorithm (Bisection Method)

    This paper uses the slope of the P-V curve in order to make
    estimations on where and how much the VREF should go in order
    to reach VMPP.

    In particular, they use the following piecewise function.

    dV = V - V_old
    dP = P - P_old
    stride = f(V)
    f(V) = (V + V_old) / 2 - V_old  , dP/dV < 0
           dV                       , dP/dV > 0

    The behavior of this function is relatively straight forward.
    On the left side of the P-V curve, where the slope is positive,
    advance by a linear change in voltage. On the right side, where
    the slope is negative, take the average of the current and previous
    voltage and the stride is the difference between the average and
    the previous voltage.

    Afnan Mir and I have further optimized this stride function for
    use in our simulations: we make the portion of the piecewise function
    that refers to the left side of the P-V curve dependent on the slope
    of the curve.

    By doing this, and applying a constant multiplier (to make sure we
    don't jump too far at a time), this stride function allows us to
    converge much faster (and surprisingly steadier) to the VMPP.

    Our new piecewise function is the following:

    f(V) = stride_min                   , |dV| < error1, |dP| < error2 (we use 0.01, 0.1, respectively)
           (V + V_old) / 2 - V_old      , dP/dV < 0
           dP / dV * slope_multiplier   , dP/dV > 0

    stride_min is a constant defined by the user.
    */

#include "Stride.h"

class BisectionStride : public Stride {
public:
    BisectionStride(float minStride=0.01, float VMPP=0.621, float error=0.05, float slopeMultiplier=0.01)
        : Stride("Bisection", minStride, VMPP, error) {}

    double mf(float arrVoltage, float arrCurrent, float irradiance, float temperature){
        float minStride = this->error * this->error * this->VMPP / (2 * (1-this->error));
        float stride = abs(this->VMPP - arrVoltage);
        return minStride + stride;
    }
};

