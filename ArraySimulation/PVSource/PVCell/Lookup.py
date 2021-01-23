"""
Lookup.py

Author: Matthew Yu, Array Lead (2020).
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

    TODO: Interpolation.
"""
# Library Imports.
import csv
import os

# Custom Imports.


class Lookup:
    """
    The Lookup class is a concrete class that can ingest environmental
    parameters to generate and read lookup tables for models that may take large
    processing loads to compute. The expected output lookup tables are in CSV
    format, and can be indexed (if one knows the indexing parameters) to quickly
    reach any expected output value.
    """

    # Where all lookup files are located.
    _fileRoot = "./External/"

    def __init__(
        self,
        parameters=[(0.01, 81), (50, 21), (0.5, 161)],
        header=["v_ref (V)", "irrad (G)", "temp (C)", "current (A)"],
        fileName="model.csv",
    ):
        """
        Sets up the initial lookup parameters.
        The default parameters signify the following:
            voltage[0]:
                resolution: .01
                num entries: 81 ([0, .8] inclusive, in increments of .01)
            irradiance[1]:
                resolution: 50
                num entries: 21 ([0, 1000] inclusive, in increments of 50)
            temperature[2]: resolution: .5
                num entries: 161 ([0, 80] inclusive, in increments of .5)

        Parameters
        ----------
        parameters: List of tuples
            A list of tuples, where each tuple represents an independent
            variable.
            The tuple is in the format (float, int), where the first entry is
            the resolution and the second entry is the total number of entries.
        header: List of Strings
            The names of the columns (both independent and dependent variables)
            prepended before the data. Dependent variables should be last.
        fileName: String
            Name of the file to access or write to. Don't abuse the file name.
        """
        # Parameters used to access our lookup table.
        self._parameters = parameters
        self._multiplier = 1
        for param in parameters:
            self._multiplier *= param[1]

        # File header we check against to make sure we're looking at a properly
        # formatted file. Additionally also used for users to interpret the csv.
        if not isinstance(header, list):
            raise Exception("Header is not a list.")
        self._header = header

        # Name of the csv file containing the lookup table to perform operations on.
        self._filename = fileName

        self.data = []

    def addLine(self, line):
        """
        Writes a line of data to the internal buffer. Should be in the buffer
        format expected.

        Parameters
        ----------
        line: List [independent var 1, ind. var 2, ..., dependent var 1, ...]
            List of the parameters to append to the buffer. No sorting is done
            and is expected to be inserted in order described in the File
            Description.
        """
        self.data.append(line)

    def lookup(self, params):
        """
        Searches the internal buffer for the matching indices given by the
        parameter values. Indexing is interpolated from the values, a line in
        the file corresponding to the indices are found, and a value pops out!

        Dealing with problematic resolutions are not yet supported, but if they
        were, we'd probably call the lookup subroutine a 2^N times (N being the
        number of parameters that have over specified resolutions) and doing an
        interpolation between all of those results.

        Parameters
        ----------
        params: List of floats
            List of independent variables in column order to search.

        Return
        ------
        float: The resultant output given the input parameters.

        Assumptions
        -----------
        params must match the number of parameters specified at initialization.
        More specifically, the number of arguments should match and are in the
        same order.
        """
        idx = 1  # Start at one to ignore the header entry.
        paramIndices = []
        for count, param in enumerate(params):
            paramIdx = int(round(param / self._parameters[count][0]))
            paramIndices.append(paramIdx)
            if paramIdx < 0 or paramIdx >= self._parameters[count][1]:
                raise Exception(
                    "Parameters are out of bounds of the data: "
                    + str(paramIdx)
                    + " for "
                    + str(param)
                    + " with max num entries "
                    + str(self._parameters[count][1] - 1)
                )

        multiplier = self._multiplier
        for count, paramIdx in enumerate(paramIndices):
            multiplier /= self._parameters[count][1]
            idx += paramIdx * multiplier

        resultStr = self.data[int(idx)][len(self._parameters) : :]
        resultFloat = []
        for result in resultStr:
            resultFloat.append(float(result))

        return resultFloat

    def writeFile(self):
        """
        Writes accumulated data into the file.
        """
        with open(self._fileRoot + self._filename, "w", newline="\n") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self._header)
            for line in self.data:
                writer.writerow(line)

    def readFile(self):
        """
        Initializes an internal buffer with the contents of the file, parsed.
        Repeat calls just repeat the operation.
        """
        self.data = []
        with open(self._fileRoot + self._filename, "r", newline="\n") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self.data.append(row)
