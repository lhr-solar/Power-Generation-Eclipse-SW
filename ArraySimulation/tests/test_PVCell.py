"""
test_PVCell.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/14/20
Last Modified: 10/21/20

Description: Test file to see if the various implemented models run as expected.
"""
# Library Imports.
import numpy as np
import pytest
import sys

sys.path.append("../")

# Custom Imports.
from ArraySimulation.PVSource.PVCell.PVCell import PVCell
from ArraySimulation.PVSource.PVCell.PVCellIdeal import PVCellIdeal
from ArraySimulation.PVSource.PVCell.PVCellNonideal import PVCellNonideal


class TestPVCell:
    def test_PVCellDefault(self):
        """
        Testing the default PVCell.
        """
        cell = PVCell()

        try:
            # Assert that we can get the default values for various function
            # calls.
            assert cell.getCurrent(0, 0, 0) == -1
            assert cell.getCurrentLookup(0, 0, 0) == -1
            assert cell.getCellIV(0, 0, 0) == []
            assert cell.getCellEdgeCharacteristics(0, 0, 0) == (0, 0, (0, 0))
            assert cell.getModelType() == "Default"
        except Exception as e:
            pytest.fail(str(e))

    def test_PVCellIdeal(self):
        """
        Testing the ideal PVCell model.
        """
        cell = PVCellIdeal()

        try:
            # Assert that we can get the default values for various function
            # calls.
            assert cell.getCurrent(0, 1000, 25) != -1
            assert cell.getCurrentLookup(0, 1000, 25) == -1
            assert cell.getCellIV(0.1, 1000, 25) != []
            assert cell.getCellEdgeCharacteristics(0.1, 1000, 25) != (0, 0, (0, 0))
            assert cell.getModelType() == "Ideal"
        except Exception as e:
            pytest.fail(str(e))

    def test_PVCellNonideal(self):
        """
        Testing the nonideal PVCell model.
        """
        cell = PVCellNonideal()

        try:
            # Assert that we can get the default values for various function
            # calls.
            assert cell.getCurrent(0, 1000, 25) != -1
            assert cell.getCurrentLookup(0, 1000, 25) == 6.146
            assert cell.getCurrent(0, 1000, 25) == cell.getCurrentLookup(
                0, 1000, 25
            )
            assert cell.getCellIV(0.1, 1000, 25) != []
            assert cell.getCellEdgeCharacteristics(0.1, 1000, 25) != (0, 0, (0, 0))
            assert cell.getModelType() == "Nonideal"
        except Exception as e:
            pytest.fail(str(e))

    def test_PVCellNonidealBuildLookup(self):
        """
        Test that we can build a lookup for the Nonideal Cell Model.
        """
        cell = PVCellNonideal()

        try:
            cell.buildCurrentLookup(
                voltageRes=0.1, irradianceRes=50, temperatureRes=5
            )
        except Exception as e:
            pytest.fail(str(e))

    @pytest.mark.additional
    def test_PVCellNonidealBuildLookupLong(self):
        """
        Test that we can build a lookup for the Nonideal Cell Model.
        This test version should match that in NonidealCellLookup.csv.
        """
        cell = PVCellNonideal()

        try:
            cell.buildCurrentLookup(
                voltageRes=0.01, irradianceRes=50, temperatureRes=0.5
            )
        except Exception as e:
            pytest.fail(str(e))

# Example test script comparing outputs between models.

# Call `python3 tests/test_PVCell.py` from ArraySimulation/ to see model output
# at STD conditions.
cell = PVCell()
cellI = PVCellIdeal()
cellNI = PVCellNonideal()
print("----------------------------------------------------------------------")
print("Input            |Default       |Ideal                  |Nonideal     ")
for voltage in np.arange(0, 0.61, 0.01):
    print(
        str(voltage / 10)
        + "V|1000G|25C   |"
        + str(cell.getCurrent(voltage, 1000, 25))
        + "\t\t|"
        + str(cellI.getCurrent(voltage, 1000, 25))
        + "\t|"
        + str(cellNI.getCurrentLookup(voltage, 1000, 25))
    )
