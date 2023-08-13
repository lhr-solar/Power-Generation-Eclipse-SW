/*
LocalMPPTAlgorithm.h

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/18/20
Last Modified: 02/27/22
Description: Implementation of the LocalMPPTAlgorithm class.
*/

#include "../MPPTComponents/Stride.h"
#include "../MPPTComponents/OptimalStride.h"
#include "../MPPTComponents/BisectionStride.h"
#include "../MPPTComponents/AdaptiveStride.h"
#include <iostream>
#include <string>

using namespace std;

class LocalMMPTAlgorithm{
public:

    /*
    The LocalMPPTAlgorithm class provides the base API for derived classes to
    calculate or predict voltage setpoints that would maximize the output power
    of the PVSource given a set of input conditions.
    */


    static const float MAX_VOLTAGE = 100;
    /*
    The upper voltage bound that should be predicted by any model. We expect
    the PV to always be at open circuit voltage at this point. Adjustable
    based on the number of cells determined from the initialization.
    */


    static const float MAX_VOLTAGE_PER_CELL = 0.8;
    /*
    The upper voltage bound for a single cell that should be predicted by any
    model. We expect the PV to always be at open circuit voltage at this
    point. The reference value was determined from experimentation from the
    Maxeon Gen III Bin Le1 solar cells, which have a rated voltage of .721V at
    standard conditions.
    */

    LocalMPPTAlgorithm(int numCells=1, string MPPTLocalAlgoType="Default", string strideType="Fixed") {
        LocalMPPTAlgorithm::MAX_VOLTAGE = numCells * LocalMPPTAlgorithm::MAX_VOLTAGE_PER_CELL;
        _MPPTLocalAlgoType = MPPTLocalAlgoType;

        if (strideType == "Adaptive") {
            _strideModel = new AdaptiveStride();
        }
        else if (strideType == "Bisection") {
            _strideModel = new BisectionStride();
        }
        else if (strideType == "Optimal") {
            _strideModel = new OptimalStride();
        }
        else {
            _strideModel = new Stride();
        }

        // Previous array voltage value.
        vOld = 0.0;

        // Previous array current voltage.
        iOld = 0.0;

        // Previous array power voltage.
        pOld = 0.0;

        // Previous array irradiance value.
        irrOld = 0.0;

        // Previous array temperature value.
        tOld = 0.0;

        // Bounds for the LocalMPPTAlgorithm. A naive assumption is that the
        // function within these bounds are unimodal.
        leftBound = 0;
        rightBound = LocalMPPTAlgorithm::MAX_VOLTAGE;
    }

    void setup(float VMPP=0.621, int leftBound=0, int rightBound=MAX_VOLTAGE) {
        this->leftBound = leftBound;
        this->rightBound = rightBound;
        _strideModel->setup(VMPP);
    }

    float getReferenceVoltage(float arrVoltage, float arrCurrent, float irradiance, float temperature) {
        return 0.0;
    }

    void reset() {
        _strideModel.reset();
        vOld = 0.0;
        iOld = 0.0;
        pOld = 0.0;
        irrOld = 0.0;
        tOld = 0.0;
        leftBound = 0;
        rightBound = LocalMPPTAlgorithm::MAX_VOLTAGE;
    }

    string getLocalMPPTType() {
        return _MPPTLocalAlgoType;
    }

    string getStrideType() {
        return _strideModel.getStrideType();
    }

protected:
    std::string _MPPTLocalAlgoType;
    double MAX_VOLTAGE;
    StrideModel _strideModel;
    double vOld;
    double iOld;
    double pOld;
    double irrOld;
    double tOld;
    double leftBound;
    double rightBound;
};
