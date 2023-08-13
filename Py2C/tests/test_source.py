"""
test_source.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/16/20
Last Modified: 11/24/20

Description: Integration test of the PVSource and PVEnvironment.
"""
# Library Imports.
import pytest
import sys

sys.path.append("../")

# Custom Imports.
from ArraySimulation.PVEnvironment.PVEnvironment import PVEnvironment
from ArraySimulation.PVSource.PVSource import PVSource
from ArraySimulation.PVSource.PVCell.PVCellIdeal import PVCellIdeal
from ArraySimulation.PVSource.PVCell.PVCellNonideal import PVCellNonideal


class TestSource:
    def test_SourceDefault(self):
        """
        A test feeding the default PVEnvironment into a PVSource with no PVCell
        model.
        """
        env = PVEnvironment()
        env.setupModel()
        source = PVSource()  # PVCell model is by default, None
        source.setupModel()

        try:
            # Generate Module definition and plug into Source
            moduleDef = env.getModuleDefinition("0", 0.0)
            modulesDef = env.getSourceDefinition(0.0)

            # Assert that we throw no module definitions for all methods of
            # PVSource.
            with pytest.raises(Exception) as excinfo:
                source.getModuleCurrent(moduleDef)
            assert "No cell model is defined for the PVSource." == str(excinfo.value)
            with pytest.raises(Exception) as excinfo:
                source.getSourceCurrent(modulesDef)
            assert "No cell model is defined for the PVSource." == str(excinfo.value)
            with pytest.raises(Exception) as excinfo:
                source.getIV(modulesDef)
            assert "No cell model is defined for the PVSource." == str(excinfo.value)
            with pytest.raises(Exception) as excinfo:
                source.getEdgeCharacteristics(modulesDef)
            assert "No cell model is defined for the PVSource." == str(excinfo.value)

            # Assert that we get the correct model type.
            assert source.getModelType() == "Default"
        except Exception as e:
            pytest.fail(str(e))

    def test_SourceIdeal(self):
        """
        A test feeding the default PVEnvironment into a PVSource with an Ideal
        PVCell model.
        """
        env = PVEnvironment()
        env.setupModel()
        source = PVSource()
        source.setupModel("Ideal")

        cell = PVCellIdeal()
        try:
            # Generate Module definition and plug into Source
            moduleDef = env.getModuleDefinition("0", 0.0)
            modulesDef = env.getSourceDefinition(0.0)

            # Assert that we get the correct function outputs for the module definition.
            assert source.getModuleCurrent(moduleDef) == cell.getCurrent(
                numCells=1, voltage=0, irradiance=1000, temperature=25
            )
            assert source.getSourceCurrent(modulesDef) == cell.getCurrent(
                numCells=1, voltage=0, irradiance=1000, temperature=25
            )
            assert source.getIV(modulesDef) == cell.getCellIV(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )
            assert source.getEdgeCharacteristics(
                modulesDef
            ) == cell.getCellEdgeCharacteristics(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )

            # Assert that we get the correct model type.
            assert source.getModelType() == "Ideal"
        except Exception as e:
            pytest.fail(str(e))

    def test_SourceNonideal(self):
        """
        A test feeding the default PVEnvironment into a PVSource with an
        Nonideal PVCell model.
        """
        env = PVEnvironment()
        env.setupModel()
        source = PVSource()
        source.setupModel("Nonideal")

        cell = PVCellNonideal()
        try:
            # Generate Module definition and plug into Source
            moduleDef = env.getModuleDefinition("0", 0.0)
            modulesDef = env.getSourceDefinition(0.0)

            # Assert that we get the correct function outputs for the module definition.
            assert source.getModuleCurrent(moduleDef) == cell.getCurrent(
                numCells=1, voltage=0, irradiance=1000, temperature=25
            )
            assert source.getSourceCurrent(modulesDef) == cell.getCurrent(
                numCells=1, voltage=0, irradiance=1000, temperature=25
            )
            assert source.getIV(modulesDef) == cell.getCellIV(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )
            assert source.getEdgeCharacteristics(
                modulesDef
            ) == cell.getCellEdgeCharacteristics(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )

            # Assert that we get the correct model type.
            assert source.getModelType() == "Nonideal"
        except Exception as e:
            pytest.fail(str(e))

    def test_SourceNonidealLookup(self):
        """
        A test feeding the default PVEnvironment into a PVSource with an
        Nonideal PVCell model. Lookup is enabled.
        """
        env = PVEnvironment()
        env.setupModel()
        source = PVSource()
        source.setupModel("Nonideal", True)

        cell = PVCellNonideal()
        try:
            # Generate Module definition and plug into Source
            moduleDef = env.getModuleDefinition("0", 0.0)
            modulesDef = env.getSourceDefinition(0.0)

            # Assert that we get the correct function outputs for the module definition.
            assert source.getModuleCurrent(moduleDef) == cell.getCurrentLookup(
                numCells=1, voltage=0, irradiance=1000, temperature=25
            )
            assert source.getSourceCurrent(modulesDef) == cell.getCurrentLookup(
                numCells=1, voltage=0, irradiance=1000, temperature=25
            )
            assert source.getIV(modulesDef) == cell.getCellIV(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )
            assert source.getEdgeCharacteristics(
                modulesDef
            ) == cell.getCellEdgeCharacteristics(
                numCells=1, resolution=0.01, irradiance=1000, temperature=25
            )

            # Assert that we get the correct model type.
            assert source.getModelType() == "Nonideal"
        except Exception as e:
            pytest.fail(str(e))
