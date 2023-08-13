#ifndef POWER_GENERATION_ECLIPSE_SW_TERNARY_H
#define POWER_GENERATION_ECLIPSE_SW_TERNARY_H

#include "LocalMPPTAlgorithm.h"
#include <stdexcept>

class Ternary : public LocalMPPTAlgorithm{
public:
    float q = 0.33;
    float powerL1;
    float powerL2;
    float l1;
    float l2;
    Ternary(int numCells = 1, string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
    ~Ternary();
};

#endif //POWER_GENERATION_ECLIPSE_SW_TERNARY_H
