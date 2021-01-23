"""
MPPTView.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/17/20
Last Modified: 11/24/20

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

    # List of MPPT algorithms that can be used.
    MPPT_MODELS = ["PandO", "IC", "FC", "Ternary", "Golden", "Bisection"]

    # List of MPPT stride algorithms that can be used.
    MPPT_STRIDE_MODELS = ["Fixed", "Adaptive", "Bisection", "Optimal"]

    def __init__(self, datastore):
        """
        Upon initialization, we perform any data and UI setup required to get
        the SourceView into a default state.
        """
        super(MPPTView, self).__init__(datastore=datastore)

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
        self._console.addComboBox("ModelSelection", (0, 1), (1, 1), MPPTView.MODELS)
        self._console.addComboBox(
            "AlgorithmSelection", (0, 2), (1, 1), MPPTView.MPPT_MODELS
        )
        self._console.addComboBox(
            "AlgorithmStrideSelection", (0, 3), (1, 1), MPPTView.MPPT_STRIDE_MODELS
        )

        self._console.addLabel("StatusLbl", (1, 0), (1, 3))

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

        controller = self._datastoreParent

        # Get options from combo boxes.
        sourceModel = self._console.getReference("ModelSelection").currentText()
        MPPTAlgo = self._console.getReference("AlgorithmSelection").currentText()
        MPPTStrideAlgo = self._console.getReference(
            "AlgorithmStrideSelection"
        ).currentText()

        controller.resetPipeline(sourceModel, MPPTAlgo, MPPTStrideAlgo)
        (cycleResults, continueBool) = controller.iteratePipelineCycleMPPT()

        powerStore = {  # TODO: maybe change naming later? Or never...
            "actualPower": 0,  # Current Cycle Actual Power
            "theoreticalPower": 0,  # Current Cycle Theoretical Power
            "cycleData": [0, 0],  # [Num cycles below threshold, Total cycles]
            "energyData": [0, 0],  # [Total Energy Generated, Total Theoretical Energy]
        }

        # print(cycleResults)

        idx = 0
        while continueBool:
            # Update derived data structures
            VREF = round(cycleResults["mpptOutput"][idx], 2)
            IVList = cycleResults["sourceOutput"][idx]["IV"]
            MPPTCurrOut = [curr for (volt, curr) in IVList if volt == VREF]
            # print(
            #     "Searching for:", VREF
            # )  # TODO: this rounding should be a function of resolution
            # print("In:", IVList)
            # print("We get:", MPPTCurrOut)

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

            # TODO: Plot VRefPosition.
            # self._datastore["VRefPosition"].clearSeries("voltage")
            # self._datastore["VRefPosition"].clearSeries("power")

            # "voltage": {
            #     "data": {"x": [], "y": []},
            #     "multiplier": 1,
            #     "label": "Source IV Curve (A)",
            #     "color": (255, 0, 0),
            # },
            # "power": {
            #     "data": {"x": [], "y": []},
            #     "multiplier": 1,
            #     "label": "Source PV Curve (W)",
            #     "color": (0, 255, 0),

            # self._datastore["VRefPosition"].addPoints(
            #     "voltage",
            #     [],
            #     []
            # )
            # self._datastore["VRefPosition"].addPoints(
            #     "power",
            #     [],
            #     []
            # )

            self._datastore["VRefPosition"].clearSeries("MPPTVREF")
            self._datastore["VRefPosition"].addPoints(
                "MPPTVREF",
                [VREF, VREF],
                [MPPTCurrOut[0], VREF * MPPTCurrOut[0]],
            )

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

            # Plot Efficiencies.
            self._datastore["Efficiency"].addPoint(
                "percentYield",
                idx,
                percentYield,
            )
            self._datastore["Efficiency"].addPoint(
                "cyclesThreshold", idx, percentThreshold
            )
            self._datastore["Efficiency"].addPoint("trackingEff", idx, trackingEff)

            (cycleResults, continueBool) = controller.iteratePipelineCycleMPPT()
            idx += 1

        """
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

    def _clearGraphs(self):
        """
        Clears the source curves for the UI.
        """
        self._datastore["SourceChars"].clearAllSeries()
        self._datastore["MPPTChars"].clearAllSeries()
        self._datastore["VRefPosition"].clearAllSeries()
        self._datastore["PowerComp"].clearAllSeries()
        self._datastore["Efficiency"].clearAllSeries()
