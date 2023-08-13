/*
 * Author: Praneel Murali, Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 5/26/23

Description: Derived class of PVCell that implements an ideal model tuned to
the Sunpower Maxeon III Bin Le1 solar cells.
 */

#include "PVCellIdeal.h"
#include <cmath>

PVCellIdeal::PVCellIdeal(bool useLookup) : PVCell(useLookup) {}

double PVCellIdeal::getCurrent(
        unsigned int numCells,
        double voltage,
        double irradiance,
        double temperature
) {
    double cellTemperature = temperature + 273.15;
    if (voltage == 0.0) {
        voltage = 0.001;
    }
    if (irradiance == 0.0) {
        irradiance = 0.001;
    }
    double SCCurrent = (
            irradiance
            / this->refIrrad
            * this->refSCCurrent
            * (1 + 6e-4 * (cellTemperature - this->refTemp))
    );
    double OCVoltage = (
            this->refOCVoltage
            - 2.2e-3 * (cellTemperature - this->refTemp)
            + numCells
              * this->k
              * cellTemperature
              / this->q
              * log(irradiance / this->refIrrad)
    );
    double PVCurrent = SCCurrent;
    double revSatCurrent = exp(
            log(SCCurrent) - this->q * OCVoltage / (this->k * cellTemperature)
    );
    double diodeCurrent = PVCurrent;
    if (voltage <= numCells * OCVoltage) {
        diodeCurrent = revSatCurrent * (
                exp(this->q * voltage / (numCells * this->k * cellTemperature)) - 1
        );
    }
    double current = PVCurrent - diodeCurrent;
    return current;
}

string PVCellIdeal::getModelType() {
    return "Ideal";
}
