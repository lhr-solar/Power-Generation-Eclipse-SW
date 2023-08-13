//
// Created by mpran on 5/26/2023.
//

#ifndef POWER_GENERATION_ECLIPSE_SW_PVCELLNONIDEAL_H
#define POWER_GENERATION_ECLIPSE_SW_PVCELLNONIDEAL_H

#include <cmath>
#include <string>
#include "PVCell.h"
#include "Lookup.h"

using namespace std;

class PVCellNonIdeal : public PVCell
{
public:
    PVCellNonIdeal(bool useLookup=true);

    double getCurrent(
            unsigned int numCells=1,
            double voltage=0,
            double irradiance=0.001,
            double temperature=0
    );

    double getCurrentLookup(
            unsigned int numCells=1,
            double voltage=0,
            double irradiance=0.001,
            double temperature=0
    );

    void buildCurrentLookup(
            string fileName="NonidealCellLookup2.csv",
            double voltageRes=0.01,
            double irradianceRes=50,
            double temperatureRes=0.5
    );

    string getModelType();
    Lookup _lookup;
};


#endif //POWER_GENERATION_ECLIPSE_SW_PVCELLNONIDEAL_H
