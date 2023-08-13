#ifndef POWER_GENERATION_ECLIPSE_SW_ADAPTIVESTRIDE_H
#define POWER_GENERATION_ECLIPSE_SW_ADAPTIVESTRIDE_H
#include "Stride.h"

class AdaptiveStride : public Stride{
public:
    AdaptiveStride(float minStride = 0.01, float VMPP = 0.621, float error = 0.05);
    float getStride(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    ~AdaptiveStride();
};

#endif //POWER_GENERATION_ECLIPSE_SW_ADAPTIVESTRIDE_H
