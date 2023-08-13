#ifndef POWER_GENERATION_ECLIPSE_SW_PVSOURCE_H
#define POWER_GENERATION_ECLIPSE_SW_PVSOURCE_H

#include <map>
#include <string>
#include <tuple>
#include <vector>
#include <memory>
#include "PVCell/PVCellIdeal.h"
#include "PVCell/PVCellNonideal.h"

using namespace std;

class PVSource {
public:
    float MAX_CELL_VOLTAGE = 0.8f;
    float MAX_CURRENT = 8.0f;
    float MIN_CURRENT = 0.0f;
    struct ModuleDef {
        int numCells;
        float voltage;
        float irradiance;
        float temperature;
    };
    PVSource();
    void setupModel(string modelType = "Default", bool useLookup = true);
    float getModuleCurrent(ModuleDef moduleDef);
    float getSourceCurrent(map<int, ModuleDef> modulesDef);
    vector<tuple<float, float>> getIV(map<int, ModuleDef> modulesDef, int numCells, float resolution = 0.01);
    tuple<float, float, tuple<float, float>> getEdgeCharacteristics(map<int, ModuleDef> modulesDef, int numCells, float resolution = 0.01);
    string getModelType();
    unique_ptr<PVCell> _model;
    string _modelType;
    bool _useLookup;
    unique_ptr<PVCell> createPVCell(string modelType, bool useLookup);
};

#endif //POWER_GENERATION_ECLIPSE_SW_PVSOURCE_H
