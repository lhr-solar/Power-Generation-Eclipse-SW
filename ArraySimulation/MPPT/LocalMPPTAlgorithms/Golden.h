#ifndef POWER_GENERATION_ECLIPSE_SW_GOLDEN_H
#define POWER_GENERATION_ECLIPSE_SW_GOLDEN_H

#include "LocalMPPTAlgorithm.h"
#include <cmath>
#include <stdexcept>

class Golden : public LocalMPPTAlgorithm{
public:
    float powerL1;
    float powerL2;
    float l1;
    float l2;
    float phi = (sqrt(5) + 1) / 2 - 1;
    Golden(int numCells = 1, string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
    ~Golden();
};

#endif //POWER_GENERATION_ECLIPSE_SW_GOLDEN_H
