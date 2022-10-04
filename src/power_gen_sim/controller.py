"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Power Gen Sim Controller. 
@version    3.0.0
@date       2022-10-04
"""

import pyqtgraph as pg
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QSizePolicy,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)


class PowerGenSimController:
    def __init__(self):
        self.data = self.Data(self)
        self.ui = self.UI(self)

    def get_data(self):
        return [self.data, "Power Gen Sim"]

    def get_ui(self):
        return [self.ui, "Power Gen Sim"]

    class Data:
        def __init__(self, parent):
            self.parent = parent

    class UI(QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            main_layout = QGridLayout()
            self.setLayout(main_layout)

            self.add_sublayout_system_diagram()
            main_layout.addWidget(self.system_diagram_ui["display"], 0, 0, 4, 5)

            self.add_sublayout_pv_window()
            main_layout.addWidget(self.pv_window_ui["display"], 4, 0, 4, 5)

            self.add_sublayout_graphs()
            main_layout.addWidget(self.graph_ui["display"], 0, 5, 8, 10)

            self.add_sublayout_toolbar()
            main_layout.addWidget(self.toolbar_ui["display"], 8, 0, 2, 15)

        def add_sublayout_system_diagram(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("Simulation Cycle")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 1)

            # Simulation Selector

            # Environment Label

            # PV Label

            # MPPT Label

            # DC-DC Label

            # Load Label

            # Graphic arrows between labels

            self.system_diagram_ui = {
                "display": display,
                "selectors": {"sel_simulation": None},
                "labels": {},
            }

        def add_sublayout_pv_window(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("Photovoltaic Config.")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 2)

            # Selectable frame of dynamically added modules.

            self.pv_window_ui = {"display": display, "selectors": {}}

        def add_sublayout_graphs(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Source Characteristics Graphs. Added dynamically.
            layout_source_char = QStackedLayout()
            layout.addLayout(layout_source_char, 0, 0, 1, 1)

            # In-place VREF Graph.
            graph_vref = pg.PlotWidget()
            graph_vref.setTitle("MPPT VREF Over Source IV/PV Curve")
            graph_vref.setLabel("left", "Current (A)")
            graph_vref.setLabel("bottom", "Voltage (V)")
            graph_vref.setLabel("right", "Power (W)")
            graph_vref.showGrid(x=True, y=True)
            layout.addWidget(graph_vref, 0, 1, 1, 1)

            # MPPT Chracteristics Graph.
            graph_mppt = pg.PlotWidget()
            graph_mppt.setTitle("MPPT Characteristics Over Time")
            # NOTE: Three series: current (A), power (W), and voltage (V)
            graph_mppt.setLabel("bottom", "Time (steps)")
            graph_mppt.showGrid(x=True, y=True)
            layout.addWidget(graph_mppt, 1, 0, 1, 1)

            # TODO: Missing Power Comparison Graph.
            graph_power = pg.PlotWidget()
            graph_power.setTitle("Power Comparison Over Time")
            graph_power.setLabel("left", "Power (Ideal, W)")
            graph_power.setLabel("bottom", "Time (steps)")
            graph_power.setLabel("right", "Power (Actual, W)")
            graph_power.showGrid(x=True, y=True)
            # layout.addWidget(graph_power, row, column, rowSpan, columnSpan)

            # Efficiency Characteristics Graph.
            graph_eff = pg.PlotWidget()
            graph_eff.setTitle("Efficiency Characteristics Over Time")
            # NOTE: Three series; % difference, % cycles < 5% deviation from
            # max, % tracking efficiency
            graph_eff.setLabel("bottom", "Time (steps)")
            graph_eff.showGrid(x=True, y=True)
            layout.addWidget(graph_eff, 1, 1, 1, 1)

            self.graph_ui = {
                "display": display,
                "selectors": {
                    "source": layout_source_char,
                    "vref": graph_vref,
                    "power": graph_power,
                    "mppt": graph_mppt,
                    "eff": graph_eff,
                },
            }

        def add_sublayout_toolbar(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("Toolbar (TEMP)")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 2)

            # From left to right:

            # Button to color PV Window modules by ID.

            # Button to color PV Window modules by irradiance.

            # Button to color PV Window modules by temperature.

            # Slider to adjust step time of all times advanced in the simulator.

            # Button to load a particular simulation capture file.

            # Button to save simulation into a simulation capture file.

            # Button to start the simulation from the beginning.

            self.toolbar_ui = {"display": display, "selectors": {}}
