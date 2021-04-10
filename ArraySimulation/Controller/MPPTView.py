"""
MPPTView.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/17/20
Last Modified: 03/06/21

Description: The MPPTView class represents a visual tab of the Display class
(and the PVSim application window). It displays a simulation of the MPPT
algorithm output versus the source model, allowing users to see the decision
making and efficiency of the algorithms in real time under different
environmental conditions.

It shows the following IV-PV Curve graphs:
  - PVSource characteristics over time, plotting voltage, current, power,
    irradiance, and temperature
  - MPPT characteristics over time, plotting voltage, current, power
  - MPPT voltage setpoint on top of the PVSource IV/PV curve at the current cycle
  - Power comparison over time between MPPT and PVSource
  - Efficiency characteristics over time, including:
    - % Difference from maximum power and mppt power
    - % Cycles above 5% difference over time
    - % Tracking efficiency of total possible power generated versus predicted
      power generated
"""
# Library Imports.
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import pathlib
import sys

# Custom Imports.
from ArraySimulation.Controller.Console import Console
from ArraySimulation.Controller.View import View
from ArraySimulation.Controller.Graph import Graph


class MPPTView(View):
    """
    The MPPTView class represents a visual tab of the Display class
    (and the PVSim application window). It displays a simulation of the MPPT
    algorithm output versus the source model, allowing users to see the decision
    making and efficiency of the algorithms in real time under different
    environmental conditions.
    """

    # List of source models that can be used.
    MODELS = ["Ideal", "Nonideal"]

    # List of Global MPPT algorithms that can be used.
    MPPT_GLOBAL_MODELS = ["Voltage Sweep","Simulated Annealing","None"]

    # List of Local MPPT algorithms that can be used.
    MPPT_LOCAL_MODELS = ["PandO", "IC", "FC", "Ternary", "Golden", "Bisection"]

    # List of MPPT stride algorithms that can be used.
    MPPT_STRIDE_MODELS = ["Fixed", "Adaptive", "Bisection", "Optimal"]

    def __init__(self, dataController, framerate):
        """
        Upon initialization, we perform any data and UI setup required to get
        the MPPTView into a default state.
        """
        super(MPPTView, self).__init__(
            dataController=dataController, framerate=framerate
        )

        self._datastore = {
            "SourceChars": Graph(
                title="Source Characteristics Over Cycle Time",
                xAxisLabel="Cycle",
                yAxisLabel="Characteristics",
                series={
                    "voltage": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Voltage (V)",
                        "color": (255, 0, 0),
                    },
                    "current": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Current (A)",
                        "color": (0, 255, 0),
                    },
                    "power": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Power (W)",
                        "color": (0, 0, 255),
                    },
                    "irradiance": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1 / 1000,
                        "label": "Irradiance (G/1000)",
                        "color": (255, 0, 122),
                    },
                    "temperature": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1 / 100,
                        "label": "Temperature (C/100)",
                        "color": (255, 122, 0),
                    },
                    "list": (
                        "voltage",
                        "current",
                        "power",
                        "irradiance",
                        "temperature",
                    ),
                },
            ),
            "MPPTChars": Graph(
                title="MPPT Characteristics Over Cycle Time",
                xAxisLabel="Cycle",
                yAxisLabel="Characteristics",
                series={
                    "voltage": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Voltage (V)",
                        "color": (255, 0, 0),
                    },
                    "current": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Current (A)",
                        "color": (0, 255, 0),
                    },
                    "power": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Power (W)",
                        "color": (0, 0, 255),
                    },
                    "list": ("voltage", "current", "power"),
                },
            ),
            "VRefPosition": Graph(
                graphType="Scatter",
                title="MPPT V_REF Over Source IV/PV Curve",
                xAxisLabel="Voltage (V)",
                yAxisLabel="Current (A)",
                series={
                    "voltage": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Source IV Curve (A)",
                        "color": (255, 0, 0),
                    },
                    "power": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Source PV Curve (W)",
                        "color": (0, 255, 0),
                    },
                    "MPPTVREF": {
                        "data": {"x": [0], "y": [0]},
                        "multiplier": 1,
                        "label": None,
                        "color": (255, 255, 255),
                        "size": 8,  # Twice the size of default.
                    },
                    "list": ("voltage", "power", "MPPTVREF"),
                },
            ),
            "PowerComp": Graph(
                title="Power Comparison Over Cycle Time",
                xAxisLabel="Cycle",
                yAxisLabel="Power (W)",
                series={
                    "MPPTPower": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "MPPT Output Power (W)",
                        "color": (255, 0, 0),
                    },
                    "power": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Max Source Power (W)",
                        "color": (0, 255, 0),
                    },
                    "list": ("MPPTPower", "power"),
                },
            ),
            "Efficiency": Graph(
                title="Efficiency Characteristics Over Cycle Time",
                xAxisLabel="Cycle",
                yAxisLabel="Efficiency (%)",
                series={
                    "percentYield": {
                        "data": {"x": [], "y": []},
                        "multiplier": 100,
                        "label": "% Yield",
                        "color": (255, 0, 0),
                    },
                    "cyclesThreshold": {
                        "data": {"x": [], "y": []},
                        "multiplier": 100,
                        "label": "% Cycles Less Than 95% Yield",
                        "color": (0, 255, 0),
                    },
                    "trackingEff": {
                        "data": {"x": [], "y": []},
                        "multiplier": 100,
                        "label": "% Tracking Efficiency",
                        "color": (0, 0, 255),
                    },
                    "list": ("percentYield", "cyclesThreshold", "trackingEff"),
                },
            ),
        }

        # Layout of widgets onto the tab.
        layoutWidget = QWidget()
        self._layout = layoutWidget
        layoutWidget.layout = QGridLayout()
        layoutWidget.setLayout(layoutWidget.layout)

        self._console = Console()
        # Mandatory widgets.
        self._console.addButton(
            "RunAlgorithm",
            "Execute MPPT Algorithm",
            (0, 0),
            (1, 1),
            self._executeMPPTAlgorithm,
        )

        self._console.addTextbox(
            "MaxCycleTextbx",
            (0, 1),
            (1, 1),
            "Maximum cycle to execute to.",
        )

        self._console.addLabel("StatusLbl", (1, 0), (1, 2))

        self._console.addComboBox("ModelSelection", (0, 2), (1, 1), MPPTView.MODELS)
        self._console.addComboBox(
            "GlobalMPPTAlgorithmSelection", (0, 3), (1, 1), MPPTView.MPPT_GLOBAL_MODELS
        )
        self._console.addComboBox(
            "LocalMPPTAlgorithmSelection", (0, 4), (1, 1), MPPTView.MPPT_LOCAL_MODELS
        )
        self._console.addComboBox(
            "AlgorithmStrideSelection", (0, 5), (1, 1), MPPTView.MPPT_STRIDE_MODELS
        )

        # TODO: may put p somewhere else so it's constantly being updated. Of
        # course, keep in mind changing indices can mess with algorithm execution.
        p = pathlib.Path("./External/")
        self._console.addComboBox(
            "EnvironmentSelection", (0, 6), (1, 1), [x.stem for x in p.glob("*.json")]
        )

        self._layout.layout.addWidget(
            self._datastore["SourceChars"].getLayout(), 1, 0, 1, 1
        )

        self._layout.layout.addWidget(
            self._datastore["MPPTChars"].getLayout(), 2, 0, 1, 1
        )

        self._layout.layout.addWidget(
            self._datastore["VRefPosition"].getLayout(), 1, 1, 1, 2
        )

        self._layout.layout.addWidget(
            self._datastore["PowerComp"].getLayout(), 2, 1, 1, 1
        )

        self._layout.layout.addWidget(
            self._datastore["Efficiency"].getLayout(), 2, 2, 1, 1
        )

        self._layout.layout.addWidget(self._console.getLayout(), 0, 0, 1, 3)

    def _executeMPPTAlgorithm(self):
        """
        This callback executes the MPPT algorithm for the selected parameters.
        """
        self._clearGraphs()

        # Get options from combo boxes and textboxes.
        sourceModel = self._console.getReference("ModelSelection").currentText()
        environmentProfile = self._console.getReference(
            "EnvironmentSelection"
        ).currentText()
        MPPTGlobalAlgo = self._console.getReference(
            "GlobalMPPTAlgorithmSelection"
        ).currentText()
        MPPTLocalAlgo = self._console.getReference(
            "LocalMPPTAlgorithmSelection"
        ).currentText()
        MPPTStrideAlgo = self._console.getReference(
            "AlgorithmStrideSelection"
        ).currentText()
        maxCycle = self._console.getReference("MaxCycleTextbx").text()
        maxCycleRes = self._validate("MaxCycle", maxCycle)

        errors = []
        errors += maxCycleRes[0]

        if not errors:
            controller = self._datastoreParent
            controller.resetPipeline(
                # TODO: case for tuple.
                sourceModel,
                environmentProfile + ".json",
                maxCycleRes[1],
                MPPTGlobalAlgo,
                MPPTLocalAlgo,
                MPPTStrideAlgo,
            )
            (cycleResults, continueBool) = controller.iteratePipelineCycleMPPT()

            powerStore = {  # TODO: maybe change naming later? Or never...
                "actualPower": 0,  # Current Cycle Actual Power
                "theoreticalPower": 0,  # Current Cycle Theoretical Power
                "cycleData": [0, 0],  # [Num cycles below threshold, Total cycles]
                "energyData": [
                    0,
                    0,
                ],  # [Total Energy Generated, Total Theoretical Energy]
            }

            self.pipelineData = {
                "continueBool": continueBool,
                "executionIdx": 0,
                "cycleResults": cycleResults,
                "powerStore": powerStore,
            }

            # Execute a timer thread for the duration of the generating the MPPT
            # algorithm graphs.
            self.timer = QTimer()
            self.timer.timeout.connect(self._executeMPPTAlgorithmHelper)
            self.timer.start(self._SECOND / self._framerate)
        else:
            self._console.getReference("StatusLbl").setText(
                "\n".join(str(error) for error in errors)
            )

    def _executeMPPTAlgorithmHelper(self):
        """
        This helper function is executed by a QTimer when enabled by
        _executeMPPTAlgorithm. It calculates results returned by the pipeline
        and displays it on the relevant graphs.
        """
        controller = self._datastoreParent
        idx = self.pipelineData["executionIdx"]
        cycleResults = self.pipelineData["cycleResults"]
        powerStore = self.pipelineData["powerStore"]

        # Update derived data structures
        VREF = round(
            cycleResults["mpptOutput"][idx], 2
        )  # TODO: I don't think we should be doing rounding here. Do it in GlobalMPPT and PVSource instead.
        IVList = cycleResults["sourceOutput"][idx]["IV"]
        print("VREF: " + str(VREF))
        # print(IVList)
        MPPTCurrOut = [curr for (volt, curr) in IVList if round(volt, 2) == VREF]
        # Percent Yield
        powerStore["actualPower"] = VREF * MPPTCurrOut[0]
        powerStore["theoreticalPower"] = (
            cycleResults["sourceOutput"][idx]["edge"][2][0]
            * cycleResults["sourceOutput"][idx]["edge"][2][1]
        )
        percentYield = powerStore["actualPower"] / powerStore["theoreticalPower"]

        # Cycles below threshold
        if percentYield < 0.95:
            powerStore["cycleData"][0] += 1
        powerStore["cycleData"][1] += 1
        percentThreshold = powerStore["cycleData"][0] / powerStore["cycleData"][1]

        # Tracking efficiency
        powerStore["energyData"][0] += powerStore["actualPower"]
        powerStore["energyData"][1] += powerStore["theoreticalPower"]
        trackingEff = powerStore["energyData"][0] / powerStore["energyData"][1]

        # Update the MPPTView UI by plotting graphs.
        self._plotSourceCharacteristics()
        self._plotMPPTCharacteristics(MPPTCurrOut)
        self._plotVRefPosition(IVList, VREF, MPPTCurrOut)
        self._plotPowerComparison(MPPTCurrOut)
        self._plotEfficiencyMetrics(percentYield, percentThreshold, trackingEff)

        # Reiterate the pipeline and store results for next run.
        (cycleResults, continueBool) = controller.iteratePipelineCycleMPPT()
        self.pipelineData["continueBool"] = continueBool
        self.pipelineData["executionIdx"] += 1
        self.pipelineData["cycleResults"] = cycleResults
        self.pipelineData["powerStore"] = powerStore

        if not self.pipelineData["continueBool"]:
            self.timer.timeout.disconnect()
            self._console.getReference("StatusLbl").setText("Success.")

    def _plotSourceCharacteristics(self):
        """
        Plots the source characteristics and environmental characteristics of
        the PV system. One point at a time.

        Utilizes the self.pipelineData object for primary data.
        """
        idx = self.pipelineData["executionIdx"]
        cycleResults = self.pipelineData["cycleResults"]

        # Plot Source Characteristics.
        self._datastore["SourceChars"].addPoint(
            "voltage",
            cycleResults["cycle"][idx],
            cycleResults["sourceOutput"][idx]["edge"][2][0],
        )

        self._datastore["SourceChars"].addPoint(
            "current",
            cycleResults["cycle"][idx],
            cycleResults["sourceOutput"][idx]["edge"][2][1],
        )

        self._datastore["SourceChars"].addPoint(
            "power",
            cycleResults["cycle"][idx],
            cycleResults["sourceOutput"][idx]["edge"][2][0]
            * cycleResults["sourceOutput"][idx]["edge"][2][1],
        )

        self._datastore["SourceChars"].addPoint(
            "irradiance",
            cycleResults["cycle"][idx],
            cycleResults["sourceDef"][idx]["0"]["irradiance"],
        )

        self._datastore["SourceChars"].addPoint(
            "temperature",
            cycleResults["cycle"][idx],
            cycleResults["sourceDef"][idx]["0"]["temperature"],
        )

    def _plotMPPTCharacteristics(self, MPPTCurrOut):
        """
        Plots the MPPT characteristics of the PV system. One point at a time.

        Utilizes the self.pipelineData object for primary data.

        Parameters
        ----------
        MPPTCurrOut: [int]
            Single element list that contains the MPPT current at the given voltage.
        """
        idx = self.pipelineData["executionIdx"]
        cycleResults = self.pipelineData["cycleResults"]

        # Plot MPPT Characteristics.
        self._datastore["MPPTChars"].addPoint(
            "voltage", cycleResults["cycle"][idx], cycleResults["mpptOutput"][idx]
        )

        self._datastore["MPPTChars"].addPoint(
            "current", cycleResults["cycle"][idx], MPPTCurrOut[0]
        )

        self._datastore["MPPTChars"].addPoint(
            "power",
            cycleResults["cycle"][idx],
            cycleResults["mpptOutput"][idx] * MPPTCurrOut[0],
        )

    def _plotVRefPosition(self, IVList, VREF, MPPTCurrOut):
        """
        Plots the reference voltage position relative to the IV and PV curves.

        Parameters
        ----------
        IVList: [(double, double), ..]
            List of voltage current tuples across the IV Curve for the current
            source conditions.
        VREF: double
            Reference voltage output of the MPPT at the end of the given cycle.
        MPPTCurrOut: [double]
            Single element list that contains the MPPT current at the given voltage.
        """
        # Plot VRefPosition.
        self._datastore["VRefPosition"].clearSeries("voltage")
        self._datastore["VRefPosition"].clearSeries("power")

        voltageList = [entry[0] for entry in IVList]
        currentList = [entry[1] for entry in IVList]
        powerList = [entry[0] * entry[1] for entry in IVList]

        self._datastore["VRefPosition"].addPoints("voltage", voltageList, currentList)
        self._datastore["VRefPosition"].addPoints("power", voltageList, powerList)

        self._datastore["VRefPosition"].clearSeries("MPPTVREF")

        idx = self.pipelineData["executionIdx"]
        cycleResults = self.pipelineData["cycleResults"]
        vMax = cycleResults["sourceOutput"][idx]["edge"][2][0]
        iMax = cycleResults["sourceOutput"][idx]["edge"][2][1]
        self._datastore["VRefPosition"].addPoints(
            "MPPTVREF",
            [VREF, VREF, vMax, vMax],
            [MPPTCurrOut[0], VREF * MPPTCurrOut[0], iMax, vMax * iMax],
        )

    def _plotPowerComparison(self, MPPTCurrOut):
        """
        Plots the theoretical power versus the MPPT output power.

        Utilizes the self.pipelineData object for primary data.

        Parameters
        ----------
        MPPTCurrOut: [int]
            Single element list that contains the MPPT current at the given voltage.
        """

        idx = self.pipelineData["executionIdx"]
        cycleResults = self.pipelineData["cycleResults"]

        # Plot Power Comparison.
        self._datastore["PowerComp"].addPoint(
            "power",
            cycleResults["cycle"][idx],
            cycleResults["sourceOutput"][idx]["edge"][2][0]
            * cycleResults["sourceOutput"][idx]["edge"][2][1],
        )

        self._datastore["PowerComp"].addPoint(
            "MPPTPower",
            cycleResults["cycle"][idx],
            cycleResults["mpptOutput"][idx] * MPPTCurrOut[0],
        )
        print(str(cycleResults["cycle"][idx]) + ", "  + str(cycleResults["mpptOutput"][idx] * MPPTCurrOut[0]) + ", "+ str(cycleResults["sourceOutput"][idx]["edge"][2][0]*cycleResults["sourceOutput"][idx]["edge"][2][1]))

    def _plotEfficiencyMetrics(self, percentYield, percentThreshold, trackingEff):
        """
        Plots the efficiency metrics of the MPPT over time.

        Utilizes the self.pipelineData object for primary data.

        Parameters
        ----------
        percentYield: double
            Percentage yield of the current cycle theoretical versus
            experimental power.
        percentThreshold: double
            Percentage of all cycles above a quantified efficiency threshold.
        trackingEff: double
            Overall tracking efficiency in terms of theoretical versus
            experimental energy generated.
        """
        idx = self.pipelineData["executionIdx"]

        # Plot Efficiencies.
        self._datastore["Efficiency"].addPoint(
            "percentYield",
            idx,
            percentYield,
        )
        self._datastore["Efficiency"].addPoint("cyclesThreshold", idx, percentThreshold)
        self._datastore["Efficiency"].addPoint("trackingEff", idx, trackingEff)

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
        elif _type == "MaxCycle":
            try:
                valCandidate = int(value)
                if 0 < valCandidate:
                    val = valCandidate
                else:
                    errors.append(
                        "The max cycle value is outside of range ["
                        + str(1)
                        + ","
                        + "inf"
                        + "]: "
                        + str(valCandidate)
                        + "."
                    )
            except ValueError:
                errors.append(
                    "The max cycle value is not of type int: " + str(val) + "."
                )
        else:
            errors.append("The input type is not defined: " + _type + ".")

        return (errors, val)

    def _clearGraphs(self):
        """
        Clears the source curves for the UI.
        """
        self._datastore["SourceChars"].clearAllSeries()
        self._datastore["MPPTChars"].clearAllSeries()
        self._datastore["VRefPosition"].clearAllSeries()
        self._datastore["PowerComp"].clearAllSeries()
        self._datastore["Efficiency"].clearAllSeries()
