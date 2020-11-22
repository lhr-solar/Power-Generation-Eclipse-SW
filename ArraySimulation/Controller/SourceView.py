"""
SourceView.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 10/17/20
Last Modified: 10/17/20

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

        self._button = Console()
        self._button.addButton(
            "0", "Init Pipeline", (0, 0), (1, 1), self._initializePipeline
        )
        self._button.addButton(
            "0",
            "Iter Pipeline",
            (0, 1),
            (1, 1),
            self._generateSourceFromPipeline,
        )
        self._button.addButton(
            "0", "Reset Pipeline", (0, 2), (1, 1), self._resetPipeline
        )

        layoutWidget.layout.addWidget(self._button.getLayout(), 0, 0, 1, 2)

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

    def _initializePipeline(self):
        """
        This callback initializes the data pipeline for a source simulation.
        """
        print("Callback init triggered")
        controller = self._datastoreParent
        controller.setupSimEnvironment((1000, 25), 200)

    def _generateSourceFromPipeline(self):
        """
        Iterates a single cycle in the pipeline and updates the datastore.
        """
        print("Callback iter triggered")
        controller = self._datastoreParent
        controller.setupSimSource("Ideal", False)
        controller.iteratePipelineCycleSource()
        for entry in controller.datastore["sourceOutput"][0]["IV"]:
            self._datastore["Ideal"]["TempIndependent"].addPoint(
                "current", entry[0], entry[1]
            )
            self._datastore["Ideal"]["TempIndependent"].addPoint(
                "power", entry[0], entry[0] * entry[1]
            )
        self._datastoreParent.resetPipeline(0.0)

        controller.setupSimSource("Nonideal", True)
        controller.iteratePipelineCycleSource()
        for entry in controller.datastore["sourceOutput"][0]["IV"]:
            self._datastore["Nonideal"]["TempIndependent"].addPoint(
                "current", entry[0], entry[1]
            )
            self._datastore["Nonideal"]["TempIndependent"].addPoint(
                "power", entry[0], entry[0] * entry[1]
            )
        self._datastoreParent.resetPipeline(0.0)

        controller.setupSimSource("Nonideal", False)
        controller.iteratePipelineCycleSource()
        for entry in controller.datastore["sourceOutput"][0]["IV"]:
            self._datastore["Nonideal"]["IrradIndependent"].addPoint(
                "current", entry[0], entry[1]
            )
            self._datastore["Nonideal"]["IrradIndependent"].addPoint(
                "power", entry[0], entry[0] * entry[1]
            )
        self._datastoreParent.resetPipeline(0.0)

    def _resetPipeline(self):
        """
        Resets the pipeline.
        """
        print("Callback reset triggered")
        self._datastore["Ideal"]["TempIndependent"].clearPoints()
        self._datastore["Nonideal"]["TempIndependent"].clearPoints()
        print(self._datastoreParent.datastore)
