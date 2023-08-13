/*
 * Author: Afnan Mir, Array Lead (2021), Praneel Murali.
Contact: afnanmir@utexas.edu
Created: 10/16/2021
Last Modified: 10/16/2021

Description: Implementation of Trapezoidal Sum Optimization GlobalMPPTAlgortihm.
 */

#include "TrapeziumMethod.h"

const float TrapeziumMethod::DV = 0.05;

TrapeziumMethod::TrapeziumMethod(int numCells, std::string MPPTLocalAlgoType, std::string strideType)
        : GlobalMPPTAlgorithm(numCells, "Trapezium Method", MPPTLocalAlgoType, strideType),
          pref(0), aref(0), vref(0), aold(0), findingtrapezoids(true), startLocal(true), kick(true) {
}

float TrapeziumMethod::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float vref = arrVoltage;
    float arrpower = arrVoltage * arrCurrent;

    if (findingtrapezoids) {
        float currentarea = (DV * 0.5) * (arrpower + pref); // Assuming pref is equivalent to pOld
        areas.push_back({currentarea, {vref, arrVoltage}});
        float DA = currentarea - aold;
        float DP = arrpower - pref; // Assuming pref is equivalent to pOld

        if (DA > 0) {
            aref = currentarea;
            pref = arrpower;
            vref = arrVoltage;
        } else if (currentarea >= aref && arrpower >= pref) {
            pref = arrpower;
            vref = arrVoltage;
        }

        vref += DV;
        aold = currentarea;

        if (vref > GlobalMPPTAlgorithm::MAX_VOLTAGE) {
            findingtrapezoids = false;
            return vref;
        }
        return vref;
    } else {
        if (startLocal) {
            vref = this->vref;
            startLocal = false;
            model.setup(this->vref, 0, GlobalMPPTAlgorithm::MAX_VOLTAGE);
        } else if (kick) {
            vref = arrVoltage + 0.02;
            kick = false;
            // Assuming vOld, pOld, and iOld are member variables
            vOld = arrVoltage;
            pOld = arrCurrent * arrVoltage;
            model.strideModel.vOld = arrVoltage;
            model.strideModel.pOld = pOld;
            iOld = arrCurrent;
        } else {
            vref = model.getReferenceVoltage(arrVoltage, arrCurrent, irradiance, temperature);
            // Assuming checkEnvironmentalChanges is a method in TrapeziumMethod or its base class
            bool needsChange = checkEnvironmentalChanges(irradiance);
            if (needsChange) {
                vref = 0;
                pref = 0;
                aref = 0;
                this->vref = 0;
                aold = 0;
                findingtrapezoids = true;
                startLocal = true;
                kick = true;
                runningHistory.clear(); // Assuming runningHistory is a member variable
                return vref;
            }
        }
    }

    std::pair<float, float> bounds = _getBounds();
    if (vref < bounds.first) {
        vref = bounds.first;
    } else if (vref > bounds.second) {
        vref = bounds.second;
    }

    return vref;
}

void TrapeziumMethod::reset() {
    pref = 0;
    aref = 0;
    vref = 0;
    aold = 0;
    findingtrapezoids = true;
    startLocal = true;
    kick = true;
    GlobalMPPTAlgorithm::reset();
}