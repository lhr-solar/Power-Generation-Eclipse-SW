"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      PV Capture Controller. 
@version    3.0.0
@date       2022-09-14
"""

from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QTextEdit,
    QHBoxLayout,
    QComboBox,
    QInputDialog,
    QFileDialog,
    QSizePolicy,
    QFormLayout,
    QFrame,
    QLineEdit,
)
from PyQt6.QtCore import Qt
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
import pyqtgraph as pg
from datetime import datetime

from src.pv_capture.pv_characterization import PVCharacterization
from src.modeling.pv_model import PVModel


class PVCaptureController:
    """_summary_
    The PV Capture Controller:
    - Is a graphical user interface
    - Interacts with the PV Curve Tracer PCB to run experiments
    - Loads historical PV test data and models
    - Characterizes PVs and generates I-V, P-V curves
    - Ranks and bins PVs against other cells or a theoretical model.
    """

    def __init__(self):
        self.pv_model = PVModel()
        self.pv_char = PVCharacterization()
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

    class Data:
        def __init__(self, parent):
            self.parent = parent
            self.test_data_instance = {"file_path": None, "loader": None, "data": None}
            self.curve_tracer_instance = {
                "loader": self.parent.pv_char.get_version_loader(
                    self.parent.pv_char.get_version()
                ),
                "com_port": None,
                "baud_rate": None,
                "pv_type": None,
                "pv_id": None,
                "data": None,
            }
            self.model_instance = {"pv_model": None, "data": None}

        def get_potential_pv_configs(self):
            # TODO: Load from pv_config.conf file.
            return {
                "CELL": {
                    "sample_range": [0.3, 0.45],
                    "step_size": 0.001,
                    "num_iters": 25,
                    "settling_time": 2,
                },
                "MODULE": {
                    "sample_range": [0.3, 0.45],
                    "step_size": 0.0001,
                    "num_iters": 25,
                    "settling_time": 2,
                },
                "ARRAY": {
                    "sample_range": [0.3, 0.45],
                    "step_size": 0.0001,
                    "num_iters": 25,
                    "settling_time": 2,
                },
            }

    class UI(QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            main_layout = QGridLayout()
            self.setLayout(main_layout)

            self.add_sublayout_pv_config()
            main_layout.addWidget(self.pv_config_ui["display"], 0, 0, 3, 3)

            comm_config_display = self.add_sublayout_comm_config()
            main_layout.addWidget(comm_config_display, 3, 0, 3, 3)

            id_display = self.add_sublayout_id()
            main_layout.addWidget(id_display, 6, 0, 1, 1)

            go_display = self.add_sublayout_go()
            main_layout.addWidget(go_display, 7, 0, 1, 1)

            char_board_display = self.add_sublayout_char_board()
            main_layout.addWidget(char_board_display, 0, 3, 4, 4)

            iv_display = self.add_sublayout_iv()
            main_layout.addWidget(iv_display, 4, 3, 4, 4)

        def add_sublayout_pv_config(self):
            display = QFrame()
            layout = QGridLayout()
            display.setLayout(layout)

            # Title Label
            title = QLabel("PV Config")
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
            selector_sample_range.setPlaceholderText("Format: '[x, y]' in range [0, 1]")
            selector_sample_range.editingFinished.connect(self.update_pv_config)
            layout_selectors.addRow(label_sample_range, selector_sample_range)

            # Step Size Selector
            label_step_size = QLabel("Step Size")
            selector_step_size = QLineEdit()
            selector_step_size.setPlaceholderText("Format: 'x' in range [0.001, 0.1]")
            selector_step_size.editingFinished.connect(self.update_pv_config)
            layout_selectors.addRow(label_step_size, selector_step_size)

            # Num Iterations
            label_num_iters = QLabel("Num Iterations")
            selector_num_iters = QLineEdit()
            selector_num_iters.setPlaceholderText("Format: 'x' > 0")
            selector_num_iters.editingFinished.connect(self.update_pv_config)
            layout_selectors.addRow(label_num_iters, selector_num_iters)

            # Settling Time Per Step
            label_settling_time = QLabel("Settling Time (ms)")
            selector_settling_time = QLineEdit()
            selector_settling_time.setPlaceholderText("Format: 'x' > 0")
            selector_settling_time.editingFinished.connect(self.update_pv_config)
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
            layout_labels.addRow(label_num_steps, val_num_steps)

            # Total Samples
            label_total_samples = QLabel("Total Samples")
            val_total_samples = QLineEdit()
            layout_labels.addRow(label_total_samples, val_total_samples)

            # Expected Test Duration (s)
            label_test_duration = QLabel("Test Duration (ms)")
            val_test_duration = QLineEdit()
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
                f"[{configs[config_name]['sample_range'][0]}:{configs[config_name]['sample_range'][1]}]"
            )
            self.pv_config_ui["selectors"]["sel_step_size"].setText(
                f"{configs[config_name]['step_size']}"
            )
            self.pv_config_ui["selectors"]["sel_num_iters"].setText(
                f"{configs[config_name]['num_iters']}"
            )
            self.pv_config_ui["selectors"]["sel_settle_time"].setText(
                f"{configs[config_name]['settling_time']}"
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

            title = QLabel("COMM Config")
            layout.addWidget(title, 0, 0, 1, 2)
            display.setLayout(layout)
            return display

        def add_sublayout_id(self):
            display = QFrame()
            layout = QGridLayout()

            title = QLabel("ID")
            layout.addWidget(title, 0, 0, 1, 2)
            display.setLayout(layout)
            return display

        def add_sublayout_go(self):
            display = QFrame()
            layout = QGridLayout()

            title = QLabel("GO")
            layout.addWidget(title, 0, 0, 1, 2)
            display.setLayout(layout)
            return display

        def add_sublayout_char_board(self):
            display = QFrame()
            layout = QGridLayout()

            title = QLabel("CHAR Board")
            layout.addWidget(title, 0, 0, 1, 2)
            display.setLayout(layout)
            return display

        def add_sublayout_iv(self):
            display = QFrame()
            layout = QGridLayout()

            title = QLabel("IV Display")
            layout.addWidget(title, 0, 0, 1, 2)
            display.setLayout(layout)
            return display
