//
// Created by mpran on 5/26/2023.
//

#ifndef POWER_GENERATION_ECLIPSE_SW_LOOKUP_H
#define POWER_GENERATION_ECLIPSE_SW_LOOKUP_H

#include <vector>
#include <string>
#include <tuple>

using namespace std;

class Lookup {
public:
    static constexpr char fileRoot[] = "./External/";
    vector<tuple<double, int>> parameters;
    int multiplier;
    vector<string> header;
    string filename;
    vector<vector<double>> data;
    Lookup(
            vector<tuple<double, int>> parameters = {{0.01, 81}, {50, 21}, {0.5, 161}},
            vector<string> header = {"v_ref (V)", "irrad (G)", "temp (C)", "current (A)"},
            string filename = "model.csv"
    );
    void addLine(const vector<double>& line);
    vector<double> lookup(const vector<double>& params);
    void writeFile();
    void readFile();
};

#endif //POWER_GENERATION_ECLIPSE_SW_LOOKUP_H
