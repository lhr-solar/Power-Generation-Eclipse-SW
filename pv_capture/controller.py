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

from pv_capture.pv_characterization import PVCharacterization


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
        self.ui.print_console(output)

    class Data:
        def __init__(self, parent):
            self.parent = parent
            self.test_data_instance = {"file_path": None, "loader": None, "data": None}
            self.curve_tracer_instance = {
                "loader": self.parent.pv_char.get_version_loader(self.parent.pv_char.get_version()),
                "com_port": None,
                "baud_rate": None,
                "pv_type": None,
                "pv_id": None,
                "data": None
            }
            self.model_instance = {
                "pv_model" : None
            }

        def go(self):
            """_summary_
            Loads in characterization data for the PV.

            Returns:
                [False, str]: An error and an error string
                [True, dict]: A success and data corresponding to the characterized PV in the form:
                    {
                        "irradiance": float,
                        "temperature": float,
                        "voltage":  [float],
                        "current":  [float],
                        "power":    [float],
                        "v_oc":     float,
                        "i_sc":     float,
                        "v_mpp":    float,
                        "i_mpp":    float,
                        "p_mpp":    float,
                        "ff":       float,
                        "eff":      float
                    }
            """
            # Pressing the GO button.
            if (
                self.test_data_instance["file_path"] is not None
                and self.test_data_instance["loader"] is not None
                and self.test_data_instance["data"] is not None
            ):
                self.parent.print("LOG", "Characterizing data...")

                # Calculate characteristics
                data = self.parent.pv_char.characterize_data(
                    self.test_data_instance["data"]
                )
                return [True, data]

            elif (
                self.curve_tracer_instance["com_port"] is not None
                and self.curve_tracer_instance["baud_rate"] is not None
                and self.curve_tracer_instance["pv_type"] is not None
                and self.curve_tracer_instance["pv_id"] is not None
            ):
                self.parent.print("LOG", "Communicating with PV Curve Tracer...")
                # Open serial port
                # Send command
                # Wait for data to be transmitted
                # Load I-V, P-V Curve data
                # Calculate characteristics
                # Save into file
                # Return stuff
                return [False, "UNIMPLEMENTED"]
            else:
                return [False, "Nothing can be run."]

        def reset(self):
            """_summary_
            Resets characterization data for the PV.

            Returns:
                dict: An empty data dict corresponding to a nonexistent PV in the same format as go.
            """
            self.test_data_instance = {"file_path": None, "loader": None, "data": None}
            self.curve_tracer_instance = {
                "com_port": None,
                "baud_rate": None,
                "pv_type": None,
                "pv_id": None,
            }

            return {
                "irradiance": 0.00,
                "temperature": 0.00,
                "voltage": [],
                "current": [],
                "power": [],
                "v_oc": 0.00,
                "i_sc": 0.00,
                "v_mpp": 0.00,
                "i_mpp": 0.00,
                "p_mpp": 0.00,
                "ff": 0.00,
                "eff": 0.00
            }

        def get_available_com_ports(self):
            """_summary_
            Returns a list of currently connected COM ports.

            Returns:
                [str]: Port Names.
            """
            port_options = ["-"]
            ports = QSerialPortInfo().availablePorts()
            if len(ports) != 0:
                port_options.extend([port.portName() for port in ports])
            return port_options

        def set_com_port(self, com_port):
            """_summary_
            Sets the current COM port of the device.

            Args:
                com_port (str): The com port to set.
            """
            self.curve_tracer_instance["com_port"] = com_port

        def get_available_baud_rates(self):
            """_summary_
            Returns a list of baud rates for talking to the device.

            Returns:
                [str]: Baud rates.
            """
            baud_options = ["-"]
            bauds = QSerialPortInfo().standardBaudRates()
            baud_options.extend([str(baud) for baud in bauds])
            return baud_options

        def set_baud_rate(self, baud_rate):
            """_summary_
            Sets the current baud rate of the device.

            Args:
                baud_rate (str): The baud rate to set.
            """
            self.curve_tracer_instance["baud_rate"] = baud_rate

        def get_available_pv_types(self):
            """_summary_
            Returns a list of PV types that the device could measure.

            Returns:
                [str]: List of PV types
            """
            return ["Cell", "Module", "Array"]

        def set_pv_type(self, pv_type):
            """_summary_
            Sets the current PV type that the device is measuring.

            Args:
                pv_type (str): The PV type to measure.
            """
            self.curve_tracer_instance["pv_type"] = pv_type

        def set_pv_id(self, id):
            """_summary_
            Sets the ID representing the PV to be tested. This is used later for
            generating a characterization file.

            Args:
                id (str): ID of the PV tested.

            Returns:
                bool: Whether the ID is valid. It could fail based on the following reasons:
                - The file already exists.
                - The name has spaces in it.
            """
            self.curve_tracer_instance["pv_id"] = id
            # Check if a file under this name already exists.
            return True

        def load_pv_char_file(self, file_path):
            """_summary_
            Load a historical PV characterization file. Select the
            correct loader associated with the file version and load in the file contents.

            Args:
                file_path (str): File to load.
            """
            self.parent.print("LOG", f"Loading PV characterization file at {file_path}...")
            [result, loader_or_err] = self.parent.pv_char.get_version_loader(file_path)

            if result is False:
                self.parent.print("ERROR", loader_or_err)
            else:
                self.test_data_instance["file_path"] = file_path
                self.test_data_instance["loader"] = loader_or_err
                self.parent.print(
                    "LOG", "Found valid loader version, extracting file..."
                )
                self.test_data_instance["data"] = loader_or_err.load_file(file_path)
                self.parent.print("LOG", "Loaded in data.")

        def save_pv_char_file(self):
            """_summary_
            Save a PV characterization into a file.
            """
            self.curve_tracer_instance["loader"].store_file(
                f"./data/{self.curve_tracer_instance['pv_id']}.log",
                self.curve_tracer_instance["data"]
            )

        def get_available_pv_models(self):
            """_summary_
            Returns a list of PV models that can be compared against the PV
            characterization data.

            Returns:
                [str]: List of PV models.
            """
            return ["Nonideal PV Cell Model", "Ideal PV Cell Model"]

        def set_pv_model(self, pv_model):
            """_summary_
            Sets the current PV model to be compared against the PV
            characterization data.

            Args:
                pv_model (str): Model name.
            """
            self.model_instance["pv_model"] = pv_model

        def normalize_data(self, data):
            """_summary_
            Normalize the PV data to 25 C and 1000 W/m^2.

            Args:
                data Data to normalize.

            Returns:
                dict: data corresponding to the characterized PV in the form:
                    {
                        "irradiance": float,
                        "temperature": float,
                        "voltage":  [float],
                        "current":  [float],
                        "power":    [float],
                        "v_oc":     float,
                        "i_sc":     float,
                        "v_mpp":    float,
                        "i_mpp":    float,
                        "p_mpp":    float,
                        "ff":       float,
                        "eff":      float
                    }
            """

            return self.parent.pv_char.normalize_data(data)

            # Normalize to 25C and 1000 W/m^2 (G)
            data = {
                "irradiance": 0.00,
                "temperature": 0.00,
                "voltage": [],
                "current": [],
                "power": [],
                "v_oc": 0.00,
                "i_sc": 0.00,
                "v_mpp": 0.00,
                "i_mpp": 0.00,
                "p_mpp": 0.00,
                "ff": 0.00,
                "eff": 0.00
            }
            return data

        def superimpose_model(self):
            # Return the data series to plot onto the graph.
            data = {"series_voltage": [], "series_current": [], "series_power": []}
            return data

        # Analyze Data Against Others
        def set_test_data_file_range(self, range):
            # Check to see if some subset of files exist under the range specifier
            self.data_set = None
            return False

        def get_analysis(self, test_data):
            # Return several things:
            #    - A headline number indicating the percentile of the cell
            #      to the set. This may be calculated arbitrarily.
            #    - A Fill Factor distribution [bin_size in %, [array of a PMF],
            #      index our PV data is associated with].
            #    - A P_MPP distribution [bin_size in mW, [array of a PMF],
            #      index our PV data is associated with].
            #    - I-V curve set (ordered array for each PV in the test set,
            #      against the test_data).
            return None

        def publish_pv_models(self, pv_model_selector):
            pass
            # print(self.parent.ui)#update_pv_model_selector(pv_model_selector, self.get_available_pv_models())

    class UI(QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            main_layout = QGridLayout()
            self.setLayout(main_layout)

            [
                widget_new_pv,
                [
                    com_port_selector,
                    baud_rate_selector,
                    pv_type_selector,
                    self.id_input,
                ],
            ] = self.add_sublayout_pull_data()
            main_layout.addWidget(widget_new_pv, 0, 0, 16, 34)

            [widget_load_pv] = self.add_sublayout_load_data()
            main_layout.addWidget(widget_load_pv, 0, 34, 16, 16)

            [
                widget_char_pv,
                [self.v_oc, self.i_sc, self.v_mpp, self.i_mpp, self.p_mpp, self.ff],
            ] = self.add_sublayout_char_data()
            main_layout.addWidget(widget_char_pv, 16, 0, 16, 50)

            [widget_compare_pv, [pv_model_selector]] = self.add_sublayout_compare_pv()
            main_layout.addWidget(widget_compare_pv, 32, 0, 10, 50)

            [
                widget_analyze_pv,
                [self.name_range_specifier, self.percentile_display],
            ] = self.add_sublayout_analyze_pv()
            main_layout.addWidget(widget_analyze_pv, 42, 0, 10, 50)

            [widget_console, [self.console]] = self.add_sublayout_console()
            main_layout.addWidget(widget_console, 52, 0, 12, 50)

            [
                widget_display,
                [self.iv_curve, self.ff_dist, self.pmpp_dist, self.iv_curve_ranked],
            ] = self.add_sublayout_graphs()
            main_layout.addWidget(widget_display, 0, 50, 64, 70)

            self.load_selector(
                com_port_selector, self.parent.data.get_available_com_ports()
            )
            self.load_selector(
                baud_rate_selector, self.parent.data.get_available_baud_rates()
            )
            self.load_selector(
                pv_type_selector, self.parent.data.get_available_pv_types()
            )
            self.load_selector(
                pv_model_selector, self.parent.data.get_available_pv_models()
            )

        # Layout setup functions
        def add_sublayout_pull_data(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Pull Data From Curve Tracer")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout_com_port = QFormLayout()
            com_port_label = QLabel("COM Port")
            com_port_selector = QComboBox()
            com_port_selector.addItem("NULL")
            layout_com_port.addRow(com_port_label, com_port_selector)

            layout_baud_rate = QFormLayout()
            baud_rate_label = QLabel("Baud Rate")
            baud_rate_selector = QComboBox()
            layout_baud_rate.addRow(baud_rate_label, baud_rate_selector)

            layout_pv_type = QFormLayout()
            pv_type_label = QLabel("PV Type")
            pv_type_selector = QComboBox()
            layout_pv_type.addRow(pv_type_label, pv_type_selector)

            layout_id = QFormLayout()
            id_label = QLabel("PV ID")
            id_input = QLineEdit()
            id_input.setPlaceholderText("cell_rp001")
            layout_id.addRow(id_label, id_input)
            # TODO: 09_15_2022 Deal with validator, verify cell exists.

            layout_display.addWidget(title, 0, 0, 1, 2)
            layout_display.addLayout(layout_com_port, 1, 0, 1, 1)
            layout_display.addLayout(layout_baud_rate, 2, 0, 1, 1)
            layout_display.addLayout(layout_pv_type, 1, 1, 1, 1)
            layout_display.addLayout(layout_id, 2, 1, 1, 1)

            display.setLayout(layout_display)

            return [
                display,
                [com_port_selector, baud_rate_selector, pv_type_selector, id_input],
            ]

        def add_sublayout_load_data(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Load Test Data From File")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            file_selector = QPushButton("Select PV Log File")
            file_selector.clicked.connect(self.get_test_data_file_from_dialog)

            layout_display.addWidget(title, 0, 0, 1, 1)
            layout_display.addWidget(file_selector, 1, 0, 2, 1)

            display.setLayout(layout_display)

            return [display]

        def add_sublayout_char_data(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Characterize Data")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            v_oc = QLabel("V_OC = 0.00V")
            v_oc.setAlignment(Qt.AlignmentFlag.AlignCenter)

            i_sc = QLabel("I_SC = 0.00A")
            i_sc.setAlignment(Qt.AlignmentFlag.AlignCenter)

            v_mpp = QLabel("V_MPP = 0.00V")
            v_mpp.setAlignment(Qt.AlignmentFlag.AlignCenter)

            i_mpp = QLabel("I_MPP = 0.00A")
            i_mpp.setAlignment(Qt.AlignmentFlag.AlignCenter)

            p_mpp = QLabel("P_MPP = 0.00W")
            p_mpp.setAlignment(Qt.AlignmentFlag.AlignCenter)

            ff = QLabel("FF = 0.00%")
            ff.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout_display.addWidget(title, 0, 0, 1, 3)
            layout_display.addWidget(v_oc, 1, 0, 1, 1)
            layout_display.addWidget(i_sc, 2, 0, 1, 1)
            layout_display.addWidget(v_mpp, 1, 1, 1, 1)
            layout_display.addWidget(i_mpp, 2, 1, 1, 1)
            layout_display.addWidget(p_mpp, 1, 2, 1, 1)
            layout_display.addWidget(ff, 2, 2, 1, 1)

            display.setLayout(layout_display)

            return [display, [v_oc, i_sc, v_mpp, i_mpp, p_mpp, ff]]

        def add_sublayout_compare_pv(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Compare Against Model")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout_pv_model = QFormLayout()
            pv_model_label = QLabel("PV Model Type")
            pv_model_selector = QComboBox()
            layout_pv_model.addRow(pv_model_label, pv_model_selector)

            normalize_iv_curve_button = QPushButton(
                "Normalize irradiance and temperature"
            )
            normalize_iv_curve_button.clicked.connect(self.normalize_data)
            superimpose_iv_curve_button = QPushButton("Superimpose on Curve")
            superimpose_iv_curve_button.clicked.connect(self.superimpose_model)

            layout_display.addWidget(title, 0, 0, 1, 3)
            layout_display.addLayout(layout_pv_model, 1, 0, 1, 1)
            layout_display.addWidget(normalize_iv_curve_button, 1, 1, 1, 1)
            layout_display.addWidget(superimpose_iv_curve_button, 1, 2, 1, 1)

            display.setLayout(layout_display)

            return [display, [pv_model_selector]]

        def add_sublayout_analyze_pv(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Analyze Data Against Others")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout_name_range = QFormLayout()
            name_range_label = QLabel("PV Range")
            name_range_specifier = QLineEdit()
            layout_name_range.addRow(name_range_label, name_range_specifier)
            name_range_label.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            name_range_specifier.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            percentile_display = QLabel("Top 0.00% Percentile")
            percentile_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
            percentile_display.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            display_dist_button = QPushButton("Display Distribution")
            display_dist_button.clicked.connect(self.set_ranking_display)
            display_dist_button.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            layout_display.addWidget(title, 0, 0, 1, 3)
            layout_display.addLayout(layout_name_range, 1, 0, 1, 1)
            layout_display.addWidget(percentile_display, 1, 1, 1, 1)
            layout_display.addWidget(display_dist_button, 1, 2, 1, 1)

            display.setLayout(layout_display)

            return [display, [name_range_specifier, percentile_display]]

        def add_sublayout_console(self):
            display = QFrame()
            layout_display = QGridLayout()

            # Left widget is the status console
            status_console = QTextEdit()
            status_console.setReadOnly(True)

            # Right widget is a pair of buttons, GO and RESET
            go_button = QPushButton("GO")
            go_button.setStyleSheet("background-color: green")
            go_button.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            go_button.clicked.connect(self.generate_data)

            reset_button = QPushButton("RESET")
            reset_button.setStyleSheet("background-color: red")
            reset_button.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            reset_button.clicked.connect(self.reset_data)

            layout_display.addWidget(status_console, 0, 0, 2, 8)
            layout_display.addWidget(go_button, 0, 8, 1, 3)
            layout_display.addWidget(reset_button, 1, 8, 1, 3)

            display.setLayout(layout_display)

            return [display, [status_console]]

        def set_ranking_display(self):
            self.display.setCurrentIndex(1)

        def add_sublayout_graphs(self):
            display = QFrame()
            layout_display = QStackedLayout()

            # Top page is graph_iv_curve
            top_display, [iv_curve] = self.add_subwindow_graph_iv_curve()

            # Next page is a gridlayout of other graphs
            bottom_display, [
                ff_dist,
                pmpp_dist,
                iv_curve_ranked,
            ] = self.add_subwindow_graph_ranking()

            layout_display.addWidget(top_display)
            layout_display.addWidget(bottom_display)

            display.setLayout(layout_display)

            return [display, [iv_curve, ff_dist, pmpp_dist, iv_curve_ranked]]

        def add_subwindow_graph_iv_curve(self):
            # Wrap the widget around the layout which holds the plot widget :)
            parent_widget = QWidget()
            layout = QVBoxLayout()
            iv_curve = pg.PlotWidget()
            iv_curve.setTitle("I-V Characteristics")
            iv_curve.setLabel("left", "Current (A)")
            iv_curve.setLabel("bottom", "Voltage (V)")
            iv_curve.setLabel("right", "Power (W)")
            iv_curve.showGrid(x=True, y=True)
            layout.addWidget(iv_curve)
            parent_widget.setLayout(layout)
            return [parent_widget, [iv_curve]]

        def add_subwindow_graph_ranking(self):
            # Wrap the widget around the layout which holds the plot widgets :)
            parent_widget = QWidget()
            layout = QGridLayout()
            ff_dist = pg.PlotWidget()
            pmpp_dist = pg.PlotWidget()
            iv_curve = pg.PlotWidget()
            layout.addWidget(ff_dist, 0, 0, 1, 1)
            layout.addWidget(pmpp_dist, 0, 1, 1, 1)
            layout.addWidget(iv_curve, 1, 0, 1, 2)
            parent_widget.setLayout(layout)
            return [parent_widget, [ff_dist, pmpp_dist, iv_curve]]

        # Generic functions
        def load_selector(self, selector_widget, items):
            selector_widget.clear()
            for item in items:
                selector_widget.addItem(item)

        def get_selector_value(self, selector_widget):
            return selector_widget.currentText()

        def populate_field(self, widget, text):
            widget.setText(text)

        def print_console(self, text):
            self.console.append(text)

        # Button specific functions
        def get_test_data_file_from_dialog(self):
            file_path = QFileDialog.getOpenFileName(self, "Open File:", "./", "")
            self.parent.data.load_pv_char_file(file_path[0])

        def normalize_data(self):
            pass

        def superimpose_model(self):
            pass

        def generate_data(self):
            # Run data generation function
            self.parent.print("LOG", "Starting Eclipse PV Capture execution...")
            [success, data] = self.parent.data.go()
            if success:
                self.parent.print("LOG", "Plotting data on main canvas...")
                self.plot_graph_iv_curve(data)
                self.parent.print("LOG", "Updating labels...")
                self.update_char_data_fields(data)
                self.parent.print("LOG", "Done!")

        def update_char_data_fields(self, data):
            self.populate_field(self.v_oc, f"V_OC = {data['v_oc']:.2f} V")
            self.populate_field(self.i_sc, f"I_SC = {data['i_sc']:.2f} A")
            self.populate_field(self.v_mpp, f"V_MPP = {data['v_mpp']:.2f} V")
            self.populate_field(self.i_mpp, f"I_MPP = {data['i_mpp']:.2f} A")
            self.populate_field(self.p_mpp, f"P_MPP = {data['p_mpp']:.2f} W")
            self.populate_field(self.ff, f"FF = {data['ff']*100:.2f} %")

        def plot_graph_iv_curve(self, data):
            self.iv_curve.plot(data["voltage"], data["current"])
            self.iv_curve.plot(data["voltage"], data["power"])

        def reset_data(self):
            pass
