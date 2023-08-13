#ifndef POWER_GENERATION_ECLIPSE_SW_OPTIMALSTRIDE_H
#define POWER_GENERATION_ECLIPSE_SW_OPTIMALSTRIDE_H

#include "Stride.h"

class OptimalStride : public Stride{
public:
    OptimalStride(float minStride = 0.01, float VMPP = 0.621, float error = 0.05);
    float getStride(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    ~OptimalStride();
};

#endif //POWER_GENERATION_ECLIPSE_SW_OPTIMALSTRIDE_H
