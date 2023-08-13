/*
 * Author: Praneel Murali, Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 08/08/2021
Last Modified: 09/25/2021

Description: Implementation of Firefly Global Maximum Power Point Tracking Algortihm.
 */
#include "Firefly.h"

Firefly::Firefly(float pos) {
    position = pos;
    brightness = 0;
}

float Firefly::getPosition() {
    return position;
}

float Firefly::getBrightness() {
    return brightness;
}

float Firefly::getAttractionLevel(Firefly* other) {
    float r_pq = abs(position - other->position);
    return B_0 * exp(-1 * GAMMA * (r_pq * r_pq));
}

float Firefly::getNextPosition(Firefly *other) {
    float beta = getAttractionLevel(other);
    float dist = position - other->position;
    float newPos = position + beta * dist + ALPHA * (static_cast<float>(rand()) / static_cast<float>(RAND_MAX) - 0.5);
    return newPos;
}

FireflyAlgorithm::FireflyAlgorithm(int numCells, string MPPTLocalAlgoType,string strideType) {
    GlobalMPPTAlgorithm(numCells, "Firefly", MPPTLocalAlgoType, strideType);
    fireflies.reserve(6);
    fireflies.resize(6);
    float interval = GlobalMPPTAlgorithm::MAX_VOLTAGE / (NUM_FIREFLIES + 1);
    for (int i = 0; i < NUM_FIREFLIES; ++i) {
        fireflies.push_back(Firefly(interval * i));
    }
    startLocal = true;
    _setup = true;
    kick = true;
}

float FireflyAlgorithm::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    return arrVoltage;
}

void FireflyAlgorithm::reset() {
    return;
}

Firefly::~Firefly() {

}