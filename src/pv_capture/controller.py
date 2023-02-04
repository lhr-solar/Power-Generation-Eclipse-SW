"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com) and Roy Mor (roymor.102@gmail.com)
@brief      PV Capture Controller. 
@version    3.1.0
@date       2023-02-04
"""

import os
import re
import time
import traceback
from datetime import datetime

import pyqtgraph as pg
from PyQt6.QtCore import (
    QObject,
    QRunnable,
    Qt,
    QThread,
    QThreadPool,
    QTimer,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtGui import QDoubleValidator, QIntValidator, QColor
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
            self.com_config = {
                "valid": False,
                "com_port": None,
                "baud_rate": None,
                "parity_bit": None,
                "enc_scheme": None,
            }
            self.pv_config = {
                "valid": False,
                "sample_range": None,
                "step_size": None,
                "num_iters": None,
                "settling_time": None,
                "pv_type": None,
                "num_steps_per_iter": None,
                "total_samples": None,
                "test_duration_ms": None,
            }
            self.pv_id = {"valid": False, "id": None}
            self.log_data = {
                "gate": [],
                "voltage": [],
                "current": [],
            }
            # self.char_data = {
            #     "v_oc": None,
            #     "c_sc": None,
            #     "v_mpp": None,
            #     "c_mpp": None,
            #     "p_mpp": None
            # }
            self.power_data = {
                "power": []
            }
        def validate_com_config(self, com_port, baud_rate, parity_bit, encoding_scheme):
            if com_port not in self.parent.curve_tracer.list_ports():
                self.com_config["valid"] = False
            elif baud_rate not in self.parent.curve_tracer.list_baud_rates():
                self.com_config["valid"] = False
            elif parity_bit not in self.parent.curve_tracer.list_parity():
                self.com_config["valid"] = False
            elif (
                encoding_scheme not in self.parent.curve_tracer.list_encoding_schemes()
            ):
                self.com_config["valid"] = False
            else:
                self.com_config["com_port"] = com_port
                self.com_config["baud_rate"] = baud_rate
                self.com_config["parity_bit"] = parity_bit
                self.com_config["enc_scheme"] = encoding_scheme

                self.com_config["valid"] = True
            return self.com_config

        def validate_pv_config(
            self, sample_range, step_size, num_iters, settling_time, pv_type
        ):
            if (
                (sample_range[0] < 0)
                or (sample_range[1] > 1)
                or (sample_range[1] <= sample_range[0])
            ):
                self.com_config["valid"] = False
            elif step_size < 0.001 or step_size > 0.100:
                self.com_config["valid"] = False
            elif num_iters < 1 or num_iters > 100:
                self.com_config["valid"] = False
            elif settling_time < 1 or settling_time > 100:
                self.com_config["valid"] = False
            else:
                self.pv_config["sample_range"] = sample_range
                self.pv_config["step_size"] = step_size
                self.pv_config["num_iters"] = num_iters
                self.pv_config["settling_time"] = settling_time
                self.pv_config["pv_type"] = pv_type

                num_steps_per_iter = int(
                    (sample_range[1] - sample_range[0]) / step_size
                )
                self.pv_config["num_steps_per_iter"] = num_steps_per_iter
                total_samples = int(num_steps_per_iter * num_iters)
                self.pv_config["total_samples"] = total_samples
                self.pv_config["test_duration_ms"] = int(total_samples * settling_time)

                self.pv_config["valid"] = True
            return self.pv_config

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

        def validate_pv_id(self, pv_id):
            if pv_id == "":
                self.pv_id["valid"] = False
                self.parent.print("ERROR", "No ID is specified.")
                return self.pv_id

            # Check if file exists in ./data/captures
            files = self.parent.curve_tracer.list_capture_files()
            files = [file.split(".")[0] for file in files]
            self.pv_id["valid"] = True
            self.pv_id["id"] = pv_id
            if pv_id in files:
                self.parent.print(
                    "WARN", f"ID {pv_id} already in use. Overwrite at your risk."
                )
            else:
                self.parent.print(
                    "LOG", f"Output will be written to data/captures/{pv_id}.capture."
                )

            return self.pv_id

    class UI(QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            main_layout = QGridLayout()
            self.setLayout(main_layout)

            self.add_sublayout_pv_config()
            main_layout.addWidget(self.pv_config_ui["display"], 0, 0, 3, 4)

            self.add_sublayout_com_config()
            main_layout.addWidget(self.com_config_ui["display"], 3, 0, 3, 3)

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
            except Exception as e:
                self.parent.print("ERROR", "Sample range error: {0}".format(e))
                return

            # Update config
            config = self.parent.data.validate_pv_config(
                sample_range,
                float(self.pv_config_ui["selectors"]["sel_step_size"].text()),
                int(self.pv_config_ui["selectors"]["sel_num_iters"].text()),
                int(self.pv_config_ui["selectors"]["sel_settle_time"].text()),
                self.pv_config_ui["selectors"]["sel_pv_type"].currentText(),
            )

            # Update UI for labels.
            if config["valid"]:
                self.pv_config_ui["labels"]["lab_num_steps"].setText(
                    str(config["num_steps_per_iter"])
                )
                self.pv_config_ui["labels"]["lab_tot_steps"].setText(
                    str(config["total_samples"])
                )
                self.pv_config_ui["labels"]["lab_test_dur"].setText(
                    str(config["test_duration_ms"])
                )
            else:
                self.pv_config_ui["labels"]["lab_num_steps"].setText("INV")
                self.pv_config_ui["labels"]["lab_tot_steps"].setText("INV")
                self.pv_config_ui["labels"]["lab_test_dur"].setText("INV")

        def add_sublayout_com_config(self):
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
            selector_com_port.currentIndexChanged.connect(self.update_com_config)
            layout_selectors.addRow(label_com_port, selector_com_port)

            # Baud Rate Selector
            label_baud_rate = QLabel("Baud Rate")
            selector_baud_rate = QComboBox()
            selector_baud_rate.addItems(
                [str(item) for item in self.parent.curve_tracer.list_baud_rates()]
            )
            selector_baud_rate.currentIndexChanged.connect(self.update_com_config)
            layout_selectors.addRow(label_baud_rate, selector_baud_rate)

            # Parity Bit Selector
            label_parity_bit = QLabel("Parity Bit")
            selector_parity_bit = QComboBox()
            selector_parity_bit.addItems(self.parent.curve_tracer.list_parity())
            selector_parity_bit.currentIndexChanged.connect(self.update_com_config)
            layout_selectors.addRow(label_parity_bit, selector_parity_bit)

            # Encoding Scheme Selector
            label_encoding_scheme = QLabel("Encoding Scheme")
            selector_encoding_scheme = QComboBox()
            selector_encoding_scheme.addItems(
                self.parent.curve_tracer.list_encoding_schemes()
            )
            selector_encoding_scheme.currentIndexChanged.connect(self.update_com_config)
            layout_selectors.addRow(label_encoding_scheme, selector_encoding_scheme)

            # Setup timer to update com config.
            # TODO: re-enable when this doesn't break config.
            timer = QTimer()
            timer.timeout.connect(self.update_com_combo)
            timer.setInterval(1000)
            timer.start()

            self.com_config_ui = {
                "display": display,
                "selectors": {
                    "sel_config_file": selector_com_config,
                    "sel_com_port": selector_com_port,
                    "sel_baud_rate": selector_baud_rate,
                    "sel_parity_bit": selector_parity_bit,
                    "sel_enc_scheme": selector_encoding_scheme,
                },
                "timer": None,  # timer
            }

            # Default setup com config.
            self.update_com_config()

        def update_com_combo(self):
            # TODO: handle the case where an active port is already selected. Do
            # not modify this port.
            com_ports = self.com_config_ui["selectors"]["sel_com_port"]
            com_ports.blockSignals(True)
            com_ports.clear()
            com_ports.addItems(self.parent.curve_tracer.list_ports())
            com_ports.blockSignals(False)

        def update_com_config(self):
            config = self.parent.data.validate_com_config(
                self.com_config_ui["selectors"]["sel_com_port"].currentText(),
                int(self.com_config_ui["selectors"]["sel_baud_rate"].currentText()),
                self.com_config_ui["selectors"]["sel_parity_bit"].currentText(),
                self.com_config_ui["selectors"]["sel_enc_scheme"].currentText(),
            )

        def select_com_config_file(self):
            file_path = QFileDialog.getOpenFileName(self, "Open File:", "./", "")
            config = self.parent.curve_tracer.load_com_config(file_path)
            self.com_config_ui["selectors"]["sel_com_port"].setCurrentText(
                config["com_port"]
            )
            self.com_config_ui["selectors"]["sel_baud_rate"].setCurrentText(
                str(config["baud_rate"])
            )
            self.com_config_ui["selectors"]["sel_parity_bit"].setCurrentText(
                config["parity_bit"]
            )
            self.com_config_ui["selectors"]["sel_enc_scheme"].setCurrentText(
                config["enc_scheme"]
            )

            self.update_com_config()

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
            selector_id.editingFinished.connect(self.update_pv_id)
            selector_id.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
            )
            selector_id.setPlaceholderText("ex. BV001")
            layout.addWidget(selector_id, 1, 0, 1, 1)

            self.id_ui = {"display": display, "selectors": selector_id}

        def update_pv_id(self):
            config = self.parent.data.validate_pv_id(self.id_ui["selectors"].text())
            if config["valid"]:
                self.id_ui["selectors"].setStyleSheet("background-color: #00FF00;")
            else:
                self.id_ui["selectors"].setStyleSheet("background-color: #FF0000;")

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
            selector_start.clicked.connect(self.start_cap)
            layout.addWidget(selector_start, 1, 0, 1, 1)

            # Stop Button
            selector_stop = QPushButton("STOP")
            selector_stop.setStyleSheet("background-color: #FF0000;")
            selector_stop.clicked.connect(self.stop_cap)
            layout.addWidget(selector_stop, 2, 0, 1, 1)

            self.control_ui = {
                "display": display,
                "selectors": {
                    "sel_start": selector_start,
                    "sel_stop": selector_stop,
                },
            }

        class CaptureTask(QRunnable):
            def __init__(self, parent, *args, **kwargs):
                super().__init__()
                self.args = args
                self.parent = parent
                self.kwargs = kwargs
                self.signals = self.CaptureSignals()

            @pyqtSlot()
            def run(self):
                self.signals.log.emit(("LOG", "Starting Capture Task."))
                self.capture_data = self.args[0].capture(
                            self.args[1],
                            self.args[2],
                            self.signals.res,
                            self.signals.log,
                            self.signals.progress,
                            self.signals.finished,
                        )
                self.args[0].save_capture_file(self.args[2], self.capture_data, self.args[3])
                #self.parent.parent.data.log_data = self.capture_data


            class CaptureSignals(QObject):
                finished = pyqtSignal()
                log = pyqtSignal(tuple)
                res = pyqtSignal(list)
                progress = pyqtSignal(int)

        def update_capture(self, dataList):
            # Feed data back to parent.data
            # Update graphs
            # Generate characteristic data, update table
            
            # valueCheck = f"{dataList[0]} {dataList[1]} {dataList[2]}\n"
            # print(valueCheck)
            
            self.parent.data.log_data["gate"].append(dataList[0])
            self.parent.data.log_data["voltage"].append(dataList[1])
            self.parent.data.log_data["current"].append(dataList[2])

            self.parent.data.power_data["power"].append(dataList[1]*dataList[2])

            self.graph_ui["ivscatter"].setData(self.parent.data.log_data["voltage"], self.parent.data.log_data["current"])
            self.graph_ui["pvscatter"].setData(self.parent.data.log_data["voltage"], self.parent.data.power_data["power"])

        def update_pv_char(self):
            # TODO: Calculate Voc and Isc to add to characteristics
            # TODO: Calculate MPP and Vmpp/Impp
            # TODO: Calculate FF%
            # Send all of the above to their respective LineEdits

            mppIndex = 0
            for i, power in enumerate(self.parent.data.power_data['power']):
                if power>self.parent.data.power_data['power'][mppIndex]:
                    mppIndex = i
            self.char_board_ui["labels"]["lab_v_mpp"].setText(str(self.parent.data.log_data["voltage"][mppIndex]))
            self.char_board_ui["labels"]["lab_i_mpp"].setText(str(self.parent.data.log_data["current"][mppIndex]))
            self.char_board_ui["labels"]["lab_p_mpp"].setText("{:.3f}".format(self.parent.data.power_data["power"][mppIndex]))
            
            volCount = 0
            volSum = 0.0
            for i, vol, in enumerate(self.parent.data.log_data["voltage"]):
                if self.parent.data.log_data["current"][i]<.1:
                    volCount+=1
                    volSum+=vol
            self.char_board_ui["labels"]["lab_v_oc"].setText("{:.3f}".format(volSum/volCount))
            
            iCount = 0
            iSum = 0.0
            for i, current, in enumerate(self.parent.data.log_data["current"]):
                if self.parent.data.log_data["voltage"][i]<.1:
                    iCount+=1
                    iSum+=current
            self.char_board_ui["labels"]["lab_i_sc"].setText("{:.3f}".format(iSum/iCount))

            # FF = (Impp*Vmpp)/(Isc*Voc)
            fillFactor = (self.parent.data.log_data["current"][mppIndex]*self.parent.data.log_data["voltage"][mppIndex])/((volSum/volCount)*(iSum/iCount))
            self.char_board_ui["labels"]["lab_ff"].setText("{:.1f}".format(fillFactor*100))
                

        def start_cap(self):
            self.parent.print("LOG", "Starting characterization.")

            # Gather all the UI parts.
            print(self.parent.data.com_config)

            if not self.parent.data.com_config["valid"]:
                self.parent.print("ERROR", "COM config invalid.")
                return
            if not self.parent.data.pv_config["valid"]:
                self.parent.print("ERROR", "PV config invalid.")
                return
            if not self.parent.data.pv_id["valid"]:
                self.parent.print("ERROR", "PV ID invalid.")
                return

            try:
                worker = self.CaptureTask(
                    self,
                    self.parent.curve_tracer,
                    self.parent.data.com_config,
                    self.parent.data.pv_config,
                    self.parent.data.pv_id,
                )

                # Tie the progress signal to a progress bar, if any.
                # worker.signals.progress.connect(self.update_progress_bar)

                # Tie the log signal to the console.
                worker.signals.log.connect(
                    lambda log: self.parent.print(log[0], log[1])
                )

                # Tie the inter_res and result signals to updating the
                # graphs and characteristics.
                worker.signals.res.connect(self.update_capture)

                # Tie the finished signal to updating the console, updating the
                # graphs and characteristics.
                worker.signals.finished.connect(
                    lambda : self.parent.print("LOG", "Capture complete.")

                    # TODO: at end of characterization, increment pv_id. Notify
                    # this change.
                    # self.parent.print("LOG", f"Incremented PV_ID from {} to {}")
                )
                worker.signals.finished.connect(self.update_pv_char)

                QThreadPool().globalInstance().start(worker)


            except Exception as e:
                self.parent.print("ERROR", e)
                self.parent.print("LOG", "Halting characterization.")
            
            
            # def update_progress_bar(self, progress):
            #     pass

        def stop_cap(self):
            self.parent.print("LOG", "Stopping characterization.")
            # TODO: kill any running threads.

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

            IVCurve = pg.ScatterPlotItem(size = 7, brush=QColor(0,0,255))
            PVCurve = pg.ScatterPlotItem(size = 7, brush=QColor(255,0,0))
            graph.addItem(IVCurve)
            graph.addItem(PVCurve)

            layout.addWidget(graph, 0, 0, 1, 1)

            self.graph_ui = {"display": display, "selectors": graph, "ivscatter": IVCurve, "pvscatter": PVCurve}
