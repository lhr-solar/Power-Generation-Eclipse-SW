"""
DataController.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/19/20
Last Modified: 10/19/20

Description: The DataController class manages the data passed throughout the
program. It exposes objects that represent the state of the application (what
models are running, what data is being captured, commands being executed, etc)
and an API for running the models in the data pipeline.
"""
# Library Imports.

# Custom Imports.
from ArraySimulation.DCDCConverter.DCDCConverter import DCDCConverter
from ArraySimulation.MPPT.MPPT import MPPT
from ArraySimulation.PVEnvironment.PVEnvironment import PVEnvironment
from ArraySimulation.PVSource.PVSource import PVSource


class DataController:
    """
    The DataController class manages the data passed throughout the
    program. It exposes objects that represent the state of the application
    (what models are running, what data is being captured, commands being
    executed, etc) and an API for running the models in the data pipeline.
    """

    def __init__(self):
        """
        Generates objects for the pipeline and initializes a data store that
        records data and prepares it for feeding into the UIController.

        The datastore is in the following format:
        {
            "cycle": [],        # List of integers
            "sourceDef": [],    # List of source environment definitions
            "sourceOutput: [],  # List of dicts in the following format:
                                    {
                                        "current": float,
                                        "IV": list of voltage/current tuples,
                                        "edge": tuple (V_OC, I_SC, (V_MPP, I_MPP))
                                    }
            "mpptOutput": [],   # List of reference voltages
            "dcdcOutput": [],   # List of output Pulse Widths
        }
        """
        # Objects in the pipeline.
        self._PVEnv = PVEnvironment()
        self._PVSource = PVSource()
        self._MPPT = MPPT()
        self._DCDCConverter = DCDCConverter()

        # Data storage.
        self._dataStore = {
            "cycle": [],
            "sourceDef": [],
            "sourceOutput": [],
            "mpptOutput": [],
            "dcdcOutput": [],
        }

        # The reference voltage applied at the start of every cycle.
        self._vREF = 0.0

    # Environment management. The user should h
    def setupSimEnvironment(self, sourceType, maxCycles):
        """
        Sets up the environment object for the simulation.

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
        self._PVEnv.setupModel(sourceType, maxCycles)

    def setSimTime(self, targetCycle):
        """
        Time travel to the specified cycle.

        Parameters
        ----------
        targetCycle: int
            The cycle the simulation should jump to.
        """
        self._environment.setCycle(targetCycle)

    # Source management.
    def setupSimSource(self, modelType, useLookup):
        """
        Sets up the PVSource object for the simulation.

        Parameters
        ----------
        modelType: String
            Specifies the PVCell model used for modeling all photovoltaics.
        useLookup: Bool
            Enables the use of lookup tables, if they exist for the model. If it
            doesn't, we default to the getCurrent function that doesn't use
            lookups.
        """
        self._PVSource.setupModel(modelType, useLookup)

    # MPPT management.
    def setupSimMPPT(self, numCells, modelType, strideType):
        """
        Sets up the MPPT object for the simulation.

        Parameters
        ----------
        numCells: int
            Number of cells expected by the MPPT model.
        modelType: String
            Specifier for the type of model to be used in the MPPT.
        strideType: String
            Specifier for the type of stride model to be used in the MPPT.
        """
        self._MPPT.setupModel(numCells, modelType, strideType)

    # DC-DC Converter management.
    def setupSimDCDCConverter(self, arrayVoltage, loadVoltage):
        """
        Sets up the DC-DC Converter object for the simulation.

        Parameters
        ----------
        arrayVoltage: float
            Expected array output voltage.
        loadVoltage: float
            Initial load voltage. This is the battery in the case of the solar
            array.
        """
        self._DCDCConverter.setup(arrayVoltage, loadVoltage)

    # Simulation pipeline management.
    def resetPipeline(self, voltage):
        """
        Resets components within the pipeline to the default state.
        By default, voltage applied across the source is 0V, and the cycle is 0.
        """
        self._PVEnv.setCycle(0)
        self._MPPT.reset()
        self._DCDCConverter.reset()
        self._dataStore = {
            "cycle": [],
            "sourceDef": [],
            "sourceOutput": [],
            "mpptOutput": [],
            "dcdcOutput": [],
        }
        self._vREF = 0.0

    def iteratePipelineCycle(self):
        """
        Runs an entire cycle through the pipeline, based on the simulation.
        """
        # Get the current simulation cycle.
        cycle = self._PVEnv.getCycle()

        # Retrieve the source definition for the current simulation cycle.
        modulesDef = self._PVEnv.getSourceDefinition(self._vREF)
        envDef = self._PVEnv.getAgglomeratedEnvironmentDefinition()

        # Retrieve the source characteristics given the source definition.
        sourceCurrent = self._PVSource.getSourceCurrent(modulesDef)
        sourceIV = self._PVSource.getIV(modulesDef)
        sourceEdgeChar = self._PVSource.getEdgeCharacteristics(modulesDef)

        # Retrieve the MPPT VREF guess given the source output current.
        vRef = self._MPPT.getReferenceVoltage(
            self._vREF, sourceCurrent, envDef["irradiance"], envDef["temperature"]
        )

        # Generate the pulsewidth of the DC-DC Converter and spit it back out.
        self._DCDCConverter.setPulseWidth(vRef)
        pulseWidth = self._DCDCConverter.getPulseWidth()

        # Store our output into our datastore.
        self._dataStore["cycle"].append(cycle)
        self._dataStore["sourceDef"].append(modulesDef)
        self._dataStore["sourceOutput"].append(
            {"current": sourceCurrent, "IV": sourceIV, "edge": sourceEdgeChar}
        )
        self._dataStore["mpptOutput"].append(vRef)
        self._dataStore["dcdcOutput"].append(pulseWidth)

        # Assign the VREF to apply across the source in the next simulation cycle.
        self._vREF = vRef

        # Increment the current simulation cycle.
        self._PVEnv.cycle()
