"""
test_PVSource.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/16/20
Last Modified: 10/16/20

Description: Test file to see if the various implemented models run as expected.
"""
# Library Imports.
import pytest
import sys

sys.path.append("../")

# Custom Imports.
from ArraySimulation.PVSource.PVSource import PVSource


class TestPVSource:
    def test_PVSourceDefault(self):
        """
        Testing the default PVSource.
        """
        print("PVSource Test.")

        # Single cell model.
        source = PVSource()
        source.setupModel()

        try:
            # Getting characteristics for the single cell.
            assert (
                source.getModuleCurrent(
                    {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    }
                )
                == None
            )

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
                == None
            )

            assert (
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
                == None
            )

            assert (
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
                == None
            )

            assert source.getModelType() == "Default"
        except Exception as e:
            pytest.fail(e)

    # TODO: test with ideal and non ideal models.
    def test_PVSourceIdeal(self):
        """
        A test feeding the default PVEnvironment to the PVSource using an ideal
        PVCell model.
        """
        source = PVSource()
        source.setupModel("Ideal")

        try:
            assert (
                source.getModuleCurrent(
                    {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    }
                )
                != None
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
                == None
            )

            assert (
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
                == None
            )

            assert (
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
                == None
            )

            assert source.getModelType() == "Ideal"
        except Exception as e:
            print(e)
            pytest.fail(e)

    def test_PVSourceNonideal(self):
        """
        A test feeding the default PVEnvironment to the PVSource using a
        nonideal PVCell model.
        """
        source = PVSource()
        source.setupModel("Nonideal")

        try:
            assert (
                source.getModuleCurrent(
                    {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    }
                )
                != None
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
                == None
            )

            assert (
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
                == None
            )

            assert (
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
                == None
            )

            assert source.getModelType() == "Nonideal"
        except Exception as e:
            print(e)
            pytest.fail(e)

    def test_PVSourceNonidealLookup(self):
        """
        A test feeding the default PVEnvironment to the PVSource using a
        nonideal PVCell model. Lookup is enabled.
        """
        source = PVSource()
        source.setupModel("Nonideal", True)

        try:
            assert (
                source.getModuleCurrent(
                    {
                        "numCells": 1,
                        "voltage": 0.0,
                        "irradiance": 1000,
                        "temperature": 25,
                    }
                )
                != None
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
                == None
            )

            assert (
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
                == None
            )

            assert (
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
                == None
            )

            assert source.getModelType() == "Nonideal"
        except Exception as e:
            print(e)
            pytest.fail(e)