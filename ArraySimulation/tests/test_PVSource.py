"""
test_PVSource.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/16/20
Last Modified: 11/24/20

Description: Test file to see if the various implemented models run as expected.
"""
# Library Imports.
import pytest
import sys

sys.path.append("../")

# Custom Imports.
from ArraySimulation.PVSource.PVSource import PVSource
from ArraySimulation.PVSource.PVCell.PVCellIdeal import PVCellIdeal
from ArraySimulation.PVSource.PVCell.PVCellNonideal import PVCellNonideal


class TestPVSource:
    def test_PVSourceDefault(self):
        """
        Testing the default PVSource.
        """
        # Single cell model.
        source = PVSource()
        source.setupModel()

        try:
            # Assert that we throw no module definitions for all methods of
            # PVSource.
            with pytest.raises(Exception) as excinfo:
                source.getModuleCurrent(
                    {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    }
                )
            assert "No cell model is defined for the PVSource." == str(excinfo.value)
            with pytest.raises(Exception) as excinfo:
                source.getSourceCurrent(
                    {
                        "0": {
                            "numCells": 1,
                            "voltage": 0.0,
                            "irradiance": 1000,
                            "temperature": 25,
                        },
                    }
                )
            assert "No cell model is defined for the PVSource." == str(excinfo.value)
            with pytest.raises(Exception) as excinfo:
                source.getIV(
                    {
                        "0": {
                            "numCells": 1,
                            "voltage": 0.0,
                            "irradiance": 1000,
                            "temperature": 25,
                        },
                    },
                    0.01,
                )
            assert "No cell model is defined for the PVSource." == str(excinfo.value)
            with pytest.raises(Exception) as excinfo:
                source.getEdgeCharacteristics(
                    {
                        "0": {
                            "numCells": 1,
                            "voltage": 0.0,
                            "irradiance": 1000,
                            "temperature": 25,
                        },
                    },
                    0.01,
                )
            assert "No cell model is defined for the PVSource." == str(excinfo.value)

            # Assert that we get the correct model type.
            assert source.getModelType() == "Default"
        except Exception as e:
            pytest.fail(str(e))

    def test_PVSourceIdeal(self):
        """
        Testing the PVSource with an Ideal PVCell model.
        """
        source = PVSource()
        source.setupModel("Ideal")

        cell = PVCellIdeal()
        try:
            # Assert that we get the same module current output as that for a
            # single cell.
            assert (
                source.getModuleCurrent(
                    {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    }
                )
                == cell.getCurrent(
                    numCells=1, voltage=0, irradiance=1000, temperature=25
                )
            )

            # TODO: fix when implemented, and implement comments
            assert (
                source.getSourceCurrent(
                    {
                        "0": {
                            "numCells": 1,
                            "voltage": 0.0,
                            "irradiance": 1000,
                            "temperature": 25,
                        },
                    }
                )
                == cell.getCurrent(
                    numCells=1, voltage=0, irradiance=1000, temperature=25
                )
            )

            assert source.getIV(
                {
                    "0": {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    },
                },
                0.01,
            ) == cell.getCellIV(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )

            assert source.getEdgeCharacteristics(
                {
                    "0": {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    },
                },
                0.01,
            ) == cell.getCellEdgeCharacteristics(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )

            # Assert that we get the correct model type.
            assert source.getModelType() == "Ideal"
        except Exception as e:
            pytest.fail(str(e))

    def test_PVSourceNonideal(self):
        """
        Testing the PVSource with an Nonideal PVCell model.
        """
        source = PVSource()
        source.setupModel("Nonideal")

        cell = PVCellNonideal()
        try:
            # Assert that we get the same module current output as that for a
            # single cell.
            assert (
                source.getModuleCurrent(
                    {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    }
                )
                == cell.getCurrent(
                    numCells=1, voltage=0, irradiance=1000, temperature=25
                )
            )

            # TODO: fix when implemented
            assert (
                source.getSourceCurrent(
                    {
                        "0": {
                            "numCells": 1,
                            "voltage": 0.0,
                            "irradiance": 1000,
                            "temperature": 25,
                        },
                    }
                )
                == cell.getCurrent(
                    numCells=1, voltage=0, irradiance=1000, temperature=25
                )
            )

            assert source.getIV(
                {
                    "0": {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    },
                },
                0.01,
            ) == cell.getCellIV(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )

            assert source.getEdgeCharacteristics(
                {
                    "0": {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    },
                },
                0.01,
            ) == cell.getCellEdgeCharacteristics(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )

            # Assert that we get the correct model type.
            assert source.getModelType() == "Nonideal"
        except Exception as e:
            pytest.fail(str(e))

    def test_PVSourceNonidealLookup(self):
        """
        Testing the PVSource with an Ideal PVCell model. Lookup is enabled.
        """
        source = PVSource()
        source.setupModel("Nonideal", True)

        cell = PVCellNonideal()
        try:
            # Assert that we get the same module current output as that for a
            # single cell.
            assert source.getModuleCurrent(
                {
                    "numCells": 1,
                    "voltage": 0.0,
                    "irradiance": 1000,
                    "temperature": 25,
                }
            ) == cell.getCurrentLookup(
                numCells=1, voltage=0, irradiance=1000, temperature=25
            )

            # TODO: fix when implemented
            assert source.getSourceCurrent(
                {
                    "0": {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    },
                }
            ) == cell.getCurrentLookup(
                numCells=1, voltage=0, irradiance=1000, temperature=25
            )

            assert source.getIV(
                {
                    "0": {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    },
                },
                0.01,
            ) == cell.getCellIV(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )

            assert source.getEdgeCharacteristics(
                {
                    "0": {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    },
                },
                0.01,
            ) == cell.getCellEdgeCharacteristics(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )

            # Assert that we get the correct model type.
            assert source.getModelType() == "Nonideal"
        except Exception as e:
            pytest.fail(str(e))
