"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Power Gen Sim Controller. 
@version    3.0.0
@date       2022-10-04
"""

import pyqtgraph as pg
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (QFrame, QGridLayout, QLabel, QPushButton,
                             QSizePolicy, QSlider, QStackedLayout, QWidget)


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
            main_layout.addWidget(self.system_diagram_ui["display"], 0, 0, 3, 5)

            self.add_sublayout_pv_window()
            main_layout.addWidget(self.pv_window_ui["display"], 3, 0, 5, 5)

            self.add_sublayout_graphs()
            main_layout.addWidget(self.graph_ui["display"], 0, 5, 8, 10)

            self.add_sublayout_toolbar()
            main_layout.addWidget(self.toolbar_ui["display"], 8, 0, 2, 15)

        def add_sublayout_system_diagram(self):
            display = QFrame()
            layout = QGridLayout()
            layout_stacked = QStackedLayout()
            layout_stacked.setStackingMode(QStackedLayout.StackingMode.StackAll)
            display.setLayout(layout)

            layout_background_widget = QWidget()
            layout_background = QGridLayout()

            # Title Label
            title = QLabel("Simulation Cycle")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 1)
            layout.addLayout(layout_stacked, 1, 0, 1, 1)

            # Background Image
            image_underlay = QLabel("Model Overlay")
            image_underlay.setPixmap(QPixmap("./src/power_gen_sim/model.png"))
            image_underlay.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_underlay.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout_background.addWidget(image_underlay, 0, 0, 1, 1)

            layout_background_widget.setLayout(layout_background)

            layout_selectors_widget = QWidget()
            layout_selectors = QGridLayout()
            layout_selectors.setSpacing(0)

            button_size = [4, 12]

            # Environmental Simulation Selector Button
            selector_env_sim = QPushButton()
            selector_env_sim.setStyleSheet("background-color: rgba(255, 0, 0, 100); border: None;")
            selector_env_sim.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            selector_env_sim.clicked.connect(self.select_env_model)
            layout_selectors.addWidget(selector_env_sim, 1, 1, *button_size)

            # PV Config Selector
            selector_pv_config = QPushButton()
            selector_pv_config.setStyleSheet("background-color: rgba(255, 0, 0, 100); border: None;")
            selector_pv_config.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            selector_pv_config.clicked.connect(self.select_pv_model)
            layout_selectors.addWidget(selector_pv_config, 1, 17, *button_size)

            # MPPT Algorithm Selector
            selector_mppt_alg = QPushButton()
            selector_mppt_alg.setStyleSheet("background-color: rgba(255, 0, 0, 100); border: None;")
            selector_mppt_alg.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            selector_mppt_alg.clicked.connect(self.select_mppt_alg_model)
            layout_selectors.addWidget(selector_mppt_alg, 7, 17, *button_size)

            # DC-DC Converter Selector
            selector_dc_dc = QPushButton()
            selector_dc_dc.setStyleSheet("background-color: rgba(15, 15, 15, 100); border: None;")
            selector_dc_dc.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            selector_dc_dc.clicked.connect(self.select_dc_dc_model)
            layout_selectors.addWidget(selector_dc_dc, 13, 9, *button_size)

            # Load Selector
            selector_load = QPushButton()
            selector_load.setStyleSheet("background-color: rgba(15, 15, 15, 100); border: None;")
            selector_load.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            selector_load.clicked.connect(self.select_load_model)
            layout_selectors.addWidget(selector_load, 7, 1, *button_size)

            # Padding
            padding = QWidget()
            padding.setStyleSheet("border: None;")
            padding_2 = QWidget()
            padding_2.setStyleSheet("border: None;")
            layout_selectors.addWidget(padding, 0, 29, 18, 1)
            layout_selectors.addWidget(padding_2, 17, 0, 1, 30)

            layout_selectors_widget.setLayout(layout_selectors)

            layout_stacked.addWidget(layout_selectors_widget)
            layout_stacked.addWidget(layout_background_widget)

            self.system_diagram_ui = {
                "display": display,
                "selectors": {"sel_simulation": None},
                "labels": {},
            }

        def select_env_model(self):
            pass

        def select_pv_model(self):
            pass

        def select_mppt_alg_model(self):
            pass

        def select_dc_dc_model(self):
            pass

        def select_load_model(self):
            pass

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
            title = QLabel("Simulation Toolbar")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 9)

            # From left to right:

            # Button to color PV Window modules by ID.
            button_id_color = QPushButton("Color by ID")
            button_id_color.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            button_id_color.clicked.connect(self.recolor_heatmap_by_id)
            layout.addWidget(button_id_color, 1, 0, 1, 1)

            # Button to color PV Window modules by irradiance.
            button_irrad_color = QPushButton("Color by IRRAD")
            button_irrad_color.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            button_irrad_color.clicked.connect(self.recolor_heatmap_by_irrad)
            layout.addWidget(button_irrad_color, 1, 1, 1, 1)

            # Button to color PV Window modules by temperature.
            button_temp_color = QPushButton("Color by TEMP")
            button_temp_color.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            button_temp_color.clicked.connect(self.recolor_heatmap_by_temp)
            layout.addWidget(button_temp_color, 1, 2, 1, 1)

            # Slider to adjust step time of all times advanced in the simulator.
            slider_timestep = QSlider(Qt.Orientation.Horizontal)
            slider_timestep.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            slider_timestep.setTickPosition(QSlider.TickPosition.TicksBothSides)
            slider_timestep.valueChanged[int].connect(self.change_sim_timestep)

            layout.addWidget(slider_timestep, 1, 3, 1, 3)

            # Button to load a particular simulation capture file.
            button_load_cap = QPushButton("Load Sim Capture")
            button_load_cap.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            button_load_cap.clicked.connect(self.load_sim_capture_file)
            layout.addWidget(button_load_cap, 1, 6, 1, 1)

            # Button to save simulation into a simulation capture file.
            button_save_cap = QPushButton("Save Sim Capture")
            button_save_cap.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            button_save_cap.clicked.connect(self.save_sim_capture_file)
            layout.addWidget(button_save_cap, 1, 7, 1, 1)

            # Button to start the simulation from the beginning.
            button_reset_sim = QPushButton("Reset Sim")
            button_reset_sim.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            button_reset_sim.clicked.connect(self.reset_sim)
            layout.addWidget(button_reset_sim, 1, 8, 1, 1)

            self.toolbar_ui = {"display": display, "selectors": {}}

        def recolor_heatmap_by_id(self):
            pass

        def recolor_heatmap_by_irrad(self):
            pass

        def recolor_heatmap_by_temp(self):
            pass

        def change_sim_timestep(self, timestep):
            pass

        def load_sim_capture_file(self):
            pass

        def save_sim_capture_file(self):
            pass

        def reset_sim(self):
            pass