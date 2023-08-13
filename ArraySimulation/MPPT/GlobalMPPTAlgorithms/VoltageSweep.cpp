/*
Author: Praneel Murali, Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 02/06/2021
Last Modified: 06/20/2023

Description: The Voltage Sweep class is a derived concrete class of
GlobalAlgorithm implementing the Voltage Sweep algorithm. It increments through
the range of all possible voltage values (the "sweep"), finding all local maxima
of the P-V curve. It then identifies the global maxima using a LocalMPPTAlgorithm.
 */
#include "VoltageSweep.h"

using namespace std;

VoltageSweep::VoltageSweep(int numCells, string MPPTLocalAlgoType, string strideType) :
        GlobalMPPTAlgorithm(numCells, "Voltage Sweep", MPPTLocalAlgoType, strideType){
    sweeping = true;
    increasing = true;
    setup = true;

    stride = 0.01;
    vOld = 0.0;
    iOld = 0.0;
    tOld = 0.0;
    irrOld = 0.0;
    pOld = 0.0;
}

float VoltageSweep::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float vRef = roundf(arrVoltage * 100) / 100;
    if(vRef < GlobalMPPTAlgorithm::MAX_VOLTAGE && sweeping){
        vRef = roundf((_sweep((roundf(arrVoltage * 100) / 100), arrCurrent, irradiance, temperature)) * 100) / 100;
    }else{
        pair<float, float> bounds = _getBounds();
        float lBound = bounds.first;
        float rBound = bounds.second;
        if(setup){
            sweeping = false;
            float maxPower = *max(power_peaks.begin(), power_peaks.end());
            auto maxPowerIter = find(power_peaks.begin(), power_peaks.end(), maxPower);
            float maxVoltage = voltage_peaks[distance(power_peaks.begin(), maxPowerIter)];
            model.setup(maxVoltage, lBound, rBound);
            setup = false;
        }
        if(arrVoltage >= GlobalMPPTAlgorithm::MAX_VOLTAGE){
            vRef = lBound;
        }else if(arrVoltage == lBound){
            vRef = lBound + 0.02;
        }else{
            vRef = model.getReferenceVoltage(arrVoltage, arrCurrent, irradiance, temperature);
            if(vRef < lBound){
                vRef = lBound;
            }
            if(vRef > rBound){
                vRef = rBound;
            }
        }
    }
    return vRef;
}

float VoltageSweep::_sweep(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float pIn = arrCurrent * arrVoltage;
    float vRef = arrVoltage;
    if(pIn < pOld && increasing){
        voltage_peaks.push_back(vOld);
        power_peaks.push_back(pOld);
        increasing = false;
    }else if (pIn >= pOld && !increasing) {
        increasing = true;
        voltage_troughs.push_back(vOld);
    }
    vRef += stride;
    iOld = arrCurrent;
    vOld = arrVoltage;
    pOld = pIn;
    tOld = temperature;
    irrOld = irradiance;
    return vRef;
}

pair<float, float> VoltageSweep::_getBounds() {
    float maxPower = *max(power_peaks.begin(), power_peaks.end());
    auto maxPowerIter = find(power_peaks.begin(), power_peaks.end(), maxPower);
    int index = distance(power_peaks.begin(), maxPowerIter);
    float maxVoltage = voltage_peaks[index];
    float leftBound = 0.0;
    float rightBound = 0.0;
    if(index == 0){
        leftBound = round(voltage_peaks[index] / 2.0 * 100) / 100;
    }else{
        leftBound = max(voltage_troughs[index], (voltage_peaks[index] + voltage_peaks[index - 1]) / 2);
    }
    if(index == power_peaks.size() - 1) {
        rightBound = MAX_VOLTAGE;
    } else {
        rightBound = min(voltage_troughs[index + 1] - 0.02f, (voltage_peaks[index] + voltage_peaks[index + 1]) / 2);
    }
    return make_pair(leftBound, rightBound);
}

void VoltageSweep::reset() {
    GlobalMPPTAlgorithm::reset();
    stride = 0.01;
    voltage_peaks = {0};
    power_peaks = {0};
    sweeping = true;
    increasing = true;
    setup = true;
}

VoltageSweep::~VoltageSweep() {

}
