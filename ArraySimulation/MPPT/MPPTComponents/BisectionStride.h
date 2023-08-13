#ifndef POWER_GENERATION_ECLIPSE_SW_BISECTIONSTRIDE_H
#define POWER_GENERATION_ECLIPSE_SW_BISECTIONSTRIDE_H

#include "Stride.h"

class BisectionStride : public Stride{
public:
    float slopeMultiplier;
    float minPowDiff;
    float minVoltDiff;
    BisectionStride(float minStride = 0.01, float VMPP = 0.621, float error = 0.05, float slopeMultiplier = 0.01);
    float getStride(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    ~BisectionStride();
};

#endif //POWER_GENERATION_ECLIPSE_SW_BISECTIONSTRIDE_H
