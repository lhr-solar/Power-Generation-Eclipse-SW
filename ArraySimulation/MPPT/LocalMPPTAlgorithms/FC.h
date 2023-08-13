#ifndef POWER_GENERATION_ECLIPSE_SW_FC_H
#define POWER_GENERATION_ECLIPSE_SW_FC_H

#include "LocalMPPTAlgorithm.h"

class FC : public LocalMPPTAlgorithm{
public:
    FC(int numCells = 1, string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    ~FC();
};

#endif //POWER_GENERATION_ECLIPSE_SW_FC_H
