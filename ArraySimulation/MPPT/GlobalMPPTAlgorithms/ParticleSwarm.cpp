//
// Created by mpran on 5/22/2023.
//

#include "ParticleSwarm.h"

Particle::Particle(float xPos, float vel) : xPos(xPos), vel(vel) {
    this->personalBest = 0.0f;
    this->personalBestVolt = 0.0f;
}

void Particle::changeXPos(float vel) {
    this->xPos += vel;
}

void Particle::changeVel(float newVel) {
    this->vel = newVel;
}

float Particle::getPBest() {
    return this->personalBest;
}

float Particle::getVoltBest() {
    return this->personalBestVolt;
}

float Particle::getXPos() {
    return this->xPos;
}

float Particle::getVel() {
    return this->vel;
}

void Particle::changePBest(float newBest, float newBestVolt) {
    this->personalBest = newBest;
    this->personalBestVolt = newBestVolt;
}

string Particle::toString() {
    string result = "Position: " + to_string(this->xPos) + "\nVelocity: " + to_string(this->vel) + "\nPersonal Best: " + to_string(this->personalBestVolt);
    return result;
}

ParticleSwarm::ParticleSwarm(int numCells, string MPPTLocalAlgoType, string strideType) : GlobalMPPTAlgorithm(numCells, "Particle Swarm", MPPTLocalAlgoType, strideType){
    gBest = 0;
    gBestVolt = 0;
    goForward = true;
    _setup = true;
    startLocal = true;
    kick = true;
    totalCycle = 0;
    float interval = GlobalMPPTAlgorithm::MAX_VOLTAGE / 5;
    for(int i = 0; i < ParticleSwarm::NUM_AGENTS; ++i) {
        float xPos = (static_cast<float>(rand()) / RAND_MAX) * interval + interval * i;
        agents.push_back(new Particle(xPos, 0.0f));
    }
}

float ParticleSwarm::getVelocityVector(Particle* agent) {
    float r1 = static_cast<float>(rand()) / RAND_MAX;
    float r2 = static_cast<float>(rand()) / RAND_MAX;

    float newVel = ParticleSwarm::W * agent->getVel() +
                   ParticleSwarm::C1 * r1 * (agent->getVoltBest() - agent->getXPos()) +
                   ParticleSwarm::C2 * r2 * (this->gBestVolt - agent->getXPos());

    return newVel;
}

float ParticleSwarm::setUp(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float agentPower = arrVoltage * arrCurrent;
    float vRef;

    if(this->cycle == -1) {
        this->cycle = 0;
        this->totalCycle += 1;
        vRef = this->agents[0]->getXPos();
    } else if(this->cycle == 0 && this->_setup) {
        if(agentPower > this->agents[0]->getPBest()) {
            this->agents[0]->changePBest(agentPower, arrVoltage);
        }
        if(agentPower > this->gBest) {
            this->gBest = agentPower;
            this->gBestVolt = arrVoltage;
        }
        this->cycle += 1;
        this->totalCycle += 1;
        vRef = this->agents[1]->getXPos();
    } else if(this->cycle == 1 && this->_setup) {
        if(agentPower > this->agents[1]->getPBest()) {
            this->agents[1]->changePBest(agentPower, arrVoltage);
        }
        if(agentPower > this->gBest) {
            this->gBest = agentPower;
            this->gBestVolt = arrVoltage;
        }
        this->totalCycle += 1;
        this->cycle += 1;
        vRef = this->agents[2]->getXPos();
    } else if(this->cycle == 2 && this->_setup) {
        if(agentPower > this->agents[2]->getPBest()) {
            this->agents[2]->changePBest(agentPower, arrVoltage);
        }
        if(agentPower > this->gBest) {
            this->gBest = agentPower;
            this->gBestVolt = arrVoltage;
        }
        this->cycle += 1;
        this->totalCycle += 1;
        vRef = this->agents[3]->getXPos();
    } else if(this->cycle == 3 && this->_setup) {
        if(agentPower > this->agents[3]->getPBest()) {
            this->agents[3]->changePBest(agentPower, arrVoltage);
        }
        if(agentPower > this->gBest) {
            this->gBest = agentPower;
            this->gBestVolt = arrVoltage;
        }
        this->totalCycle += 1;
        this->cycle = 2;
        this->_setup = false;
        this->goForward = false;
        vRef = this->agents[2]->getXPos();
    }

    return vRef;
}

float ParticleSwarm::agentUpdate(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float vRef = arrVoltage;
    if (this->_setup) {
        vRef = this->setUp(arrVoltage, arrCurrent, irradiance, temperature);
    } else {
        float agentPower = arrVoltage * arrCurrent;
        float newVel;
        if (this->cycle == 0) {
            if (agentPower > this->agents[0]->getPBest()) {
                this->agents[0]->changePBest(agentPower, arrVoltage);
            }
            if (agentPower > this->gBest) {
                this->gBest = agentPower;
                this->gBestVolt = arrVoltage;
            }
            newVel = this->getVelocityVector(this->agents[0]);
            this->agents[0]->changeXPos(newVel);
            this->agents[0]->changeVel(newVel);
            this->goForward = true;
            this->cycle = 1;
            this->totalCycle++;
            vRef = this->agents[1]->getXPos();
        } else if (this->cycle % 4 == 1) {
            if (agentPower > this->agents[1]->getPBest()) {
                this->agents[1]->changePBest(agentPower, arrVoltage);
            }
            if (agentPower > this->gBest) {
                this->gBest = agentPower;
                this->gBestVolt = arrVoltage;
            }
            newVel = this->getVelocityVector(this->agents[1]);
            this->agents[1]->changeXPos(newVel);
            this->agents[1]->changeVel(newVel);
            if (this->goForward) {
                vRef = this->agents[2]->getXPos();
                this->cycle = 2;
            } else {
                vRef = this->agents[0]->getXPos();
                this->cycle = 0;
            }
            this->totalCycle++;
        } else if (this->cycle % 4 == 2) {
            if (agentPower > this->agents[2]->getPBest()) {
                this->agents[2]->changePBest(agentPower, arrVoltage);
            }
            if (agentPower > this->gBest) {
                this->gBest = agentPower;
                this->gBestVolt = arrVoltage;
            }
            newVel = this->getVelocityVector(this->agents[2]);
            this->agents[2]->changeXPos(newVel);
            this->agents[2]->changeVel(newVel);
            if (this->goForward) {
                vRef = this->agents[3]->getXPos();
                this->cycle = 3;
            } else {
                vRef = this->agents[1]->getXPos();
                this->cycle = 1;
            }
            this->totalCycle++;
        } else if (this->cycle % 4 == 3) {
            if (agentPower > this->agents[3]->getPBest()) {
                this->agents[3]->changePBest(agentPower, arrVoltage);
            }
            if (agentPower > this->gBest) {
                this->gBest = agentPower;
                this->gBestVolt = arrVoltage;
            }
            newVel = this->getVelocityVector(this->agents[3]);
            this->agents[3]->changeXPos(newVel);
            this->agents[3]->changeVel(newVel);
            vRef = this->agents[2]->getXPos();
            this->cycle = 2;
            this->totalCycle++;
            this->goForward = false;
        }
    }
    return vRef;
}

float ParticleSwarm::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float vRef;
    if (this->totalCycle <= 45) {
        vRef = this->agentUpdate(arrVoltage, arrCurrent, irradiance, temperature);
    } else {
        if (this->startLocal) {
            this->model.setup(this->gBestVolt, 0, GlobalMPPTAlgorithm::MAX_VOLTAGE);
            vRef = this->gBestVolt;
            this->startLocal = false;
        } else if (this->kick) {
            vRef = arrVoltage + 0.02;
            this->kick = false;
            this->vOld = arrVoltage;
            this->pOld = arrCurrent * arrVoltage;
            this->model.strideModel.vOld = arrVoltage;
            this->model.strideModel.pOld = this->pOld;
            this->iOld = arrCurrent;
        } else {
            vRef = this->model.getReferenceVoltage(arrVoltage, arrCurrent, irradiance, temperature);
            bool needsChange = this->checkEnvironmentalChanges(irradiance);
            if (needsChange) {
                this->gBest = 0.0;
                this->gBestVolt = 0.0;
                this->agents.clear();
                this->runningHistory.clear();
                this->goForward = true;
                this->_setup = true;
                this->startLocal = true;
                this->kick = true;
                this->totalCycle = 0;
                float interval = GlobalMPPTAlgorithm::MAX_VOLTAGE / 5;
                for (int i = 0; i < ParticleSwarm::NUM_AGENTS; i++) {
                    this->agents.push_back(new Particle((rand() / (float)RAND_MAX * interval) + (interval * i), 0.0));
                }
                this->cycle = -1;
            }
            this->totalCycle++;
        }
    }
    return vRef;
}

ParticleSwarm::~ParticleSwarm() {
    for(auto agent : agents) {
        delete agent;
    }
}

void ParticleSwarm::reset() {
    this->gBest = 0.0;
    this->gBestVolt = 0.0;
    this->goForward = true;
    this->_setup = true;
    this->startLocal = true;
    this->kick = true;
    this->totalCycle = 0;
    float interval = GlobalMPPTAlgorithm::MAX_VOLTAGE / 5;
    this->agents.clear();
    for (int i = 0; i < ParticleSwarm::NUM_AGENTS; i++) {
        this->agents.push_back(new Particle((rand() / (float)RAND_MAX * interval) + (interval * i), 0.0));
    }
    this->cycle = -1;
    for (Particle* p : this->agents) {
        std::cout << p->getXPos() << std::endl;
    }
}