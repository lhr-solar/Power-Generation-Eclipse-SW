//
// Created by mpran on 5/22/2023.
//

#ifndef POWER_GENERATION_ECLIPSE_SW_PARTICLESWARM_H
#define POWER_GENERATION_ECLIPSE_SW_PARTICLESWARM_H

#include <vector>
#include <random>
#include "GlobalMPPTAlgorithm.h"

using namespace std;

class Particle {
public:
    float personalBest;
    float personalBestVolt;
    float xPos;
    float vel;
    Particle(float xPos, float vel);
    void changeXPos(float vel);
    void changeVel(float newVel);
    float getPBest();
    float getVoltBest();
    float getXPos();
    float getVel();
    void changePBest(float newBest, float newBestVolt);
    string toString();
};

class ParticleSwarm : public GlobalMPPTAlgorithm {
public:
    static const int NUM_AGENTS = 4;
    static const float C1;
    static const float C2;
    static const float W;
    float gBest;
    float gBestVolt;
    vector<Particle*> agents;
    bool goForward;
    bool _setup;
    bool startLocal;
    bool kick;
    int totalCycle;
    int cycle;
    ParticleSwarm(int numCells=1, string MPPTLocalAlgoType="Default", string strideType="Fixed");
    float getVelocityVector(Particle* agent);
    float setUp(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    float agentUpdate(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
    ~ParticleSwarm();
};

#endif //POWER_GENERATION_ECLIPSE_SW_PARTICLESWARM_H
