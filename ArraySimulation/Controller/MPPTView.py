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
                    },
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
                    "irradiance": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1 / 1000,
                        "label": "Irradiance (G/1000)",
                    },
                    "temperature": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1 / 100,
                        "label": "Temperature (C/100)",
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
                    },
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
                    "list": ("voltage", "current", "power"),
                },
            ),
            "VRefPosition": Graph(
                title="MPPT V_REF Over Source IV/PV Curve",
                xAxisLabel="Voltage (V)",
                yAxisLabel="Current (A)",
                series={
                    "voltage": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Source IV Curve (A)",
                    },
                    "power": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Source PV Curve (W)",
                    },
                    "MPPTVREF": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": None,
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
                    },
                    "power": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "Max Source Power (W)",
                    },
                    "list": ("MPPTPower", "power"),
                },
            ),
            "Efficiency": Graph(
                title="Efficiency Characteristics Over Cycle Time",
                xAxisLabel="Cycle",
                yAxisLabel="Efficiency (%)",
                series={
                    "maxDiff": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "% Max Diff",
                    },
                    "cyclesThreshold": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "% Cycles Above 5% Diff Threshold",
                    },
                    "trackingEff": {
                        "data": {"x": [], "y": []},
                        "multiplier": 1,
                        "label": "% Tracking Efficiency",
                    },
                    "list": ("maxDiff", "cyclesThreshold", "trackingEff"),
                },
            ),
        }

        # Layout of widgets onto the tab.
        layoutWidget = QWidget()
        layoutWidget.layout = QGridLayout()
        layoutWidget.setLayout(layoutWidget.layout)

        layoutWidget.layout.addWidget(
            self._datastore["SourceChars"].getLayout(), 0, 0, 1, 1
        )

        layoutWidget.layout.addWidget(
            self._datastore["MPPTChars"].getLayout(), 1, 0, 1, 1
        )

        layoutWidget.layout.addWidget(
            self._datastore["VRefPosition"].getLayout(), 0, 1, 1, 2
        )

        layoutWidget.layout.addWidget(
            self._datastore["PowerComp"].getLayout(), 1, 1, 1, 1
        )

        layoutWidget.layout.addWidget(
            self._datastore["Efficiency"].getLayout(), 1, 2, 1, 1
        )

        self._layout = layoutWidget
