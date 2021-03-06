"""
test_PVCell.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 11/24/20

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
            assert (
                cell.getCurrent(numCells=1, voltage=0, irradiance=0, temperature=0)
                == -1
            )
            assert (
                cell.getCurrentLookup(
                    numCells=1, voltage=0, irradiance=0, temperature=0
                )
                == -1
            )
            assert (
                cell.getCellIV(numCells=1, resolution=0, irradiance=0, temperature=0)
                == []
            )
            assert cell.getCellEdgeCharacteristics(
                numCells=1, resolution=0, irradiance=0, temperature=0
            ) == (0, 0, (0, 0))
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
            assert (
                cell.getCurrent(numCells=1, voltage=0, irradiance=1000, temperature=25)
                != -1
            )
            assert (
                cell.getCurrentLookup(
                    numCells=1, voltage=0, irradiance=1000, temperature=25
                )
                == -1
            )
            assert (
                cell.getCellIV(
                    numCells=1, resolution=0.1, irradiance=1000, temperature=25
                )
                != []
            )
            assert cell.getCellEdgeCharacteristics(
                numCells=1, resolution=0.1, irradiance=1000, temperature=25
            ) != (
                0,
                0,
                (0, 0),
            )
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
            assert (
                cell.getCurrent(numCells=1, voltage=0, irradiance=1000, temperature=25)
                != -1
            )
            assert (
                cell.getCurrentLookup(
                    numCells=1, voltage=0, irradiance=1000, temperature=25
                )
                == 6.146
            )
            assert cell.getCurrent(
                numCells=1, voltage=0, irradiance=1000, temperature=25
            ) == cell.getCurrentLookup(1, 0, 1000, 25)
            assert (
                cell.getCellIV(
                    numCells=1, resolution=0.1, irradiance=1000, temperature=25
                )
                != []
            )
            assert cell.getCellEdgeCharacteristics(1, 0.1, 1000, 25) != (
                0,
                0,
                (0, 0),
            )
            assert cell.getModelType() == "Nonideal"
        except Exception as e:
            pytest.fail(str(e))

    def test_PVCellNonidealBuildLookup(self):
        """
        Test that we can build a lookup for the Nonideal Cell Model.
        """
        cell = PVCellNonideal()

        try:
            cell.buildCurrentLookup(voltageRes=0.1, irradianceRes=50, temperatureRes=5)
        except Exception as e:
            pytest.fail(str(e))

    # NOTE: We can use this test to generate our models for us.
    @pytest.mark.additional
    def test_PVCellNonidealBuildLookupLong(self):
        """
        Test that we can build a lookup for the Nonideal Cell Model.
        This test version should match that in NonidealCellLookup.csv.
        """
        cell = PVCellNonideal()

        try:
            cell.buildCurrentLookup(voltageRes=0.01, irradianceRes=50, temperatureRes=1)
        except Exception as e:
            pytest.fail(str(e))


# Example test script comparing outputs between models.

# Call `python3 tests/test_PVCell.py` from ArraySimulation/ to see model output
# at STD conditions.
cell = PVCell()
cellI = PVCellIdeal()
cellNI = PVCellNonideal()
print("----------------------------------------------------------------------")
print("Input          |Default       |Ideal                  |Nonideal     ")
for voltage in np.arange(0, 0.81, 0.01):
    print(
        str(round(voltage, 3))
        + "V|1000G|25C\t|"
        + str(cell.getCurrent(1, voltage, 1000, 25))
        + "\t\t|"
        + str(cellI.getCurrent(1, voltage, 1000, 25))
        + "\t|"
        + str(cellNI.getCurrentLookup(1, voltage, 1000, 25))
    )
