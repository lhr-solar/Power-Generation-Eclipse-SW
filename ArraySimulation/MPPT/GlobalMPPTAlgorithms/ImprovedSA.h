#ifndef POWER_GENERATION_ECLIPSE_SW_IMPROVEDSA_H
#define POWER_GENERATION_ECLIPSE_SW_IMPROVEDSA_H

#include "GlobalMPPTAlgorithm.h"
#include "stdlib.h"
#include "cmath"

class ImprovedSA : public GlobalMPPTAlgorithm{
public:
    float ALPHA = 0.75;
    float INIT_TEMP = 25;
    float MIN_TEMP = 0.4;
    float N_S = 6;
    float INIT_STEP = 0.8;
    float N_T = 3;
    float k = 15;
    float temp;
    float cycle;
    bool startLocal;
    bool kick;
    ImprovedSA(int numCells = 1, string MPPTLocalAlgoType = "Default", string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
    ~ImprovedSA();
};

#endif //POWER_GENERATION_ECLIPSE_SW_IMPROVEDSA_H
