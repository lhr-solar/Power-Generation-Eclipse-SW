#ifndef POWER_GENERATION_ECLIPSE_SW_BISECTION_H
#define POWER_GENERATION_ECLIPSE_SW_BISECTION_H

#include "LocalMPPTAlgorithm.h"
#include <cmath>
#include <stdexcept>

class Bisection : public LocalMPPTAlgorithm{
public:
    Bisection(int numCells = 1, string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
    ~Bisection();
};

#endif //POWER_GENERATION_ECLIPSE_SW_BISECTION_H
