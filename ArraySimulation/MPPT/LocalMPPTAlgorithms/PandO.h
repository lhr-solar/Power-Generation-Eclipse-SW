#ifndef POWER_GENERATION_ECLIPSE_SW_PANDO_H
#define POWER_GENERATION_ECLIPSE_SW_PANDO_H

#include "LocalMPPTAlgorithm.h"
#include <cmath>

class PandO : public LocalMPPTAlgorithm{
public:
    float minVoltage;
    PandO(int numCells = 1, string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    ~PandO();
};

#endif //POWER_GENERATION_ECLIPSE_SW_PANDO_H
