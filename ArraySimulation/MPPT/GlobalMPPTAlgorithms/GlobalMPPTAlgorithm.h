#ifndef POWER_GENERATION_ECLIPSE_SW_GLOBALMPPTALGORITHM_H
#define POWER_GENERATION_ECLIPSE_SW_GLOBALMPPTALGORITHM_H

#include "../LocalMPPTAlgorithms/LocalMPPTAlgorithm.h"
#include "../LocalMPPTAlgorithms/Bisection.h"
#include "../LocalMPPTAlgorithms/FC.h"
#include "../LocalMPPTAlgorithms/FuzzyLogic.h"
#include "../LocalMPPTAlgorithms/Golden.h"
#include "../LocalMPPTAlgorithms/IC.h"
#include "../LocalMPPTAlgorithms/PandO.h"
#include "../LocalMPPTAlgorithms/Ternary.h"
#include <cmath>

using namespace std;

class GlobalMPPTAlgorithm{
public:
    float MAX_VOLTAGE = 100;
    float MAX_VOLTAGE_PER_CELL = 0.8;
    string MPPTGlobalAlgoType;
    LocalMPPTAlgorithm model;
    float vOld;
    float iOld;
    float pOld;
    float irrOld;
    float tOld;
    GlobalMPPTAlgorithm(int numCells = 1,
                        string MPPTGlobalAlgoType = "Default",
                        string MPPTLocalAlgoType = "Default",
                        string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
    string getGlobalMPPTType();
    string getLocalMPPTType();
    string getStrideType();
    pair<float, float> _getBounds();
};


#endif //POWER_GENERATION_ECLIPSE_SW_GLOBALMPPTALGORITHM_H
