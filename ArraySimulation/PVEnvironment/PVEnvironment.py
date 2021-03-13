"""
PVSource.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/14/20
Last Modified: 03/07/21

Description: Implementation of the PVEnvironment class.
"""
# Library Imports.
import json
import jsbeautifier

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
    _fileRoot = "./External/"

    def __init__(self):
        pass

    def setupModel(self, source=(1, 1000, 25), maxCycles=200):
        """
        Sets up the initial source parameters.

        Parameters
        ----------
        source: Union -> tuple `(1, 1000, 255)` or string `single_cell.json`
            Specifies how and/or where the source model is defined and its
            environmental regime over time. It checks for either a tuple of
            initial conditions (Step response mode) or a string pointing to a
            JSON file in 'External/'. Step response mode can only performed with
            a single module of arbitrary cell length.

            The method builds a data model of the modules in the PVSource and
            a mapping of their environmental regime to return on demand.

            A tuple may only have 1, 2, 4, or 8 cells in the step response.
        maxCycles: int
            Maximum number of cycles our environment should extend to.

        Return
        ------
        bool: True for success, False elsewise. Upon encountering an exception,
        the PVEnvironment source becomes None.
        """
        # Current cycle of the PVEnvironment. Dictates what environmental
        # conditions come out at the time. Adjustable.
        self._cycle = PVEnvironment.MIN_CYCLES

        # Maximum cycle in the environment. We extrapolate data up to this point.
        self._maxCycle = maxCycles

        # Reference to the dictionary containing the environmental properties for
        # each module in the PVSource.
        try:
            if isinstance(source, str):
                # Source file input.
                self._sourceFile = source

                # Check for relevant filename at /External/
                self._source = json.load(open(PVEnvironment._fileRoot + source))

                return True

                # TODO: validate whether the header matches.
            elif isinstance(source, tuple):
                self._source = {
                    "name": "Single String Model.",
                    "description": str(source[0])
                    + " cell(s) in series. "
                    + "Emulates a step function with irradiance "
                    + str(source[1])
                    + " and temperature "
                    + str(source[2])
                    + " for t => 0.",
                    "num_modules": 1,
                    "pv_model": {
                        "0": {
                            # This is a bit of annoying code that takes our
                            # numCells, converts it into the right key
                            # (i.e. "1x1"), which is THEN later used to convert
                            # it back into the number of cells per module.
                            #
                            # We want the keyed version because in the event we
                            # eventually want to save our modules definition
                            # into a JSON file.
                            #
                            # Of course, this limits the amount of cell options
                            # to 1, 2, 4, or 8 cells.
                            "module_type": list(PVEnvironment._cellDefinitions.keys())[
                                list(PVEnvironment._cellDefinitions.values()).index(
                                    source[0]
                                )
                            ],
                            "env_type": "Step",
                            "needs_interp": False,
                            "env_regime": [source[1], source[2]],
                        }
                    },
                }
                return True
            else:
                raise Exception(
                    "Invalid source. Currently supported types are a "
                    + "properly formatted JSON file or a step response tuple in "
                    + "the format (irradiance, temperature)."
                )
        except Exception as e:
            print(e)
            self._source = None
            return False

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
        Sets the internal cycle of the PVEnvironment. Cannot be larger than max
        cycle.

        Parameters
        ----------
        cycle: int
            The current moment in time the environment should be set to.

        Return
        ------
        bool: Whether cycle was successfully incremented or not.
        """
        if PVEnvironment.MIN_CYCLES <= cycle and cycle <= self._maxCycle:
            self._cycle = cycle
            return True
        else:
            print(
                "We can never have a negative cycle in the PVEnvironment, nor "
                + "can we exceed the maximum cycles defined at initialization. "
                + "As such, the current cycle is not changed."
            )
            return False

    def incrementCycle(self):
        """
        Cycles the internal clock once. Halts the clock when the max cycle is
        reached.

        Return
        ------
        bool: Whether cycle was successfully incremented or not.
        """
        if self._cycle < self._maxCycle:
            self._cycle += 1
            return True
        return False

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
        Throws an exception for non existent modules and invalid module types.

        If the entry in the env_regime does not exist for the module, this
        method will perform a comprehensive interpolation for the profile up
        until the max cycle.
        """
        module = self._source["pv_model"].get(moduleName)
        if module is not None:
            if module["env_type"] == "Array":
                if (
                    module["needs_interp"] == False
                    or module["env_regime"][self._cycle][0] != self._cycle
                ):
                    # Take the current and next entry and add all interpolations
                    # to a new list.
                    events = []
                    for (idx, event) in enumerate(module["env_regime"][0:-1]):
                        currEvent = event
                        nextEvent = module["env_regime"][
                            (idx + 1) % len(module["env_regime"])
                        ]
                        numEntries = nextEvent[0] - currEvent[0]
                        slopeIrrad = (nextEvent[1] - currEvent[1]) / numEntries
                        slopeTemp = (nextEvent[2] - currEvent[2]) / numEntries

                        for idx in range(currEvent[0], nextEvent[0]):
                            events.append(
                                [
                                    idx,
                                    currEvent[1] + slopeIrrad * (idx - currEvent[0]),
                                    currEvent[2] + slopeTemp * (idx - currEvent[0]),
                                ]
                            )

                    # Append the last event.
                    events.append(module["env_regime"][-1])

                    # Write the last interpolated event for all cycles extending
                    # to max_cycles.
                    lastEvent = events[-1]
                    for idx in range(lastEvent[0] + 1, self._maxCycle + 1):
                        events.append([idx, lastEvent[1], lastEvent[2]])

                    module["env_regime"] = events
                    module["needs_interp"] = True

                # Get current model conditions.
                envConditions = module["env_regime"][self._cycle]

                # An array of size 2 is returned.
                return {
                    "numCells": PVEnvironment._cellDefinitions[module["module_type"]],
                    "voltage": voltage,
                    "irradiance": envConditions[1],
                    "temperature": envConditions[2],
                }
            elif module["env_type"] == "Step":
                return {
                    "numCells": PVEnvironment._cellDefinitions[module["module_type"]],
                    "voltage": voltage,
                    "irradiance": module["env_regime"][0],
                    "temperature": module["env_regime"][1],
                }
            else:
                raise Exception("Undefined environment type " + module["env_type"])
        else:
            raise Exception(
                "Module does not exist in PVEnvironment with the name " + moduleName
            )

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
            A dictionary of the source properties.
        Throws an exception for non existent modules and invalid module types.
        """
        modulesDef = {}
        modules = self._source["pv_model"]
        for key in modules.keys():
            modulesDef[key] = self.getModuleDefinition(key, voltage)
        return modulesDef

    def getModuleNumCells(self, moduleName):
        """
        Gets the module num cells given the module name.

        Parameters
        ----------
        moduleName: String
            Key to the source dictionary that corresponds to the module
            selected.

        Returns
        -------
        int: Number of cells in series within this module.
        """
        modulesDict = self.getModuleMapping()
        return PVEnvironment._cellDefinitions[modulesDict[moduleName]]

    def getSourceNumCells(self):
        """
        Gets the total num cells in the array.

        Returns
        -------
        int: Number of cells in series within the entire array.
        """
        numCells = 0
        for moduleName in self._source["pv_model"].keys():
            numCells += self.getModuleNumCells(moduleName)
        return numCells

    def getModuleEnvironmentDefinition(self, moduleName):
        """
        A stripped down version of getModuleDefinition. Returns just the
        environment definition of the module referenced.

        The environment definition is in the following format:

            envDef = {
                "irradiance": float,    (W/m^2)
                "temperature": float,   (C)
            }

        Parameters
        ----------
        moduleName: String
            Key to the source dictionary that corresponds to the module
            selected. The moduleDef of this module is constructed and returned.

        Returns
        -------
        dict:  moduleDef
            A dictionary of the source environment properties.
        Throws an exception for non existent modules and invalid module types.
        """
        moduleDef = self.getModuleDefinition(moduleName, 0)
        return {
            "irradiance": moduleDef["irradiance"],
            "temperature": moduleDef["temperature"],
        }

    def getSourceEnvironmentDefinition(self):
        """
        Returns a weighted average environment definition of the PVSource model.

        The environment definition is in the following format:

            envDef = {
                "irradiance": float,    (W/m^2)
                "temperature": float,   (C)
            }

        Returns
        -------
        dict: envDef
            A dictionary of the source environment properties, weighted.
        """
        totalIrrad = 0
        totalTemp = 0
        cellCount = 0
        modules = self._source["pv_model"]
        for key in modules.keys():
            module = modules[key]
            numCells = PVEnvironment._cellDefinitions[module["module_type"]]
            cellCount += numCells
            if module["env_type"] == "Array":
                totalIrrad += numCells * module["env_regime"][self._cycle][1]
                totalTemp += numCells * module["env_regime"][self._cycle][2]
            elif module["env_type"] == "Step":
                totalIrrad += numCells * module["env_regime"][0]
                totalTemp += numCells * module["env_regime"][1]
            else:
                raise Exception("Undefined environment type.")

        return {
            "irradiance": totalIrrad / cellCount,
            "temperature": totalTemp / cellCount,
        }

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

    def saveEnvironment(self):
        """
        This function saves the environment file in place of the previous
        environment file. Useful if the user wants to retain interpolation.
        """
        with open(PVEnvironment._fileRoot + self._sourceFile, "w") as fp:
            options = jsbeautifier.default_options()
            options.indent_size = 4
            fp.write(jsbeautifier.beautify(json.dumps(self._source), options))
            json.dump(self._source, fp)
