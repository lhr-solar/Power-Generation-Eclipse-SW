"""
PVSource.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/14/20
Last Modified: 10/14/20

Description: The PVEnvironment class is a concrete base class that manages the
environmental conditions received by the PVSource at any cycle. In fact, it
manages the cycle time of the entire simulation, and outputs the
environmental conditions based on that cycle. It has the ability to extract
environmental regimes from JSON files, as well as generate a unit step
function with a fixed irradiance and temperature for steady state behavior
testing.
"""
# Library Imports.
import json

# Custom Imports.


class PVEnvironment:
    """
    The PVEnvironment class is a concrete base class that manages the
    environmental conditions received by the PVSource at any cycle. In fact, it
    manages the cycle time of the entire simulation, and outputs the
    environmental conditions based on that cycle. It has the ability to extract
    environmental regimes from JSON files, as well as generate a unit step
    function with a fixed irradiance and temperature for steady state behavior
    testing.
    """

    # The smallest cycle number the simulation can be.
    MIN_CYCLES = 0

    # A dictionary referencing module_type strings to the number of cells.
    _cellDefinitions = {"1x1": 1, "1x2": 2, "2x2": 4, "2x4": 8}

    # Where all lookup files are located.
    file_root = "./External/"

    def __init__(self):
        pass

    def setupModel(self, sourceType=(1000, 25), maxCycles=200):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        sourceType: Union -> tuple `(1000, 255)` or string `single_cell.json`
            Specifies how and/or where the source model is defined and its
            environmental regime over time. It checks for either a tuple of
            initial conditions (Step mode) or a string pointing to a JSON file
            in 'External/'.

            The method builds a data model of the modules in the PVSource and
            a mapping of their environmental regime to return on demand.
        maxCycles: int
            Maximum number of cycles our environment should extend to.
        """
        # Current cycle of the PVEnvironment. Dictates what environmental
        # conditions come out at the time. Adjustable.
        self._cycle = self.MIN_CYCLES

        # Maximum cycle in the environment. We extrapolate data up to this point.
        self._maxCycle = maxCycles

        # Reference to the dictionary containing the environmental properties for
        # each module in the PVSource.
        try:
            if isinstance(sourceType, str):
                # Check for relevant filename at /External
                f = open(self.file_root + sourceType)
                self._source = json.load(f)

            elif isinstance(sourceType, tuple):
                self._source = {
                    "name": "Single Cell.",
                    "description": "A single cell. "
                    + "Emulates a step function with irradiance "
                    + str(sourceType[0])
                    + " and temperature "
                    + str(sourceType[1])
                    + " for t => 0.",
                    "num_modules": 1,
                    "pv_model": {
                        "0": {
                            "module_type": "1x1",
                            "env_type": "Step",
                            "env_regime": sourceType,
                        }
                    },
                }

            else:
                raise Exception(
                    "Invalid sourceType. Currently supported types are a "
                    + "properly formatted JSON file or a step response tuple in "
                    + "the format (irradiance, temperature)."
                )

        except Exception as e:
            self._source = None
            print(e)

    def getCycle(self):
        """
        Returns the current cycle of the environment.

        Return
        ------
        int: Current cycle.
        """
        return self._cycle

    def setCycle(self, cycle):
        """
        Sets the internal cycle of the PVEnvironment.

        Parameters
        ----------
        cycle: int
            The current moment in time the environment should be set to.
        """
        if self.MIN_CYCLES <= cycle and cycle <= self._maxCycle:
            self._cycle = cycle
        else:
            raise Exception(
                "We can never have a negative cycle in the PVEnvironment. "
                + "Nor can we exceed the maximum cycles defined at initialization."
            )

    def cycle(self):
        """
        Cycles the internal clock once.
        """
        self._cycle += 1

    def getSourceDefinition(self, voltage):
        """
        Gets the source definition at the current cycle.

        The modules definition is in the following format:

            modulesDef = {
                "0": {
                    "numCells": int,
                    "voltage": float,       (V)
                    "irradiance": float,    (W/m^2)
                    "temperature": float,   (C)
                },
                ...
            }

        Parameters
        ----------
        voltage: float
            Voltage across the module in Volts.

        Returns
        -------
        dict:  modulesDef
            A dictionary of the selected module's properties.
        """
        modulesDef = {}

        modules = self._source["pv_model"]
        for key in modules.keys():
            module = modules[key]
            if module["env_type"] == "Array":
                modulesDef[key] = {
                    "numCells": self._cellDefinitions[module["module_type"]],
                    "voltage": voltage,
                    "irradiance": module["env_regime"][self._cycle][
                        1
                    ],  # TODO: This assumes env_regime is evenly spaced and requires no interpolation (each entry is 1 cycle apart from each other)
                    "temperature": module["env_regime"][self._cycle][2],
                }
            elif module["env_type"] == "Step":
                modulesDef[key] = {
                    "numCells": self._cellDefinitions[module["module_type"]],
                    "voltage": voltage,
                    "irradiance": module["env_regime"][0],
                    "temperature": module["env_regime"][1],
                }
            else:
                raise Exception("Undefined environment type.")

        return modulesDef

    def getModuleDefinition(self, moduleName, voltage):
        """
        Gets the module definition of a specific module at the current cycle.

        The module definition is in the following format:

            moduleDef = {
                "numCells": int,
                "voltage": float,       (V)
                "irradiance": float,    (W/m^2)
                "temperature": float,   (C)
            }

        Parameters
        ----------
        moduleName: String
            Key to the source dictionary that corresponds to the module
            selected. The moduleDef of this module is constructed and returned.
        voltage: float
            Voltage across the module in Volts.

        Returns
        -------
        dict:  moduleDef
            A dictionary of the selected module's properties.
        """
        module = self._source["pv_model"].get(moduleName)
        if module is not None:
            if module["env_type"] == "Array":
                return {
                    "numCells": self._cellDefinitions[module["module_type"]],
                    "voltage": voltage,
                    "irradiance": module["env_regime"][self._cycle][
                        1
                    ],  # TODO: This assumes env_regime is evenly spaced and requires no interpolation (each entry is 1 cycle apart from each other)
                    "temperature": module["env_regime"][self._cycle][2],
                }
            elif module["env_type"] == "Step":
                return {
                    "numCells": self._cellDefinitions[module["module_type"]],
                    "voltage": voltage,
                    "irradiance": module["env_regime"][0],
                    "temperature": module["env_regime"][1],
                }
            else:
                raise Exception("Undefined environment type.")
        else:
            raise Exception(
                "Module does not exist in PVEnvironment with the name "
                + moduleName
            )

    def getModuleMapping(self):
        """
        Returns a stripped dictionary of modules, and the number of cells in
        each.

        Return
        ------
        dict: {"module1": "1x1", "module2": "2x4", ...}
            A dictionary of modules where each module key defines the cell
            layout of the module.
        """
        modulesDict = {}
        for module in self._source["pv_model"].items():
            modulesDict[module[0]] = module[1]["module_type"]

        return modulesDict
