#ifndef POWER_GENERATION_ECLIPSE_SW_IC_H
#define POWER_GENERATION_ECLIPSE_SW_IC_H

#include "LocalMPPTAlgorithm.h"
#include <cmath>

class IC : public LocalMPPTAlgorithm{
public:
    float error = 0.01;
    IC(int numCells = 1, string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    ~IC();
};

#endif //POWER_GENERATION_ECLIPSE_SW_IC_H
