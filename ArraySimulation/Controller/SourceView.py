"""
SourceView.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/17/20
Last Modified: 11/24/20

Description: The SourceView class represents a visual tab of the Display class
(and the PVSim application window). It displays a simulation of the PVSource
Models, allowing users to interact with it and generate it in real time under
various environmental conditions.

It shows the following IV-PV Curve graphs:
  - Ideal model with Temperature as the independent variable at 1000 G
  - Ideal model Irradiance as the independent variable at 25 C
  - Nonideal model with Temperature as the independent variable at 1000 G
  - Nonideal model Irradiance as the independent variable at 25 C
"""
# Library Imports.
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QGridLayout,
    QWidget,
)
import numpy as np
from time import sleep

# Custom Imports.
from ArraySimulation.Controller.Console import Console
from ArraySimulation.Controller.Graph import Graph
from ArraySimulation.Controller.View import View


class SourceView(View):
    """
    The SourceView class represents a visual tab of the Display class (and the
    PVSim application window). It displays a simulation of the PVSource Models,
    allowing users to interact with it and generate it in real time under
    various environmental conditions.
    """

    # Update rate of any simulation in the program. Upper bound.
    FRAME_RATE = 100

    # Acceptable boundaries for various inputs for the SourceView.
    VOLTAGE_RES_RANGE = [0.001, 0.1]
    IRRADIANCE_RANGE = [0, 1000]
    IRRADIANCE_RES_RANGE = [1, 200]
    TEMPERATURE_RANGE = [0, 80]
    TEMPERATURE_RES_RANGE = [0.5, 20]
    ACCEPTABLE_NUM_CELLS = [1, 2, 4, 8]

    # List of source models that can be used.
    MODELS = ["Ideal", "Nonideal"]

    def __init__(self, datastore, framerate):
        """
        Upon initialization, we perform any data and UI setup required to get
        the SourceView into a default state.
        """
        super(SourceView, self).__init__(datastore=datastore, framerate=framerate)

        self._datastore = {
            "Ideal": {
                "TempIndependent": Graph(
                    title="Ideal Model Temperature Independent @ 1000G",
                    xAxisLabel="Voltage (V)",
                    yAxisLabel="Characteristics",
                    series={"list": []},
                ),
                "IrradIndependent": Graph(
                    title="Ideal Model Irradiance Independent @ 25C",
                    xAxisLabel="Voltage (V)",
                    yAxisLabel="Characteristics",
                    series={"list": []},
                ),
            },
            "Nonideal": {
                "TempIndependent": Graph(
                    title="Nonideal Model Temperature Independent @ 1000G",
                    xAxisLabel="Voltage (V)",
                    yAxisLabel="Characteristics",
                    series={"list": []},
                ),
                "IrradIndependent": Graph(
                    title="Nonideal Model Irradiance Independent @ 25C",
                    xAxisLabel="Voltage (V)",
                    yAxisLabel="Characteristics",
                    series={"list": []},
                ),
            },
            "Arbitrary": Graph(
                title="Single Shot Model",
                xAxisLabel="Voltage (V)",
                yAxisLabel="Characteristics",
                series={"list": []},
            ),
        }

        self._mode = "Single Shot"

        # Layout of widgets onto the tab.
        layoutWidget = QWidget()
        self._layout = layoutWidget
        layoutWidget.layout = QGridLayout()
        layoutWidget.setLayout(layoutWidget.layout)

        self._console = Console()

        # Mandatory widgets.
        self._console.addButton(
            "GenSrcCurve",
            "Generate Source Curves",
            (0, 0),
            (1, 1),
            self._generateSourceCurves,
        )
        self._console.addComboBox(
            "ModeSelection",
            (0, 1),
            (1, 1),
            ["Single Shot", "Irradiance and Temperature Independent Curves"],
            self._showMode,
        )
        self._console.addLabel(
            "StatusLbl",
            (1, 0),
            (1, 2),
        )

        # Single Shot specific widgets.
        # We should have the specific widgets:
        # - Model Selection combo box
        # - Lookup Selection combo box
        # - Irradiance level text box
        # - Temperature level text box
        # - Voltage resolution text box
        # - Status label.
        self._console.addButton(
            "ClrSrcCurve",
            "Clear Source Curves",
            (0, 2),
            (1, 1),
            self._clearSourceCurves,
        )
        self._console.addComboBox("ModelSelection", (0, 3), (1, 1), SourceView.MODELS)
        self._console.addComboBox(
            "LookupSelection", (0, 4), (1, 1), ["UseLookup", "NoLookup"]
        )
        self._console.addTextbox(
            "NumCellsTxtbx",
            (0, 5),
            (1, 1),
            "Number of cells in the module.",
        )
        self._console.addTextbox(
            "IrradTxtbx",
            (0, 6),
            (1, 1),
            "Irradiance (W/M^2)",
        )
        self._console.addTextbox(
            "TempTxtbx",
            (0, 7),
            (1, 1),
            "Temperature (C)",
        )
        self._console.addTextbox(
            "VoltResTxtbx",
            (0, 8),
            (1, 1),
            "Voltage Resolution (V)",
        )

        # Irradiance and Temperature Independent Curve specific widgets.
        # We should have the specific widgets:
        # - Irradiance resolution text box
        # - Temperature resolution text box
        # - Voltage resolution text box
        # - Status label.
        self._console.addTextbox(
            "IrradResTxtbx",
            (0, 2),
            (1, 1),
            "Irradiance Resolution (W/M^2)",
        )
        self._console.addTextbox(
            "TempResTxtbx",
            (0, 3),
            (1, 1),
            "Temperature Resolution (C)",
        )
        self._console.addTextbox(
            "VoltResTxtbx2",
            (0, 4),
            (1, 1),
            "Voltage Resolution (V)",
        )

        # Add the graphs to the UI.
        self._layout.layout.addWidget(
            self._datastore["Arbitrary"].getLayout(), 1, 0, 1, 1
        )

        self._layout.layout.addWidget(
            self._datastore["Ideal"]["TempIndependent"].getLayout(),
            1,
            0,
            1,
            1,
        )

        self._layout.layout.addWidget(
            self._datastore["Ideal"]["IrradIndependent"].getLayout(),
            1,
            1,
            1,
            1,
        )

        self._layout.layout.addWidget(
            self._datastore["Nonideal"]["TempIndependent"].getLayout(),
            2,
            0,
            1,
            1,
        )

        self._layout.layout.addWidget(
            self._datastore["Nonideal"]["IrradIndependent"].getLayout(),
            2,
            1,
            1,
            1,
        )

        self._showSingleShotUI()

        self._layout.layout.addWidget(self._console.getLayout(), 0, 0, 1, 2)

    def _generateSourceCurves(self):
        """
        This callback captures a source curve for the selected parameters.
        """
        mode = self._console.getReference("ModeSelection").currentText()

        if mode == "Single Shot":
            self._executeSingleShotMode()
        elif mode == "Irradiance and Temperature Independent Curves":
            self._executeIndCurvesMode()
        else:
            raise Exception("Invalid mode selected:", mode)

    def _clearSourceCurves(self):
        """
        Clears the source curves for the SingleShot mode UI.
        """
        self._datastore["Arbitrary"].clearPoints()

    def _executeSingleShotMode(self):
        """
        Helper function for _generateSourceCurves that generates the Single Shot
        graph.
        """
        controller = self._datastoreParent

        # Get textbox values from the console.
        numCells = self._console.getReference("NumCellsTxtbx").text()
        irradiance = self._console.getReference("IrradTxtbx").text()
        temperature = self._console.getReference("TempTxtbx").text()
        voltageResolution = self._console.getReference("VoltResTxtbx").text()

        # Validate textbox values from the console.
        numCellsRes = self._validate("NumberCells", numCells)
        irradianceRes = self._validate("Irradiance", irradiance)
        temperatureRes = self._validate("Temperature", temperature)
        voltageRes = self._validate("VoltageResolution", voltageResolution)

        # Aggregate errors from the validation input.
        errors = []
        errors += numCellsRes[0]
        errors += irradianceRes[0]
        errors += temperatureRes[0]
        errors += voltageRes[0]

        if not errors:
            # Grab combo box based parameters.
            model = self._console.getReference("ModelSelection").currentText()
            useLookup = self._console.getReference("LookupSelection").currentText()
            useLookupBool = False
            if useLookup == "UseLookup":
                useLookupBool = True

            self._console.getReference("StatusLbl").setText("Building...")

            # Generate the source curves.
            (voltages, currents) = controller.generateSourceCurve(
                numCellsRes[1],
                irradianceRes[1],
                temperatureRes[1],
                0.01,
                model,
                useLookupBool,
            )
            powers = [voltage * current for voltage, current in zip(voltages, currents)]

            # Update the graph.
            self._datastore["Arbitrary"].addSeries(
                model
                + ".lookup:"
                + str(useLookupBool)
                + ".current:temp."
                + str(temperatureRes[1])
                + ":irrad."
                + str(irradianceRes[1])
                + ":numCells."
                + str(numCellsRes[1]),
                {
                    "data": {"x": voltages, "y": currents},
                    "multiplier": 1,
                    "label": "Current (A): "
                    + str(numCellsRes[1])
                    + " cell(s), Temp "
                    + str(temperatureRes[1])
                    + " C, Irrad "
                    + str(irradianceRes[1])
                    + " G",
                    "color": (
                        temperatureRes[1] * 255 / SourceView.TEMPERATURE_RANGE[1],
                        255 - irradianceRes[1] * 255 / SourceView.IRRADIANCE_RANGE[1],
                        numCellsRes[1] * 255 / SourceView.ACCEPTABLE_NUM_CELLS[-1],
                    ),
                },
            )
            self._datastore["Arbitrary"].addSeries(
                model
                + ".lookup:"
                + str(useLookupBool)
                + ".power:temp."
                + str(temperatureRes[1])
                + ":irrad."
                + str(irradianceRes[1])
                + ":numCells."
                + str(numCellsRes[1]),
                {
                    "data": {"x": voltages, "y": powers},
                    "multiplier": 1,
                    "label": "Power (W): "
                    + str(numCellsRes[1])
                    + " cell(s), Temp "
                    + str(temperatureRes[1])
                    + " C, Irrad "
                    + str(irradianceRes[1])
                    + " G",
                    "color": (
                        temperatureRes[1] * 255 / SourceView.TEMPERATURE_RANGE[1],
                        255 - irradianceRes[1] * 255 / SourceView.IRRADIANCE_RANGE[1],
                        255
                        - numCellsRes[1] * 255 / SourceView.ACCEPTABLE_NUM_CELLS[-1],
                    ),
                },
            )

            self._console.getReference("StatusLbl").setText("Success.")
        else:
            self._console.getReference("StatusLbl").setText(
                "\n".join(str(error) for error in errors)
            )

    def _executeIndCurvesMode(self):
        """
        Helper function for _generateSourceCurves that generates the Independent
        Curves graphs.
        """
        # Clear points for each graph.
        self._datastore["Ideal"]["TempIndependent"].clearPoints()
        self._datastore["Nonideal"]["TempIndependent"].clearPoints()
        self._datastore["Ideal"]["IrradIndependent"].clearPoints()
        self._datastore["Nonideal"]["IrradIndependent"].clearPoints()

        controller = self._datastoreParent

        # Get textbox values from the console.
        irradResolution = self._console.getReference("IrradResTxtbx").text()
        tempResolution = self._console.getReference("TempResTxtbx").text()
        voltageResolution = self._console.getReference("VoltResTxtbx2").text()

        # Validate textbox values from the console.
        irradRes = self._validate("IrradianceResolution", irradResolution)
        tempRes = self._validate("TemperatureResolution", tempResolution)
        voltageRes = self._validate("VoltageResolution", voltageResolution)

        # Aggregate errors from the validation input.
        errors = []
        errors += irradRes[0]
        errors += tempRes[0]
        errors += voltageRes[0]

        if not errors:
            # Generate the source curves.
            for model in ["Ideal", "Nonideal"]:
                # Build temperature independent graphs.
                self._console.getReference("StatusLbl").setText(
                    "Building the " + model + " temperature independent graph."
                )
                for temperature in np.arange(
                    SourceView.TEMPERATURE_RANGE[0],
                    SourceView.TEMPERATURE_RANGE[1] + tempRes[1],
                    tempRes[1],
                ):
                    # Note that by default we try to use lookups.
                    (voltages, currents) = controller.generateSourceCurve(
                        1, 1000, temperature, voltageRes[1], model, True
                    )
                    powers = [
                        voltage * current
                        for voltage, current in zip(voltages, currents)
                    ]

                    # Update the graph.
                    self._datastore[model]["TempIndependent"].addSeries(
                        model + ".current:temp." + str(temperature),
                        {
                            "data": {"x": voltages, "y": currents},
                            "multiplier": 1,
                            "label": "Current (A): Temperature "
                            + str(temperature)
                            + " C",
                            "color": (
                                temperature * 255 / SourceView.TEMPERATURE_RANGE[1],
                                255
                                - temperature * 255 / SourceView.TEMPERATURE_RANGE[1],
                                255
                                - temperature * 255 / SourceView.TEMPERATURE_RANGE[1],
                            ),
                        },
                    )
                    self._datastore[model]["TempIndependent"].addSeries(
                        model + ".power:temp." + str(temperature),
                        {
                            "data": {"x": voltages, "y": powers},
                            "multiplier": 1,
                            "label": "Power (W): Temperature "
                            + str(temperature)
                            + " C",
                            "color": (
                                temperature * 255 / SourceView.TEMPERATURE_RANGE[1],
                                255
                                - temperature * 255 / SourceView.TEMPERATURE_RANGE[1],
                                temperature * 255 / SourceView.TEMPERATURE_RANGE[1],
                            ),
                        },
                    )

                # Build irradiance independent graphs.
                self._console.getReference("StatusLbl").setText(
                    "Building the " + model + " irradiance independent graph."
                )
                for irradiance in np.arange(
                    SourceView.IRRADIANCE_RANGE[0],
                    SourceView.IRRADIANCE_RANGE[1] + irradRes[1],
                    irradRes[1],
                ):
                    # Note that by default we try to use lookups.
                    (voltages, currents) = controller.generateSourceCurve(
                        1, irradiance, 25, voltageRes[1], model, True
                    )
                    powers = [
                        voltage * current
                        for voltage, current in zip(voltages, currents)
                    ]

                    # Update the graph.
                    self._datastore[model]["IrradIndependent"].addSeries(
                        model + ".current:irrad." + str(irradiance),
                        {
                            "data": {"x": voltages, "y": currents},
                            "multiplier": 1,
                            "label": "Current (A): Irradiance "
                            + str(irradiance)
                            + " G",
                            "color": (
                                122
                                + irradiance * 255 / SourceView.IRRADIANCE_RANGE[1] / 2,
                                122
                                + irradiance * 255 / SourceView.IRRADIANCE_RANGE[1] / 2,
                                255 - irradiance * 255 / SourceView.IRRADIANCE_RANGE[1],
                            ),
                        },
                    )
                    self._datastore[model]["IrradIndependent"].addSeries(
                        model + ".power:irrad." + str(irradiance),
                        {
                            "data": {"x": voltages, "y": powers},
                            "multiplier": 1,
                            "label": "Power (W): Irradiance " + str(irradiance) + " G",
                            "color": (
                                122
                                + irradiance * 255 / SourceView.IRRADIANCE_RANGE[1] / 2,
                                255
                                - irradiance * 255 / SourceView.IRRADIANCE_RANGE[1] / 2,
                                255 - irradiance * 255 / SourceView.IRRADIANCE_RANGE[1],
                            ),
                        },
                    )

            self._console.getReference("StatusLbl").setText("Success.")
        else:
            self._console.getReference("StatusLbl").setText(
                "\n".join(str(error) for error in errors)
            )

    def _validate(self, _type, value):
        """
        Attempts to validate the value of an assumed type. Returns an error
        array upon failure.

        Parameters
        ----------
        _type: String
            String defined value type.
        value: String
            Value to be parsed.

        Returns
        -------
        A tuple of the format:
            ([errors], val)

        Upon success, errors is an empty list and val has a value.
        Upon failure, errors is a populated list of errors and val is None.
        """
        errors = []
        val = None

        if value is None or value == "":
            errors.append("No value. Please type something in!")
        elif _type == "Irradiance":
            try:
                valCandidate = float(value)
                if (
                    SourceView.IRRADIANCE_RANGE[0] <= valCandidate
                    and valCandidate <= SourceView.IRRADIANCE_RANGE[1]
                ):
                    val = valCandidate
                else:
                    errors.append(
                        "The irradiance value is outside of range ["
                        + str(SourceView.IRRADIANCE_RANGE[0])
                        + ","
                        + str(SourceView.IRRADIANCE_RANGE[1])
                        + "]: "
                        + str(valCandidate)
                        + "."
                    )
            except ValueError:
                errors.append(
                    "The irradiance value is not of type int or float: "
                    + str(val)
                    + "."
                )
        elif _type == "Temperature":
            try:
                valCandidate = float(value)
                if (
                    SourceView.TEMPERATURE_RANGE[0] <= valCandidate
                    and valCandidate <= SourceView.TEMPERATURE_RANGE[1]
                ):
                    val = valCandidate
                else:
                    errors.append(
                        "The temperature value is outside of range ["
                        + str(SourceView.TEMPERATURE_RANGE[0])
                        + ","
                        + str(SourceView.TEMPERATURE_RANGE[1])
                        + "]: "
                        + str(valCandidate)
                        + "."
                    )
            except ValueError:
                errors.append(
                    "The temperature value is not of type int or float: "
                    + str(val)
                    + "."
                )
        elif _type == "VoltageResolution":
            try:
                valCandidate = float(value)
                if (
                    SourceView.VOLTAGE_RES_RANGE[0] <= valCandidate
                    and valCandidate <= SourceView.VOLTAGE_RES_RANGE[1]
                ):
                    val = valCandidate
                else:
                    errors.append(
                        "The voltage resolution is outside of range ["
                        + str(SourceView.VOLTAGE_RES_RANGE[0])
                        + ","
                        + str(SourceView.VOLTAGE_RES_RANGE[1])
                        + "]: "
                        + str(valCandidate)
                        + "."
                    )
            except ValueError:
                errors.append(
                    "The voltage resolution is not of type int or float: "
                    + str(val)
                    + "."
                )
        elif _type == "IrradianceResolution":
            try:
                valCandidate = float(value)
                if (
                    SourceView.IRRADIANCE_RES_RANGE[0] <= valCandidate
                    and valCandidate <= SourceView.IRRADIANCE_RES_RANGE[1]
                ):
                    val = valCandidate
                else:
                    errors.append(
                        "The irradiance resolution is outside of range ["
                        + str(SourceView.IRRADIANCE_RES_RANGE[0])
                        + ","
                        + str(SourceView.IRRADIANCE_RES_RANGE[1])
                        + "]: "
                        + str(valCandidate)
                        + "."
                    )
            except ValueError:
                errors.append(
                    "The irradiance resolution is not of type int or float: "
                    + str(val)
                    + "."
                )
        elif _type == "TemperatureResolution":
            try:
                valCandidate = float(value)
                if (
                    SourceView.TEMPERATURE_RES_RANGE[0] <= valCandidate
                    and valCandidate <= SourceView.TEMPERATURE_RES_RANGE[1]
                ):
                    val = valCandidate
                else:
                    errors.append(
                        "The temperature resolution is outside of range ["
                        + str(SourceView.TEMPERATURE_RES_RANGE[0])
                        + ","
                        + str(SourceView.TEMPERATURE_RES_RANGE[1])
                        + "]: "
                        + str(valCandidate)
                        + "."
                    )
            except ValueError:
                errors.append(
                    "The temperature resolution is not of type int or float: "
                    + str(val)
                    + "."
                )
        elif _type == "NumberCells":
            try:
                valCandidate = int(value)
                if valCandidate in SourceView.ACCEPTABLE_NUM_CELLS:
                    val = valCandidate
                else:
                    errors.append(
                        "The number of cells is not in the list of acceptable number of cells: "
                        + str(valCandidate)
                        + " ["
                        + ", ".join(
                            str(entry) for entry in SourceView.ACCEPTABLE_NUM_CELLS
                        )
                        + "]."
                    )
            except ValueError:
                errors.append(
                    "The number of cells is not of type int: " + str(val) + "."
                )
        else:
            errors.append("The input type is not defined: " + _type + ".")

        return (errors, val)

    def _showMode(self, _idx):
        """
        Updates the UI to show relevant graphs and options based on the mode.

        Parameters
        ----------
        _idx: int
            Unused parameter that is the index of the item in the combo box
            selected.
        """
        mode = self._console.getReference("ModeSelection").currentText()
        if mode != self._mode:
            if mode == "Single Shot":
                self._showSingleShotUI()
                self._mode = mode
            elif mode == "Irradiance and Temperature Independent Curves":
                self._showIndCurvesUI()
                self._mode = mode
            else:
                raise Exception("Invalid mode selected:", mode)

    def _showSingleShotUI(self):
        """
        Subroutine to display all components of the SingleShot mode UI.
        """
        # Manage console widgets.
        self._console.hideConsoleWidgets(
            ["IrradResTxtbx", "TempResTxtbx", "VoltResTxtbx2"]
        )
        self._console.showConsoleWidgets(
            [
                "ClrSrcCurve",
                "ModelSelection",
                "LookupSelection",
                "NumCellsTxtbx",
                "IrradTxtbx",
                "TempTxtbx",
                "VoltResTxtbx",
            ]
        )

        # Hide the graphs. We assume that the following graphs should be hidden:
        # - Ideal, Temperature Independent
        # - Ideal, Irradiance Independent
        # - Nonideal, Temperature Independent
        # - Nonidea, Irradiance Independent
        self._datastore["Ideal"]["TempIndependent"].getLayout().hide()
        self._datastore["Ideal"]["IrradIndependent"].getLayout().hide()
        self._datastore["Nonideal"]["TempIndependent"].getLayout().hide()
        self._datastore["Nonideal"]["IrradIndependent"].getLayout().hide()

        # Add our Single Shot graph to the UI.
        self._datastore["Arbitrary"].getLayout().show()

    def _showIndCurvesUI(self):
        """
        Subroutine to display all components of the Independent Curves mode UI.
        """
        # Manage console widgets.
        self._console.hideConsoleWidgets(
            [
                "ClrSrcCurve",
                "ModelSelection",
                "LookupSelection",
                "NumCellsTxtbx",
                "IrradTxtbx",
                "TempTxtbx",
                "VoltResTxtbx",
            ]
        )
        self._console.showConsoleWidgets(
            ["IrradResTxtbx", "TempResTxtbx", "VoltResTxtbx2"]
        )

        # Hide the graphs. We assume that the following graph should be hidden:
        # - Arbitrary
        self._datastore["Arbitrary"].getLayout().hide()

        # Add the graphs to the UI.
        self._datastore["Ideal"]["TempIndependent"].getLayout().show()
        self._datastore["Ideal"]["IrradIndependent"].getLayout().show()
        self._datastore["Nonideal"]["TempIndependent"].getLayout().show()
        self._datastore["Nonideal"]["IrradIndependent"].getLayout().show()
