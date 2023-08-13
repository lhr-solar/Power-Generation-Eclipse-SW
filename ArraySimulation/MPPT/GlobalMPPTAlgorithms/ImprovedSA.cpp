/*
 * Author: Praneel Murali, Afnan Mir, Array Lead (2021).
Contact: afnanmir@utexas.edu
Created: 04/10/2021
Last Modified: 09/25/2021

Description: Implementation of an improved simulated annealing algorithm as an extension of GlobalMPPTAlgortihm.

    The Simulated Annealing class is a derived concrete class of GlobalAlgorithm
    implementing the Simulated Annealing algorithm. It randomly samples values from
    the range of voltages and chooses the operating point of the voltage either if the power
    at the sampled point is greater than the power of the current operating point, or based
    on a calculated probability. It then identifies the global maxima using a LocalMPPTAlgorithm.
 */

#include "ImprovedSA.h"

ImprovedSA::ImprovedSA(int numCells, string MPPTLocalAlgoType, string strideType) :
    GlobalMPPTAlgorithm(numCells, "Improved SA", MPPTLocalAlgoType, strideType){

    temp = INIT_TEMP;
    cycle = 0;
    startLocal = true;
    kick = true;
}

float ImprovedSA::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    float vRef = arrVoltage;
    if(temp > 0.2){
        if(cycle == 0){
            vRef = round(static_cast<float>(rand()) / RAND_MAX * MAX_VOLTAGE * 100) / 100;
            cycle += 1;
            vOld = arrVoltage;
            iOld = arrCurrent;
            pOld = arrVoltage * arrCurrent;
            irrOld = irradiance;
            tOld = temperature;
        }else if(cycle == 1){
            vOld = arrVoltage;
            iOld = arrCurrent;
            irrOld = irradiance;
            tOld = temperature;
            cycle += 1;
        }else{
            float arrPower = arrVoltage * arrCurrent;
            if(arrPower > pOld){
                vOld = arrVoltage;
                pOld = arrPower;
                iOld = arrCurrent;
                vRef = arrVoltage;
            }else{
                float p_r = exp((arrPower - pOld) / temp);
                cout << "pOld: " << pOld << " arrPower: " << arrPower << " temp: " << temp << endl;
                cout << p_r << endl;
                double diceRoll = static_cast<double>(rand()) / RAND_MAX;
                if (diceRoll < p_r){
                    vOld = arrVoltage;
                    pOld = arrPower;
                    iOld = arrCurrent;
                    vRef = arrVoltage;
                }
            }
            if(fmod(cycle , 4) == 0){
                temp = temp * ALPHA;
                cout << "Temp: " << temp << endl;
            }
            cycle += 1;
            vRef = round(static_cast<double>(rand()) / RAND_MAX * MAX_VOLTAGE * 100) / 100;
        }
    }else{
        if(startLocal){
            vRef = vOld;
            startLocal = false;
            model.setup(vOld, 0, MAX_VOLTAGE);
        }else if(kick){
            vRef = arrVoltage + 0.02;
            kick = false;
            vOld = arrVoltage;
            pOld = arrVoltage * arrCurrent;
            model.strideModel.vOld = arrVoltage;
            model.strideModel.pOld = pOld;
            iOld = arrCurrent;
        }else{
            vRef = model.getReferenceVoltage(arrVoltage, arrCurrent, irradiance, temperature);
            /*
             * needsChange = self.checkEnvironmentalChanges(irradiance)
                print(self.runningHistory)
                if needsChange:
                    vRef = 0
                    self.cycle = 0
                    self.temp = ImprovedSA.INIT_TEMP
                    self.startLocal = True
                    self.kick = True
                    self.runningHistory.clear()
                    return vRef
             */
        }
    }
    return vRef;
}

void ImprovedSA::reset() {
    GlobalMPPTAlgorithm::reset();
    temp = INIT_TEMP;
    cycle = 0;
    startLocal = true;
    kick = true;
}