"""
test_PVEnvironment.py

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
from ArraySimulation.PVEnvironment.PVEnvironment import PVEnvironment


class TestPVEnvironment:
    def test_PVEnvironmentDefault(self):
        """
        Testing the default PVEnvironment.
        """
        print("PVEnvironment Test at STD conditions.")

        # The photovoltaic environment. By default we generate a single cell at
        # STD conditions (1000 G, 25 C).
        env = PVEnvironment()
        env.setupModel()

        try:
            # Assert that the module definition for our single module is correct.
            assert env.getModuleDefinition("0", 0.0) == {
                "numCells": 1,
                "voltage": 0.0,
                "irradiance": 1000,
                "temperature": 25,
            }

            # Assert that our PV definition for our single module is correct.
            assert env.getSourceDefinition(0.0) == {
                "0": {
                    "numCells": 1,
                    "voltage": 0.0,
                    "irradiance": 1000,
                    "temperature": 25,
                },
            }

            # Assert that cycling doesn't change our output.
            assert env.getCycle() == 0
            env.cycle()
            assert env.getCycle() == 1

            # Assert that the module definition for our single module is correct.
            assert env.getModuleDefinition("0", 0.0) == {
                "numCells": 1,
                "voltage": 0.0,
                "irradiance": 1000,
                "temperature": 25,
            }

            # Assert that our PV definition for our single module is correct.
            assert env.getSourceDefinition(0.0) == {
                "0": {
                    "numCells": 1,
                    "voltage": 0.0,
                    "irradiance": 1000,
                    "temperature": 25,
                },
            }

            # Assert that setting the cycle doesn't change our output.
            env.setCycle(100)
            assert env.getCycle() == 100

            # Assert that the module definition for our single module is correct.
            assert env.getModuleDefinition("0", 0.0) == {
                "numCells": 1,
                "voltage": 0.0,
                "irradiance": 1000,
                "temperature": 25,
            }

            # Assert that our PV definition for our single module is correct.
            assert env.getSourceDefinition(0.0) == {
                "0": {
                    "numCells": 1,
                    "voltage": 0.0,
                    "irradiance": 1000,
                    "temperature": 25,
                },
            }

            # Assert that we can get a list of modules from the PVEnvironment.
            assert env.getModuleMapping() == {"0": "1x1"}

        except Exception as e:
            print(e)
            pytest.fail(e)

    def test_PVEnvironmentProfile(self):
        """
        Testing the PVEnvironment using a file reference.
        """
        print("PVEnvironment Test with a file.")

        env = PVEnvironment()
        env.setupModel(sourceType="SingleCell.json")

        try:
            # Assert that the module definition for our single module is correct.
            assert env.getModuleDefinition("0", 0.0) == {
                "numCells": 1,
                "voltage": 0.0,
                "irradiance": 1000,
                "temperature": 45.5,
            }

            # Assert that our PV definition for our single module is correct.
            assert env.getSourceDefinition(0.0) == {
                "0": {
                    "numCells": 1,
                    "voltage": 0.0,
                    "irradiance": 1000,
                    "temperature": 45.5,
                },
            }

            # Assert that cycling doesn't change our output.
            assert env.getCycle() == 0
            env.cycle()
            assert env.getCycle() == 1

            # Assert that the module definition for our single module is correct.
            assert env.getModuleDefinition("0", 0.0) == {
                "numCells": 1,
                "voltage": 0.0,
                "irradiance": 1000,
                "temperature": 45.5,
            }

            # Assert that our PV definition for our single module is correct.
            assert env.getSourceDefinition(0.0) == {
                "0": {
                    "numCells": 1,
                    "voltage": 0.0,
                    "irradiance": 1000,
                    "temperature": 45.5,
                },
            }

            # Assert that setting the cycle reflects the entry in the lookup.
            env.setCycle(100)
            assert env.getCycle() == 100

            # Assert that the module definition for our single module is correct.
            assert env.getModuleDefinition("0", 0.0) == {
                "numCells": 1,
                "voltage": 0.0,
                "irradiance": 1000,
                "temperature": 28.0,
            }

            # Assert that our PV definition for our single module is correct.
            assert env.getSourceDefinition(0.0) == {
                "0": {
                    "numCells": 1,
                    "voltage": 0.0,
                    "irradiance": 1000,
                    "temperature": 28.0,
                },
            }

            # Assert that we can get a list of modules from the PVEnvironment.
            assert env.getModuleMapping() == {"0": "1x1"}

        except Exception as e:
            print(e)
            pytest.fail(e)
