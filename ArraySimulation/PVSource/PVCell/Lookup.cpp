/*
 * Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 11/24/20

Description: The Lookup class is a concrete class that can ingest environmental
parameters to generate and read lookup tables for models that may take large
processing loads to compute. The expected output lookup tables are in CSV
format, and can be indexed (if one knows the indexing parameters) to quickly
reach any expected output value.

    The file is organized into the following columns:
        v_ref, irradiance, temperature, current

    Every entry should be unique.

    The file is sorted in increasing order by leftmost column priority.
        That is:
        v   |   irr |   temp|   current
        ---------------------------------------
        0   ,   0   ,   0   ,   X
        0   ,   0   ,   0   ,   X
        0   ,   0   ,   0.1 ,   X
        0   ,   0   ,   0.2 ,   X
        0   ,   1.0 ,   10  ,   X
        0   ,   1.0 ,   12  ,   X
        0   ,   1.0 ,   15  ,   X
        ... and so on.

    We can ignore sorting and insertion costs if we insert in order with a clever
    source building scheme. Retrieval is reduced to an O(1) lookup.

    We can also reduce the constraints of our minimum resolution if we
    interpolate our data across each independent variable. This is a semi hard
    problem that can be resolved. An example procedure would be to check which
    parameters are finer grained than the built resolution, and search for 2^N
    points on the lookup with the two closest resolved solutions for each
    parameter.

    For example, given              and our lookup resolution is:
        V = 0.1,                        V = 1,
        IRRAD = 1000,                   IRRAD = 1,
        TEMP = 25                       TEMP = 1

    We see that the relevant V entry will not exist in the lookup table.
    We can then take the nearest neighbor points:
    P1  V = 0,          P2  V = 1,
        IRRAD = 1000,       IRRAD = 1000,       P1 -o-------- P2
        TEMP = 25           TEMP = 25

    And interpolate between the two. We could take the average of the points or
    do a quadratic interpolation and so on...

    For two variables that are beyond our resolution:
    For example, given              and our lookup resolution is:
        V = 0.1,                        V = 1,
        IRRAD = 1000.5,                 IRRAD = 1,
        TEMP = 25                       TEMP = 1

    The nearest neighbor points are:
    P1  V = 0,          P2  V = 0,          P3  V = 1,          P4  V = 1,
        IRRAD = 1000,       IRRAD = 1001,       IRRAD = 1000,       IRRAD = 1001,
        TEMP = 25           TEMP = 25           TEMP = 25           TEMP = 25

        P1 -------- P3
         |          |
         |          |
         |  o       |
         |          |
         |          |
        P2 -------- P4

    Interpolation will be similar here, although with an extra dimension. This
    can become complex fast with many independent variables that are beyond the
    listed resolution.
 */

#include "Lookup.h"
#include <fstream>
#include <sstream>
#include <cmath>
#include <stdexcept>

Lookup::Lookup(
        std::vector<std::tuple<double, int>> parameters,
        std::vector<std::string> header,
        std::string filename
) {
    this->parameters = parameters;
    this->header = header;
    this->filename = filename;
    multiplier = 1;
    for (auto param : parameters) {
        multiplier *= std::get<1>(param);
    }
}

void Lookup::addLine(const std::vector<double>& line) {
    data.push_back(line);
}

std::vector<double> Lookup::lookup(const std::vector<double>& params) {
    int idx = 1;
    std::vector<int> paramIndices;
    for (int count = 0; count < params.size(); ++count) {
        int paramIdx = static_cast<int>(round(params[count] / std::get<0>(parameters[count])));
        paramIndices.push_back(paramIdx);
        if (paramIdx < 0 || paramIdx >= std::get<1>(parameters[count])) {
            throw std::out_of_range("Parameters are out of bounds of the data.");
        }
    }

    int multiplier = this->multiplier;
    for (int count = 0; count < paramIndices.size(); ++count) {
        multiplier /= std::get<1>(parameters[count]);
        idx += paramIndices[count] * multiplier;
    }
    return data[idx];
}

void Lookup::writeFile() {
    std::ofstream csv_file(fileRoot + filename);
    for (int i = 0; i < header.size(); ++i) {
        csv_file << header[i];
        if (i < header.size() - 1) {
            csv_file << ",";
        }
    }
    csv_file << "\n";
    for (const auto& line : data) {
        for (int i = 0; i < line.size(); ++i) {
            csv_file << line[i];
            if (i < line.size() - 1) {
                csv_file << ",";
            }
        }
        csv_file << "\n";
    }
}

void Lookup::readFile() {
    data.clear();
    std::ifstream csv_file(fileRoot + filename);
    std::string line;
    std::getline(csv_file, line);
    while (std::getline(csv_file, line)) {
        std::istringstream ss(line);
        std::string field;
        std::vector<double> row;
        while (std::getline(ss, field, ',')) {
            row.push_back(std::stod(field));
        }
        data.push_back(row);
    }
}