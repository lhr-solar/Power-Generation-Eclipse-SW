"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      PV Capture Controller. 
@version    3.0.0
@date       2022-09-14
"""

import os
import re
from datetime import datetime

import pyqtgraph as pg
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator, QIntValidator
from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QStackedLayout,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from src.modeling.pv_model import PVModel
from src.pv_capture.pv_curve_tracer_controller import PVCurveTracerController


class PVCaptureController:
    def __init__(self):
        self.pv_model = PVModel()
        self.curve_tracer = PVCurveTracerController()
        self.data = self.Data(self)
        self.ui = self.UI(self)

    def get_data(self):
        return [self.data, "PV Capture"]

    def get_ui(self):
        return [self.ui, "PV Capture"]

    def print(self, level, text):
        """_summary_
        Formats and sends logging data to the GUI.

        Args:
            level (str): The output level of the text to be displayed.
            text (str): The text to be displayed.
        """
        date = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        output = f"[{level}][{date}] {text}"
        print(output)
        self.ui.print_console(output)

    class Data:
        def __init__(self, parent):
            self.parent = parent
            self.cwd = os.getcwd()

        def get_potential_pv_configs(self):
            configs = {}
            valid_params = [
                "sample_range_low",
                "sample_range_high",
                "step_size",
                "num_iterations",
                "settling_time_ms",
            ]

            # Grab any pv_conf files in data/pv_confs
            obj = os.scandir(path=self.cwd + "/data/pv_confs")
            pv_conf_files = [
                entry.name
                for entry in obj
                if entry.is_file() and entry.name.endswith(".pv_conf")
            ]

            # Check for __pv_type parameter to get the name
            # Then pull out anything matching our valid params.
            for file in pv_conf_files:
                with open(self.cwd + "/data/pv_confs/" + file, "r") as f:
                    pv_type = None
                    lines = f.readlines()
                    for line in lines:
                        blobs = [blob.strip(":\n") for blob in line.split(" ")]
                        if blobs[0] == "__pv_type":
                            pv_type = blobs[1]
                            configs[pv_type] = {}
                        elif pv_type != None and len(blobs) == 2:
                            if blobs[0] in valid_params:
                                configs[pv_type][blobs[0]] = blobs[1]
            return configs

    class UI(QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            main_layout = QGridLayout()
            self.setLayout(main_layout)

            self.add_sublayout_pv_config()
            main_layout.addWidget(self.pv_config_ui["display"], 0, 0, 3, 4)

            self.add_sublayout_comm_config()
            main_layout.addWidget(self.comm_config_ui["display"], 3, 0, 3, 3)

            self.add_sublayout_id()
            main_layout.addWidget(self.id_ui["display"], 3, 3, 1, 1)

            self.add_sublayout_controls()
            main_layout.addWidget(self.control_ui["display"], 4, 3, 2, 1)

            self.add_sublayout_console()
            main_layout.addWidget(self.console_ui["display"], 6, 0, 2, 4)

            self.add_sublayout_char_board()
            main_layout.addWidget(self.char_board_ui["display"], 0, 4, 2, 4)

            self.add_sublayout_graph()
            main_layout.addWidget(self.graph_ui["display"], 2, 4, 6, 4)

        def add_sublayout_pv_config(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("PV Config")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 2)

            # Selectors
            layout_selectors = QFormLayout()
            layout.addLayout(layout_selectors, 1, 0, 5, 1)

            # PV Type Dropdown Selector
            label_pv_type = QLabel("PV Type")
            selector_pv_type = QComboBox()
            layout_selectors.addRow(label_pv_type, selector_pv_type)

            # Call method to autopopulate from parent.data.
            selector_pv_type.addItems(
                self.parent.data.get_potential_pv_configs().keys()
            )

            # Sample Range Selector
            label_sample_range = QLabel("Sample Range")
            selector_sample_range = QLineEdit()
            selector_sample_range.setPlaceholderText("Float '[x, y]' ∈ [0, 1]")
            selector_sample_range.editingFinished.connect(self.update_pv_config)
            layout_selectors.addRow(label_sample_range, selector_sample_range)

            # Step Size Selector
            label_step_size = QLabel("Step Size")
            selector_step_size = QLineEdit()
            selector_step_size.setPlaceholderText("Float 'x' ∈ [0.001, 0.100]")
            selector_step_size.editingFinished.connect(self.update_pv_config)
            selector_step_size.setValidator(QDoubleValidator(0.001, 0.1, 3))
            layout_selectors.addRow(label_step_size, selector_step_size)

            # Num Iterations
            label_num_iters = QLabel("Num Iterations")
            selector_num_iters = QLineEdit()
            selector_num_iters.setPlaceholderText("Int 'x' ∈ [1, 100]")
            selector_num_iters.editingFinished.connect(self.update_pv_config)
            selector_num_iters.setValidator(QIntValidator(1, 100))
            layout_selectors.addRow(label_num_iters, selector_num_iters)

            # Settling Time Per Step
            label_settling_time = QLabel("Settling Time (ms)")
            selector_settling_time = QLineEdit()
            selector_settling_time.setPlaceholderText("Int 'x' ∈ [1, 100]")
            selector_settling_time.editingFinished.connect(self.update_pv_config)
            selector_settling_time.setValidator(QIntValidator(1, 100))
            layout_selectors.addRow(label_settling_time, selector_settling_time)

            # Labels
            layout_labels = QFormLayout()
            layout.addLayout(layout_labels, 1, 1, 5, 1)

            # Empty row
            label_empty = QLabel()
            layout_labels.addRow(label_empty)

            # Num Steps
            label_num_steps = QLabel("Num Steps")
            val_num_steps = QLineEdit()
            val_num_steps.setReadOnly(True)
            layout_labels.addRow(label_num_steps, val_num_steps)

            # Total Samples
            label_total_samples = QLabel("Total Samples")
            val_total_samples = QLineEdit()
            val_total_samples.setReadOnly(True)
            layout_labels.addRow(label_total_samples, val_total_samples)

            # Expected Test Duration (s)
            label_test_duration = QLabel("Test Duration (ms)")
            val_test_duration = QLineEdit()
            val_test_duration.setReadOnly(True)
            layout_labels.addRow(label_test_duration, val_test_duration)

            self.pv_config_ui = {
                "display": display,
                "selectors": {
                    "sel_pv_type": selector_pv_type,
                    "sel_sample_range": selector_sample_range,
                    "sel_step_size": selector_step_size,
                    "sel_num_iters": selector_num_iters,
                    "sel_settle_time": selector_settling_time,
                },
                "labels": {
                    "lab_num_steps": val_num_steps,
                    "lab_tot_steps": val_total_samples,
                    "lab_test_dur": val_test_duration,
                },
            }

            # Default select a PV Type.
            selector_pv_type.currentIndexChanged.connect(self.set_pv_config)
            self.set_pv_config()

        def set_pv_config(self):
            """_summary_
            Pass in default values to the PV Config selectors based on the
            selected.

            Args:
                config_name (enum): Config selected.
            """
            config_name = self.pv_config_ui["selectors"]["sel_pv_type"].currentText()
            configs = self.parent.data.get_potential_pv_configs()
            self.pv_config_ui["selectors"]["sel_sample_range"].setText(
                f"[{configs[config_name]['sample_range_low']}:{configs[config_name]['sample_range_high']}]"
            )
            self.pv_config_ui["selectors"]["sel_step_size"].setText(
                f"{configs[config_name]['step_size']}"
            )
            self.pv_config_ui["selectors"]["sel_num_iters"].setText(
                f"{configs[config_name]['num_iterations']}"
            )
            self.pv_config_ui["selectors"]["sel_settle_time"].setText(
                f"{configs[config_name]['settling_time_ms']}"
            )

            # Force update of labels.
            self.update_pv_config()

        def update_pv_config(self):
            try:
                sample_range = []
                for item in (
                    self.pv_config_ui["selectors"]["sel_sample_range"].text().split(":")
                ):
                    sample_range.append(float(item.strip("[]")))

                # Update config
                config = {
                    "sample_range": sample_range,
                    "step_size": float(
                        self.pv_config_ui["selectors"]["sel_step_size"].text()
                    ),
                    "num_iters": int(
                        self.pv_config_ui["selectors"]["sel_num_iters"].text()
                    ),
                    "settling_time": int(
                        self.pv_config_ui["selectors"]["sel_settle_time"].text()
                    ),
                }
                config["num_steps_per_iter"] = int(
                    (config["sample_range"][1] - config["sample_range"][0])
                    / config["step_size"]
                )
                config["total_samples"] = int(
                    config["num_steps_per_iter"] * config["num_iters"]
                )
                config["test_duration_ms"] = int(
                    config["total_samples"] * config["settling_time"]
                )

                # Update UI
                self.pv_config_ui["labels"]["lab_num_steps"].setText(
                    str(config["num_steps_per_iter"])
                )
                self.pv_config_ui["labels"]["lab_tot_steps"].setText(
                    str(config["total_samples"])
                )
                self.pv_config_ui["labels"]["lab_test_dur"].setText(
                    str(config["test_duration_ms"])
                )

                self.parent.data.pv_config = config
            except Exception as e:
                print("Input error: {0}".format(e))

        def add_sublayout_comm_config(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("COMM Config")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 1)

            # Selectors
            layout_selectors = QFormLayout()
            layout.addLayout(layout_selectors, 1, 0, 1, 1)

            # Config File Selector
            label_config = QLabel("COMM Config")
            selector_com_config = QPushButton("Select File")
            selector_com_config.clicked.connect(self.select_com_config_file)
            layout_selectors.addRow(label_config, selector_com_config)

            # COM Port Selector
            label_com_port = QLabel("COM Port")
            selector_com_port = QComboBox()
            selector_com_port.addItems(self.parent.curve_tracer.list_ports())
            layout_selectors.addRow(label_com_port, selector_com_port)

            # Baud Rate Selector
            label_baud_rate = QLabel("Baud Rate")
            selector_baud_rate = QComboBox()
            selector_baud_rate.addItems(
                [str(item) for item in self.parent.curve_tracer.list_baud_rates()]
            )
            layout_selectors.addRow(label_baud_rate, selector_baud_rate)

            # Parity Bit Selector
            label_parity_bit = QLabel("Parity Bit")
            selector_parity_bit = QComboBox()
            selector_parity_bit.addItems(self.parent.curve_tracer.list_parity())
            layout_selectors.addRow(label_parity_bit, selector_parity_bit)

            # Encoding Scheme Selector
            label_encoding_scheme = QLabel("Encoding Scheme")
            selector_encoding_scheme = QComboBox()
            selector_encoding_scheme.addItems(
                self.parent.curve_tracer.list_encoding_schemes()
            )
            layout_selectors.addRow(label_encoding_scheme, selector_encoding_scheme)

            self.comm_config_ui = {
                "display": display,
                "selectors": {
                    "sel_config_file": selector_com_config,
                    "sel_com_port": selector_com_port,
                    "sel_baud_rate": selector_baud_rate,
                    "sel_parity_bit": selector_parity_bit,
                    "sel_enc_scheme": selector_encoding_scheme,
                },
            }

        def select_com_config_file(self):
            file_path = QFileDialog.getOpenFileName(self, "Open File:", "./", "")
            config = self.parent.curve_tracer.load_com_config(file_path)
            self.comm_config_ui["selectors"]["sel_com_port"].setCurrentText(
                config["com_port"]
            )
            self.comm_config_ui["selectors"]["sel_baud_rate"].setCurrentText(
                str(config["baud_rate"])
            )
            self.comm_config_ui["selectors"]["sel_parity_bit"].setCurrentText(
                config["parity_bit"]
            )
            self.comm_config_ui["selectors"]["sel_enc_scheme"].setCurrentText(
                config["enc_scheme"]
            )

        def add_sublayout_id(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("PV ID")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 1)

            # Name of PV to capture.
            selector_id = QLineEdit()
            selector_id.setObjectName("pv_id")
            selector_id.editingFinished.connect(self.check_pv_id)
            selector_id.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
            )
            selector_id.setPlaceholderText("ex. BV001")
            layout.addWidget(selector_id, 1, 0, 1, 1)

            self.id_ui = {"display": display, "selectors": selector_id}

        def check_pv_id(self):
            # Check if file exists in ./data/captures
            files = self.parent.curve_tracer.list_capture_files()
            files = [file.split(".")[0] for file in files]
            if self.id_ui["selectors"].text() in files:
                self.id_ui["selectors"].setStyleSheet("background-color: #FF0000;")
            else:
                self.id_ui["selectors"].setStyleSheet("background-color: #00FF00;")

        def add_sublayout_controls(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("Controls")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 0)

            # Start Button
            selector_start = QPushButton("START")
            selector_start.setStyleSheet("background-color: #00FF00;")
            selector_start.clicked.connect(self.start_char)
            layout.addWidget(selector_start, 1, 0, 1, 1)

            # Stop Button
            selector_stop = QPushButton("STOP")
            selector_stop.setStyleSheet("background-color: #FF0000;")
            selector_stop.clicked.connect(self.stop_char)
            layout.addWidget(selector_stop, 2, 0, 1, 1)

            # Save Button
            selector_save = QPushButton("SAVE")
            selector_save.clicked.connect(self.save_char)
            layout.addWidget(selector_save, 3, 0, 1, 1)

            self.control_ui = {
                "display": display,
                "selectors": {
                    "sel_start": selector_start,
                    "sel_stop": selector_stop,
                    "sel_save": selector_save,
                },
            }

        def start_char(self):
            self.parent.print("LOG", "Start characterization.")

        def stop_char(self):
            self.parent.print("LOG", "Stop characterization.")

        def save_char(self):
            if self.id_ui["selectors"].text() == "":
                self.parent.print("WARN", "Specify a PV ID to save as.")
            else:
                file_path = (
                    "/data/captures/" + self.id_ui["selectors"].text() + ".capture"
                )
                self.parent.print("LOG", f"Saving characterization to {file_path}")

        def add_sublayout_console(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("Console")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )
            layout.addWidget(title, 0, 0, 1, 0)

            # Status Console
            selector_console = QTextEdit()
            selector_console.setReadOnly(True)
            layout.addWidget(selector_console, 1, 0, 3, 0)

            self.console_ui = {"display": display, "selectors": selector_console}

        def print_console(self, text):
            self.console_ui["selectors"].append(text)

        def add_sublayout_char_board(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("PV Characteristics")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title, 0, 0, 1, 2)

            # Labels left
            layout_labels_left = QFormLayout()
            layout.addLayout(layout_labels_left, 1, 0, 4, 1)

            # Labels right
            layout_labels_right = QFormLayout()
            layout.addLayout(layout_labels_right, 1, 1, 4, 1)

            # V_OC
            label_v_oc = QLabel("V_OC (V)")
            val_v_oc = QLineEdit()
            val_v_oc.setReadOnly(True)
            layout_labels_left.addRow(label_v_oc, val_v_oc)

            # I_SC
            label_i_sc = QLabel("I_SC (A)")
            val_i_sc = QLineEdit()
            val_i_sc.setReadOnly(True)
            layout_labels_left.addRow(label_i_sc, val_i_sc)

            # FF
            label_ff = QLabel("FF (%)")
            val_ff = QLineEdit()
            val_ff.setReadOnly(True)
            layout_labels_left.addRow(label_ff, val_ff)

            # V_MPP
            label_v_mpp = QLabel("V_MPP (V)")
            val_v_mpp = QLineEdit()
            val_v_mpp.setReadOnly(True)
            layout_labels_right.addRow(label_v_mpp, val_v_mpp)

            # I_MPP
            label_i_mpp = QLabel("I_MPP (A)")
            val_i_mpp = QLineEdit()
            val_i_mpp.setReadOnly(True)
            layout_labels_right.addRow(label_i_mpp, val_i_mpp)

            # P_MPP
            label_p_mpp = QLabel("P_MPP (W)")
            val_p_mpp = QLineEdit()
            val_p_mpp.setReadOnly(True)
            layout_labels_right.addRow(label_p_mpp, val_p_mpp)

            self.char_board_ui = {
                "display": display,
                "labels": {
                    "lab_v_oc": val_v_oc,
                    "lab_i_sc": val_i_sc,
                    "lab_v_mpp": val_v_mpp,
                    "lab_i_mpp": val_i_mpp,
                    "lab_p_mpp": val_p_mpp,
                    "lab_ff": val_ff,
                },
            }

        def add_sublayout_graph(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Graph
            graph = pg.PlotWidget()
            graph.setTitle("I-V, P-V Curve")
            graph.setLabel("left", "Current (A)")
            graph.setLabel("bottom", "Voltage (V)")
            graph.setLabel("right", "Power (W)")
            graph.showGrid(x=True, y=True)
            layout.addWidget(graph, 0, 0, 1, 1)

            self.graph_ui = {"display": display, "selectors": graph}
