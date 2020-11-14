"""
test_source.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/16/20
Last Modified: 10/16/20

Description: Integration test of the PVSource and PVEnvironment.
"""
# Library Imports.
import pytest
import sys

sys.path.append("../")

# Custom Imports.
from ArraySimulation.PVEnvironment.PVEnvironment import PVEnvironment
from ArraySimulation.PVSource.PVSource import PVSource


class TestSource:
    def test_SourceDefault(self):
        """
        A test feeding the default PVEnvironment to the PVSource using no PVCell
        model.
        """
        env = PVEnvironment()
        env.setupModel()
        source = PVSource()  # PVCell model is by default, None
        source.setupModel()

        try:
            # Generate Module definition and plug into Source
            moduleDef = env.getModuleDefinition("0", 0.0)
            assert source.getModuleCurrent(moduleDef) == None

            modulesDef = env.getSourceDefinition(0.0)
            assert source.getSourceCurrent(modulesDef) == None
            assert source.getIV(modulesDef) == None
            assert source.getEdgeCharacteristics(modulesDef) == None

            assert source.getModelType() == "Default"
        except Exception as e:
            print(e)
            pytest.fail(e)

    # TODO: Default PVEnvironment feeding into a PVSource using the ideal PVCell
    # model.

    # TODO: Default PVEnvironment feeding into a PVSource using the nonideal
    # PVCell model.
