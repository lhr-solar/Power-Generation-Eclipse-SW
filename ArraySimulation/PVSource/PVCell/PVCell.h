//
// Created by mpran on 5/26/2023.
//

#ifndef POWER_GENERATION_ECLIPSE_SW_PVCELL_H
#define POWER_GENERATION_ECLIPSE_SW_PVCELL_H

#include <vector>
#include <tuple>
#include <string>

using namespace std;

class PVCell {
public:
    static const double MAX_CELL_VOLTAGE;
    static const double MIN_RESOLUTION;

    PVCell(bool useLookup = true);

    double getCurrent(int numCells = 1, double voltage = 0, double irradiance = 0.001, double temperature = 0);
    double getCurrentLookup(int numCells = 1, double voltage = 0, double irradiance = 0.001, double temperature = 0);

    vector<tuple<double, double>> getCellIV(int numCells = 1, double resolution = 0.01, double irradiance = 0.001, double temperature = 0);
    tuple<double, double, tuple<double, double>> getCellEdgeCharacteristics(int numCells = 1, double resolution = 0.001, double irradiance = 0.001, double temperature = 0);

    string getModelType();

    double refIrrad;
    double refTemp;
    double refSCCurrent;
    double refOCVoltage;
    double k;
    double q;
    double rSeries;
    double rShunt;
    bool _useLookup;
};

#endif //POWER_GENERATION_ECLIPSE_SW_PVCELL_H
