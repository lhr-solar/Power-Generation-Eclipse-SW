#ifndef POWER_GENERATION_ECLIPSE_SW_FIREFLY_H
#define POWER_GENERATION_ECLIPSE_SW_FIREFLY_H

#include <cmath>
#include <vector>
#include "GlobalMPPTAlgorithm.h"

class Firefly{
public:
    int B_0 = 1;
    int N = 2;
    int GAMMA = 2;
    float ALPHA = 0.5;
    float position;
    float brightness;
    Firefly(float pos = 0.0);
    float getPosition();
    float getBrightness();
    float getAttractionLevel(Firefly* other);
    float getNextPosition(Firefly* other);
    ~Firefly();
};

class FireflyAlgorithm : public GlobalMPPTAlgorithm{
public:
    int NUM_FIREFLIES = 6;
    vector<Firefly> fireflies;
    bool startLocal;
    bool _setup;
    bool kick;
    FireflyAlgorithm(int numCells = 1, string MPPTLocalAlgoType = "Default", string strideType = "Fixed");
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
    ~FireflyAlgorithm();
};

#endif //POWER_GENERATION_ECLIPSE_SW_FIREFLY_H
