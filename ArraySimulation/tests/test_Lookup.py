"""
test_Lookup.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/21/20
Last Modified: 10/21/20

Description: Test file to see if we can extract from a pre generated model file
and write to a new file using the Lookup class.
"""
# Library Imports.
import pytest
import sys

sys.path.append("../")

# Custom Imports.
from ArraySimulation.PVSource.PVCell.Lookup import Lookup


class TestLookup:
    def test_LookupRead(self):
        """
        Testing whether we can read data from the lookup with the correct input
        values.
        """
        print("Lookup read test.")

        lookup = Lookup(fileName="NonidealCellLookup.csv")
        lookup.readFile()

        try:
            assert lookup.lookup([0, 0.001, 0.001]) == [0.001]
            assert lookup.lookup([0, 50, 80.0]) == [0.318]
            assert lookup.lookup([0.6, 1000, 25.5]) == [3.162]
            assert lookup.lookup([0.8, 1000, 80]) == [0.001]

            # Failure cases.
            with pytest.raises(Exception) as excinfo:
                lookup.lookup([0.2, 1000, 80.5])
            assert (
                "Parameters are out of bounds of the data: 161 for 80.5 with max num entries 160"
                == str(excinfo.value)
            )

            with pytest.raises(Exception) as excinfo:
                lookup.lookup([0.2, 1050, 80.3])
            assert (
                "Parameters are out of bounds of the data: 21 for 1050 with max num entries 20"
                == str(excinfo.value)
            )
        except Exception as e:
            pytest.fail(e)

    def test_LookupWrite(self):
        """
        Testing whether we can write data to a file and extract it out the same
        way.
        """
        print("Lookup write and read test.")

        lookup = Lookup(fileName="TestLookup.csv")

        try:
            lookup.addLine([0, 0.001, 0.001, 0.1])
            lookup.addLine([0, 0.001, 0.5, 0.2])
            lookup.addLine([0, 0.001, 1.0, 0.3])
            lookup.addLine([0, 0.001, 1.5, 0.4])
            lookup.addLine([0, 0.001, 2.0, 0.5])
            lookup.addLine([0, 0.001, 2.5, 0.6])

            lookup.writeFile()
            lookup.readFile()
            assert lookup.lookup([0.0, 0.0, 0.0]) == [0.1]
            assert lookup.lookup([0.0, 0.0, 2.5]) == [0.6]
        except Exception as e:
            pytest.fail(e)
