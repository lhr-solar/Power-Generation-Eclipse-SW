#ifndef POWER_GENERATION_ECLIPSE_SW_PVCELLIDEAL_H
#define POWER_GENERATION_ECLIPSE_SW_PVCELLIDEAL_H

#include <cmath>
#include "PVCell.h"

using namespace std;

class PVCellIdeal : public PVCell {
public:
    PVCellIdeal(bool useLookup = true);
    double getCurrent(
            unsigned int numCells = 1,
            double voltage = 0,
            double irradiance = 0.001,
            double temperature = 0
    );
    string getModelType();
};

#endif //POWER_GENERATION_ECLIPSE_SW_PVCELLIDEAL_H
