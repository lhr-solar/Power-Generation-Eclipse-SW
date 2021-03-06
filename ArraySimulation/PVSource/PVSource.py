"""
PVSource.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 11/24/20

Description: The PVSource (Photovoltaic Cell/Module/Subarray) class is a
concrete base class that provides a common API for derived classes to use. The
PVCell class enables users to retrieve information of the PV model, such as
IV curves, maximum power points, and so on given a set of input conditions.

The following paper discusses how to model multiple module PV sources with
variable shading:

    Accurate Modeling of Partially Shaded PV Arrays (Meyers
    et Mikofski)

    A library developed by these authors is called PVMismatch;
    it can be found at [https://github.com/SunPower/PVMismatch].
    We can potentially draw inspiration on this work to build
    PVSource (This is very hard, since I don't understand their
    code!)

    Attribution of the library:

    Mark Mikofski, Bennet Meyers, Chetan Chaudhari (2018).
    “PVMismatch Project: https://github.com/SunPower/PVMismatch".
    SunPower Corporation, Richmond, CA.

TODO: for now, we'll just use the first module we come across when generating
current and associated IV curve characteristics.
"""
# Library Imports.
import numpy as np

# Custom Imports.
from ArraySimulation.PVSource.PVCell.PVCellIdeal import PVCellIdeal
from ArraySimulation.PVSource.PVCell.PVCellNonideal import PVCellNonideal


class PVSource:
    """
    The PVSource (Photovoltaic source, which encompasses cells, modules, and
    subarrays), is a concrete base class that provides a common API for clients
    to use. The PVSource class enables users to retrieve information on the
    PVSource model, such as IV curves, maximum power points, and so on given a
    set of input conditions.
    """

    # The upper voltage bound that should be tested by any model for a single
    # cell. We expect the PV to always be at open circuit voltage at this point.
    # Adjustable based on the number of cells determined from the initialization.
    MAX_CELL_VOLTAGE = 0.8

    # Our starting upper current bound when looking for the minimum current of
    # a set of modules in series with bypass diodes.
    MAX_CURRENT = 8

    # Out starting lower current bound when looking for the I-V curve of a set
    # of modules in series with bypass diodes.
    MIN_CURRENT = 0

    def __init__(self):
        self._modelType = None
        self._useLookup = None

    def setupModel(self, modelType="Default", useLookup=True):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        modelType: String
            Specifies the PVCell model used for modeling all photovoltaics.
        useLookup: Bool
            Enables the use of lookup tables, if they exist for the model. If it
            doesn't, we default to the getCurrent function that doesn't use
            lookups.
        """
        # Determines the model used by each cell. Every cell gets the same model.
        self._modelType = modelType
        if modelType == "Ideal":
            self._model = PVCellIdeal(useLookup)
        elif modelType == "Nonideal":
            self._model = PVCellNonideal(useLookup)
        else:
            self._model = None

        # Controls whether each cell in a model calculates its current using a
        # lookup table or not.
        self._useLookup = useLookup

    def getModuleCurrent(self, moduleDef):
        """
        Calculates and returns the source model current for a specific module
        given various environmental parameters.

        Parameters
        ----------
        moduleDef: Dict
            A dictionary for a single module, in the following format:

            moduleDef = {
                "numCells": int,
                "voltage": float,       (V)
                "irradiance": float,    (W/m^2)
                "temperature": float,   (C)
            }

        Returns
        -------
        float|None:
            Current of the module model or None if the model is not defined.

        Assumptions
        -----------
        Current is roughly linear to the number of cells in series.
        """
        if self._model is not None:
            if self._useLookup:
                return self._model.getCurrentLookup(
                    moduleDef["numCells"],
                    moduleDef["voltage"],
                    moduleDef["irradiance"],
                    moduleDef["temperature"],
                )
            else:
                return self._model.getCurrent(
                    moduleDef["numCells"],
                    moduleDef["voltage"],
                    moduleDef["irradiance"],
                    moduleDef["temperature"],
                )
        else:
            raise Exception("No cell model is defined for the PVSource.")

    def getSourceCurrent(self, modulesDef):
        """
        Calculates and returns the source model current given various
        environmental parameters.

        Parameters
        ----------
        modulesDef: Dict
            A dictionary for a set of modules representing the source, in the
            following format:

            modulesDef = {
                "0": {
                    "numCells": int,
                    "voltage": float,       (V)
                    "irradiance": float,    (W/m^2)
                    "temperature": float,   (C)
                },
                ...
            }

        Returns
        -------
        float|None:
            Current of the source model or None if the model is not defined.

        Assumptions
        -----------
        Current is roughly linear to the number of cells in series.
        """
        if self._model is not None:
            cell1Current = self.getModuleCurrent({"numCells":1,"voltage":modulesDef["0"]["voltage"],"irradiance":1000,"temperature": 25})
            cell2Current = self.getModuleCurrent({"numCells":2,"voltage":modulesDef["0"]["voltage"],"irradiance":400,"temperature": 25})
            cell3Current = self.getModuleCurrent({"numCells":3,"voltage":modulesDef["0"]["voltage"],"irradiance":200,"temperature": 25})
            current = max(cell1Current,cell2Current,cell3Current)*(1-np.exp(-1000*modulesDef["0"]["voltage"]))
            return current
        else:
            raise Exception("No cell model is defined for the PVSource.")

    def getIV(self, modulesDef, resolution=0.01):
        """
        TODO: implement multimodule support
        Calculates the entire source model current voltage plot given various
        environmental parameters.

        Parameters
        ----------
        modulesDef: Dict
            A dictionary for a set of modules representing the source, in the
            following format:

            modulesDef = {
                "0": {
                    "numCells": int,
                    "voltage": float,       (V)     
                    "irradiance": float,    (W/m^2)
                    "temperature": float,   (C)
                },
                ...
            }
        resolution: float
            Voltage stride across the source. Occurs within the bounds of [0,
            MAX_VOLTAGE], inclusive.

        Returns
        -------
        list: [(voltage:float, current:float), ...]
            A list of paired voltage|current tuples across the cell IV curve.

        Assumptions
        -----------
        The IV curve of the source has a short circuit current of 0A at
        MAX_VOLTAGE.
        """
        # We need to calculate the expected maximum voltage that can be applied
        # over all modules.
        model = []
        if self._model is not None:
            for voltage in np.arange(0, round(PVSource.MAX_CELL_VOLTAGE*3,2)+0.01, 0.01):
                modulesDef = {"0":{"numCells": 1,"voltage":voltage,"irradiance": 1000, "temperature":25}}
                current = self.getSourceCurrent(modulesDef)
                voltCurrPair = (voltage, current)
                model.append(voltCurrPair)
            return model
            # return self._model.getCellCurrent(
            #     moduleDef["numCells"],
            #     resolution,
            #     moduleDef["irradiance"],
            #     moduleDef["temperature"],
            # )

            # model = []
            # maxVoltage = 0
            # for moduleDef in modulesDef.values():
            #     maxVoltage += moduleDef["numCells"] * PVSource.MAX_CELL_VOLTAGE

            # for voltage in np.arange(0, maxVoltage + resolution, resolution):
            #     currents = []

            #     # We're looking for the maximum of current of all modules. We
            #     # can do this by putting each module result into a list and then
            #     # finding the max of the list.
            #     # TODO: needs to match desmos.
            #     for moduleDef in modulesDef.values():
            #         print(moduleDef)
            #         if self._useLookup:
            #             currents.append(self._model.getCurrentLookup(
            #                 moduleDef["numCells"],
            #                 voltage,
            #                 moduleDef["irradiance"],
            #                 moduleDef["temperature"]
            #             ))
            #         else:
            #             currents.append(self._model.getCurrent(
            #                 moduleDef["numCells"],
            #                 voltage,
            #                 moduleDef["irradiance"],
            #                 moduleDef["temperature"]
            #             ))
            #     print(currents)
            #     model.append((voltage, max(currents)))
            # return model

        else:
            raise Exception("No cell model is defined for the PVSource.")

    def getEdgeCharacteristics(self, modulesDef, resolution=0.01):
        """
        TODO: implement multimodule support
        Calculates the source model edge characteristics given various
        environmental parameters.

        Parameters
        ----------
        modulesDef: Dict
            A dictionary for a set of modules representing the source, in the
            following format:

            modulesDef = {
                "0": {
                    "numCells": int,
                    "voltage": float,       (V)     <- This is ignored.
                    "irradiance": float,    (W/m^2)
                    "temperature": float,   (C)
                },
                ...
            }
        resolution: float
            Voltage stride across the source. Occurs within the bounds of [0,
            MAX_VOLTAGE], inclusive.

        Returns
        -------
        tuple: (V_OC:float, I_SC:float, (V_MPP:float, I_MPP:float)):
            A tuple of tuples indicating the open circuit voltage, the short
            circuit current, and the GLOBAL maximum power point (MPP) voltage
            and current.
        """
        if self._model is not None:
            moduleDef = modulesDef["0"]
            return self._model.getCellEdgeCharacteristics(
                moduleDef["numCells"],
                resolution,
                moduleDef["irradiance"],
                moduleDef["temperature"],
            )
        else:
            raise Exception("No cell model is defined for the PVSource.")

    def getModelType(self):
        """
        Returns the model type used for each PVCell in PVSource.

        Return
        ------
        String: Model type name.
        """
        return self._modelType
