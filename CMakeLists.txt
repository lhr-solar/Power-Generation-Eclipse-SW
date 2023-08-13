cmake_minimum_required(VERSION 3.24)
project(Power_Generation_Eclipse_SW)

set(CMAKE_CXX_STANDARD 14)

include_directories(ArraySimulation/MPPT)
include_directories(ArraySimulation/MPPT/GlobalMPPTAlgorithms)
include_directories(ArraySimulation/MPPT/MPPTComponents)

add_executable(Power_Generation_Eclipse_SW
        ArraySimulation/MPPT/GlobalMPPTAlgorithms/GlobalMPPTAlgorithm.cpp
        ArraySimulation/MPPT/GlobalMPPTAlgorithms/GlobalMPPTAlgorithm.h
        ArraySimulation/MPPT/MPPTComponents/AdaptiveStride.cpp
        ArraySimulation/MPPT/MPPTComponents/AdaptiveStride.h
        ArraySimulation/MPPT/MPPTComponents/Stride.cpp
        ArraySimulation/MPPT/MPPTComponents/Stride.h
        ArraySimulation/MPPT/MPPT.cpp
        ArraySimulation/MPPT/MPPT.h
        "src/source_models/Array Testing 9-14-19/Array Testing 9-14-19/ReadArrayFile.m" ArraySimulation/MPPT/GlobalMPPTAlgorithms/Firefly.h ArraySimulation/MPPT/GlobalMPPTAlgorithms/Firefly.cpp)
