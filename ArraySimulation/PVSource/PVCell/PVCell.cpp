/*
 * Author: Praneel Murali, Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 5/26/2023

Description: The PVCell (Photovoltaic Cell) class is a concrete base class that
provides a common API for derived classes to use. The PVCell class enables users
to retrieve information of the PVCell model, such as IV curves, maximum power
points, and so on given a set of input conditions.
 */

#include <stdexcept>
#include "PVCell.h"

const double PVCell::MAX_CELL_VOLTAGE = 0.8;
const double PVCell::MIN_RESOLUTION = 0.001;

PVCell::PVCell(bool useLookup){
    refIrrad = 1000;
    refTemp = 25 + 273.15;
    refSCCurrent = 6.15;
    refOCVoltage = 0.721;
    k = 1.381e-23;
    q = 1.602e-19;
    rSeries = 0.032;
    rShunt = 36.1;
    _useLookup = useLookup;
}

double PVCell::getCurrent(int numCells, double voltage, double irradiance, double temperature) {
    return -1;
}

double PVCell::getCurrentLookup(int numCells, double voltage, double irradiance, double temperature) {
    return getCurrent(numCells, voltage, irradiance, temperature);
}

std::vector<std::tuple<double, double>> PVCell::getCellIV(int numCells, double resolution, double irradiance, double temperature) {
    std::vector<std::tuple<double, double>> model;

    if (resolution <= 0) {
        resolution = MIN_RESOLUTION;
    }

    for (double voltage = 0; voltage <= MAX_CELL_VOLTAGE * numCells + resolution; voltage += resolution) {
        double current = _useLookup ? getCurrentLookup(numCells, voltage, irradiance, temperature) : getCurrent(numCells, voltage, irradiance, temperature);

        if (current >= 0.0) {
            model.push_back(std::make_tuple(voltage, current));
        }
        else {
            throw std::runtime_error("Negative current output from the model: " + std::to_string(current));
        }
    }

    return model;
}

std::tuple<double, double, std::tuple<double, double>> PVCell::getCellEdgeCharacteristics(int numCells, double resolution, double irradiance, double temperature) {
    std::tuple<double, double> mpp(0, 0);
    double OCVoltage = 0.0;

    if (resolution <= 0) {
        resolution = MIN_RESOLUTION;
    }

    auto model = getCellIV(numCells, resolution, irradiance, temperature);

    if (!model.empty()) {
        double SCCurrent = std::get<1>(model[0]);

        for (auto &[voltage, current] : model) {
            if (std::get<0>(mpp) * std::get<1>(mpp) < voltage * current) {
                mpp = std::make_tuple(voltage, current);
            }
            if (OCVoltage != 0.0 && current == 0) {
                OCVoltage = voltage;
            }
        }

        return std::make_tuple(OCVoltage, SCCurrent, mpp);
    }
    else {
        return std::make_tuple(0.0, 0.0, std::make_tuple(0.0, 0.0));
    }
}

std::string PVCell::getModelType() {
    return "Default";
}