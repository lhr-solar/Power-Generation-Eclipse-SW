/*
Author: Praneel Murali, Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 11/26/20

Description: Source file for the PVCellNonIdeal class. Derived class of PVCell that implements a nonideal model tuned to the Sunpower Maxeon III Bin Le1 solar cells.
*/

#include <cmath>
#include <iostream>
#include "PVCellNonIdeal.h"

PVCellNonIdeal::PVCellNonIdeal(bool useLookup)
        : PVCell(useLookup)
{
    _lookup = Lookup({{0.01, 81}, {50, 21}, {0.5, 161}}, 
                     {"v_ref (V)", "irrad (G)", "temp (C)", "current (A)"}, 
                     "NonidealCellLookup.csv");
    _lookup.readFile();
}

double PVCellNonIdeal::getCurrent(
        unsigned int numCells,
        double voltage,
        double irradiance,
        double temperature
) {
    double cellTemperature = temperature + 273.15;
    if (voltage == 0.0)
        voltage = 0.001;
    if (irradiance == 0.0)
        irradiance = 0.001;
    double SCCurrent = irradiance / refIrrad * refSCCurrent * (1 + 6e-4 * (cellTemperature - refTemp));
    double OCVoltage = refOCVoltage - 2.2e-3 * (cellTemperature - refTemp) + k * cellTemperature / q * log(irradiance / refIrrad);
    double PVCurrent = SCCurrent;
    double revSatCurrent = exp(log(SCCurrent) - q * OCVoltage / (k * cellTemperature));
    double currentPrediction = 0;
    double left = currentPrediction;
    double diodeCurrent = revSatCurrent * (exp(q * (voltage + currentPrediction * rSeries) / (k * cellTemperature)) - 1) - (voltage + currentPrediction * rSeries) / rShunt;
    double right = PVCurrent - diodeCurrent;
    double difference = pow(left - right, 2);
    bool decreasing = true;

    while (decreasing) {
        currentPrediction += 0.001;
        left = currentPrediction;
        diodeCurrent = revSatCurrent * (exp(q * (voltage + currentPrediction * rSeries) / (k * cellTemperature)) - 1) - (voltage + currentPrediction * rSeries) / rShunt;
        right = PVCurrent - diodeCurrent;
        if ((difference - pow(left - right, 2)) <= 0.0) {
            decreasing = false;
        }
        difference = pow(left - right, 2);
    }

    return currentPrediction;
}

double PVCellNonIdeal::getCurrentLookup(
        unsigned int numCells,
        double voltage,
        double irradiance,
        double temperature
) {
    return _lookup.lookup({voltage, irradiance, temperature})[0];
}

void PVCellNonIdeal::buildCurrentLookup(
        string fileName,
        double voltageRes,
        double irradianceRes,
        double temperatureRes
) {
    Lookup lookup({{0.01, 81}, {50, 21}, {0.5, 161}},
                  {"v_ref (V)", "irrad (G)", "temp (C)", "current (A)"}, 
                  fileName);
    for (double voltage = 0.00; voltage <= 0.80 + voltageRes; voltage += voltageRes) {
        for (double irradiance = 0.00; irradiance <= 1000 + irradianceRes; irradiance += irradianceRes) {
            for (double temperature = 0.00; temperature <= 80 + temperatureRes; temperature += temperatureRes) {
                // TODO: test to see if irrad, temp = 0 breaks the model.
                double current = getCurrent(1, voltage, irradiance, temperature);
                lookup.addLine({voltage, irradiance, temperature, current});
            }
        }
    }

    lookup.writeFile();
    lookup.readFile();
    _lookup = lookup;
}

string PVCellNonIdeal::getModelType() {
    return "Nonideal";
}
