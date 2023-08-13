#ifndef POWER_GENERATION_ECLIPSE_SW_FUZZYLOGIC_H
#define POWER_GENERATION_ECLIPSE_SW_FUZZYLOGIC_H

#include "LocalMPPTAlgorithm.h"
#include <vector>
#include <map>

class FuzzyLogic : public LocalMPPTAlgorithm{
public:
    float minVoltage;
    float maxVoltage;
    float maxPower;
    float maxCurrent;
    bool start;
    vector<pair<int, int>> dP;
    vector<pair<int, int>> dI;
    vector<vector<int>> ruleset;
    vector<double> dV;
    FuzzyLogic(int numCells = 1, string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    ~FuzzyLogic();
};

#endif //POWER_GENERATION_ECLIPSE_SW_FUZZYLOGIC_H
