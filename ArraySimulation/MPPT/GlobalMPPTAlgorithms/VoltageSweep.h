#ifndef POWER_GENERATION_ECLIPSE_SW_VOLTAGESWEEP_H
#define POWER_GENERATION_ECLIPSE_SW_VOLTAGESWEEP_H

#include "GlobalMPPTAlgorithm.h"
#include <vector>
#include <algorithm>

class VoltageSweep : public GlobalMPPTAlgorithm{
public:
    vector<float> voltage_peaks;
    vector<float> voltage_troughs;
    vector<float> power_peaks;
    bool sweeping;
    bool increasing;
    bool setup;
    float stride;
    VoltageSweep(int numCells = 1, string MPPTLocalAlgoType = "Default", string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    float _sweep(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    pair<float, float> _getBounds();
    void reset();
    ~VoltageSweep();
};

#endif //POWER_GENERATION_ECLIPSE_SW_VOLTAGESWEEP_H
