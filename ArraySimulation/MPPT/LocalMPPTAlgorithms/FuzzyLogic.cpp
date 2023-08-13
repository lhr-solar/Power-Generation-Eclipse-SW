/*
 * Author: Praneel Murali, Matthew Yu.
Contact: matthewjkyu@gmail.com
Created: 5/14/22
Last Modified: 5/14/22

Description: Implementation of the Fuzzy Logic algorithm.
  The Fuzzy Logic class is a derived class of LocalMPPTAlgorithm.
    This particular verstion attempts to replicate Takun et al and has two input variables:
    - change in power
    - change in current


    These two input variables are classified by their respective membership
    functions (MFs).

    The power membership function defines 5 terms
    - NB - Negative Big     | [, -10%]
    - NS - Negative Small   | (-10%, -3%]
    - ZE - Zero             | (-3%, 3%)
    - PS - Positive Small   | [3%, 10%)
    - PB - Positive Big     | [10%, ]

    And the current membership function defines 3 terms:
    - N - Negative          | [, -1%]
    - Z - Zero              | (-1%, 1%)
    - P - Positive          | [1%, ]

    The rule table for the juxtaposition of both MFs is as follows, and is
    strictly arbitrary. The output term is the change in the reference voltage.

    Fuzzy Rule         dP/dV
                  NB | NS | ZE | PS | PB
            N   | NB | NS | PS | PS | PB
    dI/dV   Z   | PB | PS | ZE | NS | NB
            P   | PB | PS | NS | NS | NB

    Where the output set corresponds to the following values:
    - NB - Negative Big     | -5%
    - NS - Negative Small   | -1%
    - ZE - Zero             | 0%
    - PS - Positive Small   | 1%
    - PB - Positive Big     | 5%

    Beyond the current scope of this validation and proof of concept paper are
    following additions:

    - The input variable set can be further expanded to include:
        - change in voltage
        - change in temperature
        - change in irradiance
    - The membership functions can have a wider set size, perhaps 5 rules per
      input.
    - The membership function shapes can also be varies (triangular, trapezoial,
      sigmoidal, etc).
    - The rule table values can be optimized using brute force automation
      testing and/or machine learning approaches.

    Fuzzy Logic utilizes the rule table to defuzzify the inputs and generate an
    output. This can be considered a form of adaptive hill climbing algorithm in
    that the  .

    , utilizing the change of power and change of voltage over
    time to determine the direction of movement and stride of the next reference
    voltage. It belongs to the classification of hill climbing algorithms.
 */

#include "FuzzyLogic.h"

FuzzyLogic::FuzzyLogic(int numCells, string strideType) {
    LocalMPPTAlgorithm(numCells, "Fuzzy Logic", strideType);
    cout << "HI" << endl;
    minVoltage = 0.05;
    maxVoltage = numCells * 0.721;
    maxPower = numCells * 3.63;
    maxCurrent = 6.15;
    start = true;
    dP = { {-100, -10}, {-10, -3}, {-3, 3}, {3, 10}, {10, 100} };
    dI = {{-100, -1}, {-1, 1}, {1, 100}};
    ruleset = {{1, 1, 1, 3, 4}, {3, 3, 2, 3, 4}, {4, 3, 3, 1, 1}};
    dV = {-0.04, -0.02, 0.01, 0.02, 0.04};
}

float FuzzyLogic::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float pIn = arrCurrent * arrVoltage;
    float diffV = arrVoltage - vOld;
    float diffI = arrCurrent - iOld;
    float diffP = pIn - pOld;

    cout << "V: " << arrVoltage << ", I: " << arrCurrent << ", P: " << arrVoltage * arrCurrent << endl;
    float vRef = arrVoltage;
    if(start == true){
        start = false;
        vRef = minVoltage;
    }else{
        int dPTerm = 2;
        int dITerm = 1;
        float dPPercentage = diffP * 100 / maxPower;
        float dIPercentage = diffI * 100 / maxCurrent;
        for(int i = 0; i < dP.size(); i++){
            if(dPPercentage > dP[i].first && dPPercentage <= dP[i].second){
                dPTerm = i;
                break;
            }
        }
        for(int i = 0; i < dI.size(); i++){
            if(dIPercentage > dI[i].first && dIPercentage <= dI[i].second){
                dITerm = i;
                break;
            }
        }
        cout << "Change in power: " << diffV << " | " << diffV / 100 * maxVoltage << endl;
        cout << "Change in current: " << diffI << " | " << dIPercentage << endl;
        cout << "Change in power: " << diffP << " | " << dPPercentage << endl;
        cout << "dP Rule: (" << dP[dPTerm].first << ", " << dP[dPTerm].second << ")" << endl;
        cout << "dI Rule: (" << dI[dITerm].first << ", " << dI[dITerm].second << ")" << endl;
        auto rulesetIdx = ruleset[dITerm][dPTerm];
        auto vRefShift = dV[rulesetIdx];
        cout << "Voltage Shift: " << vRefShift << " | " << rulesetIdx << endl;
        vRef += vRefShift;
        cout << "New VREF: " << vRef << endl;
    }
    vOld = arrVoltage;
    iOld = arrCurrent;
    pOld = pIn;

    if(vRef >= maxVoltage){
        vRef = maxVoltage - 0.01;
    }
    return vRef;
}

FuzzyLogic::~FuzzyLogic() {

}