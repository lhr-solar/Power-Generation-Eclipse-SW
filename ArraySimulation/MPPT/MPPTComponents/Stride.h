#ifndef POWER_GENERATION_ECLIPSE_SW_STRIDE_H
#define POWER_GENERATION_ECLIPSE_SW_STRIDE_H
#include <iostream>
#include <string>

using namespace std;

class Stride{
public:
    Stride(string strideType = "Fixed", float minStride = 0.01, float VMPP = 0.621, float error = 0.05);
    void setup(float VMPP = 0.621, float error = 0.05); //was setup in Stride.py
    float getStride(float arrVoltage, float arrCurrent, float irradiance, float temperature);
    void reset();
    string getStrideType();
    string strideType;
    float minStride;
    float VMPP;
    float error;
    float vOld;
    float iOld;
    float pOld;
    float irrOld;
    float tOld;
    ~Stride();
};

#endif //POWER_GENERATION_ECLIPSE_SW_STRIDE_H
