
#include "GlobalMPPTAlgorithm.h"

using namespace std;

GlobalMPPTAlgorithm::GlobalMPPTAlgorithm(int numCells, string MPPTGlobalAlgoType, string MPPTLocalAlgoType, string strideType) {
    float temp = MAX_VOLTAGE_PER_CELL * numCells * 100;
    MAX_VOLTAGE = round(temp) / 100;
    if (MPPTLocalAlgoType == "Bisection"){
        model = Bisection(numCells, strideType);
    }else if(MPPTLocalAlgoType == "FC"){
        model = FC(numCells, strideType);
    }else if(MPPTLocalAlgoType == "Golden"){
        model = Golden(numCells, strideType);
    }else if(MPPTLocalAlgoType == "IC"){
        model = IC(numCells, strideType);
    }else if(MPPTLocalAlgoType == "PandO"){
        model = PandO(numCells, strideType);
    }else if(MPPTLocalAlgoType == "Ternary"){
        model = Ternary(numCells, strideType);
    }else{
        model = LocalMPPTAlgorithm(numCells, MPPTLocalAlgoType, strideType);
    }
    vOld = 0.0;
    iOld = 0.0;
    tOld = 0.0;
    irrOld = 0.0;
    pOld = 0.0;
}

float GlobalMPPTAlgorithm::getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
    /*
     * Calculates the reference voltage output for the given PVSource output.
        May use prior history.

        Parameters
        ----------
        arrVoltage: float
            Array voltage in V.
        arrCurrent: float
            Array current in A.
        irradiance: float
            Irradiance in W/M^2 (G)
        temperature: float
            Cell Temperature in C.

        Return
        ------
        float The reference voltage that should be applied to the array in the
        next cycle.

        Assumptions
        -----------
        This method is called sequentially in increasing cycle order. The
        arrVoltage and arrCurrent are expected to have stabilized to the
        reference voltage applied in the last cycle, if any.

        Note that the second assumption doesn't hold true in reality, as large
        changes in reference voltage may mean the array does not converge to
        steady state behavior by the next MPPT cycle. This should always be
        considered in the algorithms.
     */

    float vRef = model.getReferenceVoltage(arrVoltage, arrCurrent, irradiance, temperature);
    pair<float, float> bounds = _getBounds();
    if(vRef < bounds.first){
        vRef = bounds.first;
    }else if(vRef > bounds.second){
        vRef = bounds.second;
    }
    return vRef;
}

void GlobalMPPTAlgorithm::reset() {
    model.reset();
    vOld = 0.0;
    iOld = 0.0;
    tOld = 0.0;
    irrOld = 0.0;
    pOld = 0.0;
}

string GlobalMPPTAlgorithm::getGlobalMPPTType() {
    return MPPTGlobalAlgoType;
}

string GlobalMPPTAlgorithm::getLocalMPPTType() {
    return model.getLocalMPPTType();
}

string GlobalMPPTAlgorithm::getStrideType() {
    return model.getStrideType();
}

pair<float, float> GlobalMPPTAlgorithm::_getBounds() {
    pair<float, float> bounds;
    bounds.first = 0.0;
    bounds.second = MAX_VOLTAGE;
    return bounds;
}