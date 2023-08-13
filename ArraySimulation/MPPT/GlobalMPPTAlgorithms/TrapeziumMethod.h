#ifndef POWER_GENERATION_ECLIPSE_SW_TRAPEZIUMMETHOD_H
#define POWER_GENERATION_ECLIPSE_SW_TRAPEZIUMMETHOD_H

#include <cmath>
#include <vector>
#include "GlobalMPPTAlgorithm.h"

class TrapeziumMethod : public GlobalMPPTAlgorithm {
public:
    static const float DV;
    float pref;
    float aref;
    float vref;
    float aold;
    bool findingtrapezoids;
    bool startLocal;
    bool kick;
    std::vector<std::pair<float, std::pair<float, float>>> areas;

    TrapeziumMethod(int numCells = 1, std::string MPPTLocalAlgoType = "Default", std::string strideType = "Variable");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
};

#endif //POWER_GENERATION_ECLIPSE_SW_TRAPEZIUMMETHOD_H
