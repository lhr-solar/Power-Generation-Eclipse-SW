#ifndef POWER_GENERATION_ECLIPSE_SW_LOCALMPPTALGORITHM_H
#define POWER_GENERATION_ECLIPSE_SW_LOCALMPPTALGORITHM_H

#include "AdaptiveStride.h"
#include "BisectionStride.h"
#include "OptimalStride.h"
#include "Stride.h"

static float MAX_VOLTAGE = 100;
static float MAX_VOLTAGE_PER_CELL = 0.8;

class LocalMPPTAlgorithm{
public:
    int numCells;
    string MPPTLocalAlgoType;
    float leftBound;
    float rightBound;
    Stride strideModel;
    string strideType;
    float minStride;
    float VMPP;
    float error;
    float vOld;
    float iOld;
    float pOld;
    float irrOld;
    float tOld;
    int cycle;
    LocalMPPTAlgorithm(int numCells = 1, string MPPTLocalAlgoType = "Default", string strideType = "Fixed");
    void setup(float VMPP = 0.621, float leftBound = 0, float rightBound = MAX_VOLTAGE);
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
    string getLocalMPPTType();
    string getStrideType();
    ~LocalMPPTAlgorithm();
};

#endif //POWER_GENERATION_ECLIPSE_SW_LOCALMPPTALGORITHM_H
