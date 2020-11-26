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

    def __init__(self, datastore):
        """
        Upon initialization, we perform any data and UI setup required to get
        the SourceView into a default state.
        """
        super(SourceView, self).__init__(datastore=datastore)

        self._datastore = {
            "Ideal": {
                "TempIndependent": Graph(
                    graphType="Scatter",
                    title="Ideal Model Temperature Dependence @ 1000G",
                    xAxisLabel="Voltage (V)",
                    yAxisLabel="Characteristics",
                    series={
                        "current": {
                            "data": {"x": [], "y": []},
                            "multiplier": 0.5,
                            "label": "Current (A)",
                        },
                        "power": {
                            "data": {"x": [], "y": []},
                            "multiplier": 1,
                            "label": "Power (W)",
                        },
                        "list": ("current", "power"),
                    },
                ),
                "IrradIndependent": Graph(
                    graphType="Scatter",
                    title="Ideal Model Irradiance Dependence @ 25C",
                    xAxisLabel="Voltage (V)",
                    yAxisLabel="Characteristics",
                    series={
                        "current": {
                            "data": {"x": [], "y": []},
                            "multiplier": 1,
                            "label": "Current (A)",
                        },
                        "power": {
                            "data": {"x": [], "y": []},
                            "multiplier": 1,
                            "label": "Power (W)",
                        },
                        "list": ("current", "power"),
                    },
                ),
            },
            "Nonideal": {
                "TempIndependent": Graph(
                    graphType="Scatter",
                    title="Nonideal Model Temperature Dependence @ 1000G",
                    xAxisLabel="Voltage (V)",
                    yAxisLabel="Characteristics",
                    series={
                        "current": {
                            "data": {"x": [], "y": []},
                            "multiplier": 1,
                            "label": "Current (A)",
                        },
                        "power": {
                            "data": {"x": [], "y": []},
                            "multiplier": 1,
                            "label": "Power (W)",
                        },
                        "list": ("current", "power"),
                    },
                ),
                "IrradIndependent": Graph(
                    graphType="Scatter",
                    title="Nonideal Model Irradiance Dependence @ 25C",
                    xAxisLabel="Voltage (V)",
                    yAxisLabel="Characteristics",
                    series={
                        "current": {
                            "data": {"x": [], "y": []},
                            "multiplier": 1,
                            "label": "Current (A)",
                        },
                        "power": {
                            "data": {"x": [], "y": []},
                            "multiplier": 1,
                            "label": "Power (W)",
                        },
                        "list": ("current", "power"),
                    },
                ),
            },
        }

        # Layout of widgets onto the tab.
        layoutWidget = QWidget()
        layoutWidget.layout = QGridLayout()
        layoutWidget.setLayout(layoutWidget.layout)

        self._console = Console()
        self._console.addButton(
            "GenSrcCurve",
            "Generate Source Curves.",
            (0, 0),
            (1, 1),
            self._generateSourceCurves,
        )
        self._console.addTextbox(
            "IrradTxtbx",
            (0, 1),
            (1, 1),
            "Irradiance (W/M^2)",
        )
        self._console.addTextbox(
            "TempTxtbx",
            (0, 2),
            (1, 1),
            "Temperature (C)",
        )
        self._console.addTextbox(
            "VoltResTxtbx",
            (0, 3),
            (1, 1),
            "Voltage Resolution (V)",
        )
        self._console.addLabel(
            "StatusLbl",
            (1, 0),
            (1, 2),
        )

        layoutWidget.layout.addWidget(self._console.getLayout(), 0, 0, 1, 2)

        layoutWidget.layout.addWidget(
            self._datastore["Ideal"]["TempIndependent"].getLayout(), 1, 0, 1, 1
        )

        layoutWidget.layout.addWidget(
            self._datastore["Ideal"]["IrradIndependent"].getLayout(), 1, 1, 1, 1
        )

        layoutWidget.layout.addWidget(
            self._datastore["Nonideal"]["TempIndependent"].getLayout(),
            2,
            0,
            1,
            1,
        )

        layoutWidget.layout.addWidget(
            self._datastore["Nonideal"]["IrradIndependent"].getLayout(),
            2,
            1,
            1,
            1,
        )

        self._layout = layoutWidget

    def _generateSourceCurves(self):
        """
        This callback captures a source curve for the selected parameters.
        """
        controller = self._datastoreParent

        # Get textbox values from the console.
        irradiance = self._console.getReference("IrradTxtbx").text()
        temperature = self._console.getReference("TempTxtbx").text()
        voltageResolution = self._console.getReference("VoltResTxtbx").text()

        # Validate textbox values from the console.
        irradianceRes = self._validate("Irradiance", irradiance)
        temperatureRes = self._validate("Temperature", temperature)
        voltageRes = self._validate("VoltageResolution", voltageResolution)

        # Aggregate errors from the validation input.
        errors = []
        errors += irradianceRes[0]
        errors += temperatureRes[0]
        errors += voltageRes[0]

        if not errors:
            (voltages, currents) = controller.generateSourceCurve(
                irradianceRes[1], temperatureRes[1], 0.01, "Ideal", False
            )
            powers = [voltage * current for voltage, current in zip(voltages, currents)]

            self._datastore["Ideal"]["TempIndependent"].addPoints(
                "current", voltages, currents
            )
            self._datastore["Ideal"]["TempIndependent"].addPoints(
                "power", voltages, powers
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

        if value is None or value is "":
            errors.append("No value. Please type something in!")
        elif _type == "Irradiance":
            try:
                valCandidate = float(value)
                if 0 <= valCandidate and valCandidate <= 1000:
                    val = valCandidate
                else:
                    errors.append(
                        "The irradiance value is outside of range [0, 1000]: "
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
                if 0 <= valCandidate and valCandidate <= 100:
                    val = valCandidate
                else:
                    errors.append(
                        "The temperature value is outside of range [0, 100]: "
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
                if 0.001 <= valCandidate and valCandidate <= 0.1:
                    val = valCandidate
                else:
                    errors.append(
                        "The voltage resolution is outside of range [0.001, .1]: "
                        + str(valCandidate)
                        + "."
                    )
            except ValueError:
                errors.append(
                    "The voltage resolution is not of type int or float: "
                    + str(val)
                    + "."
                )
        else:
            errors.append("The input type is not defined: " + _type + ".")

        return (errors, val)
