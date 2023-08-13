/*
 * Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 11/24/20

Description: The PVSource (Photovoltaic Cell/Module/Subarray) class is a
concrete base class that provides a common API for derived classes to use. The
PVCell class enables users to retrieve information of the PV model, such as
IV curves, maximum power points, and so on given a set of input conditions.

The following paper discusses how to model multiple module PV sources with
variable shading:

    Accurate Modeling of Partially Shaded PV Arrays (Meyers
    et Mikofski)

    A library developed by these authors is called PVMismatch;
    it can be found at [https://github.com/SunPower/PVMismatch].
    We can potentially draw inspiration on this work to build
    PVSource (This is very hard, since I don't understand their
    code!)

    Attribution of the library:

    Mark Mikofski, Bennet Meyers, Chetan Chaudhari (2018).
    “PVMismatch Project: https://github.com/SunPower/PVMismatch".
    SunPower Corporation, Richmond, CA.
 */
#include "PVSource.h"
#include "stdexcept"
#include <algorithm>
#include <cmath>


PVSource::PVSource(){
    MAX_CELL_VOLTAGE = 0.8;
    MAX_CURRENT = 8;
    MIN_CURRENT = 0;
    _modelType = "";
    _useLookup = false;
}

void PVSource::setupModel(string modelType, bool useLookup){
    _modelType = modelType;
    _useLookup = useLookup;

    if (modelType == "Ideal") {
        _model = make_unique<PVCellIdeal>(useLookup);
    } else if (modelType == "Nonideal") {
        _model = make_unique<PVCellNonIdeal>(useLookup);
    } else {
        _model = nullptr;
    }
}

float PVSource::getModuleCurrent(ModuleDef moduleDef) {
    if (_model) {
        if (_useLookup) {
            return _model->getCurrentLookup(moduleDef.numCells, moduleDef.voltage, moduleDef.irradiance, moduleDef.temperature);
        } else {
            return _model->getCurrent(moduleDef.numCells, moduleDef.voltage, moduleDef.irradiance, moduleDef.temperature);
        }
    } else {
        throw runtime_error("No cell model is defined for the PVSource.");
    }
}

float PVSource::getSourceCurrent(map<int, ModuleDef> modulesDef) {
    if (_model) {
        map<int, double> moduleCurrents;
        for (auto itr = modulesDef.begin(); itr != modulesDef.end(); ++itr) {
            int moduleKey = itr->first;
            ModuleDef moduleVals = itr->second;
            moduleCurrents[moduleKey] = getModuleCurrent(moduleVals);
        }

        vector<pair<int, double>> moduleCurrentsSorted(moduleCurrents.begin(), moduleCurrents.end());
        sort(moduleCurrentsSorted.begin(), moduleCurrentsSorted.end(),
                  [](pair<int, double> a, pair<int, double> b) { return a.second > b.second; });

        vector<double> currents;
        int curCellNum = 0;
        for (auto itr = moduleCurrentsSorted.begin(); itr != moduleCurrentsSorted.end(); ++itr) {
            int moduleKey = itr->first;
            ModuleDef module = modulesDef[moduleKey];
            ModuleDef modifiedModule;
            modifiedModule.numCells = module.numCells + curCellNum;
            modifiedModule.voltage = module.voltage;
            modifiedModule.irradiance = module.irradiance;
            modifiedModule.temperature = module.temperature;
            currents.push_back(getModuleCurrent(modifiedModule));
            curCellNum += module.numCells;
        }

        double current = *max_element(currents.begin(), currents.end()) * (1 - exp(-1000));
        return current;
    } else {
        throw runtime_error("No cell model is defined for the PVSource.");
    }
}

vector<tuple<float, float>> PVSource::getIV(map<int, ModuleDef> modulesDef, int numCells, float resolution) {
    vector<tuple<float, float>> model;
    if (_model) {
        for (double voltage = 0; voltage <= (round(MAX_CELL_VOLTAGE * numCells * 100) / 100) + 0.01; voltage += 0.01) {
            for (auto itr = modulesDef.begin(); itr != modulesDef.end(); ++itr) {
                itr->second.voltage = voltage;
            }
            double current = getSourceCurrent(modulesDef);
            model.push_back({voltage, current});
        }
        return model;
    } else {
        throw runtime_error("No cell model is defined for the PVSource.");
    }
}

tuple<float, float, tuple<float, float>> PVSource::getEdgeCharacteristics(map<int, ModuleDef> modulesDef, int numCells, float resolution) {
    if (_model) {
        pair<float, float> mpp = make_pair(0, 0);  // voltage, current
        float OCVoltage = 0.0f;

        if (resolution <= 0)
            resolution = 0.01;

        vector<tuple<float, float>> model = getIV(modulesDef, numCells, resolution);

        if (!model.empty()) {
            float SCCurrent = get<1>(model[0]);  // Current in first entry
            for (auto itr = model.begin(); itr != model.end(); ++itr) {
                float voltage = get<0>(*itr);
                float current = get<1>(*itr);
                if (mpp.first * mpp.second < voltage * current) {
                    mpp.first = voltage;
                    mpp.second = current;
                }
                if (OCVoltage != 0.0f && current == 0)
                    OCVoltage = voltage;
            }
            return make_tuple(OCVoltage, SCCurrent, mpp);
        } else {
            return make_tuple(0.0f, 0.0f, make_pair(0.0f, 0.0f));
        }
    } else {
        throw runtime_error("No cell model is defined for the PVSource.");
    }
}

string PVSource::getModelType() {
    return this->_modelType;
}