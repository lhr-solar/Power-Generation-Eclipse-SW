#ifndef POWER_GENERATION_ECLIPSE_SW_SIMULATEDANNEALING_H
#define POWER_GENERATION_ECLIPSE_SW_SIMULATEDANNEALING_H

#include "GlobalMPPTAlgorithm.h"
#include "PVEnvironment.h"
#include "PVSource.h"

using namespace std;

class SimulatedAnnealing : public GlobalMPPTAlgorithm {
public:
    static const double ALPHA;
    static const double MIN_TEMP;
    static const double INIT_TEMP;
    static const int k;

    SimulatedAnnealing(int numCells=1, std::string MPPTLocalAlgoType="Default", std::string strideType="Fixed");

    double getReferenceVoltage(double arrVoltage, double arrCurrent, double irradiance, double temperature);
    void reset();
    double temp;
    int cycle;
    bool startLocal;
    PVEnvironment _PVEnv;
    PVSource _PVSource;
    vector<double> runningHistory;
    vector<double> pastHistories;
};

#endif //POWER_GENERATION_ECLIPSE_SW_SIMULATEDANNEALING_H
