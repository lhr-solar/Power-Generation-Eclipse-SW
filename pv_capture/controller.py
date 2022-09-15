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
    QFileDialog
)
from PyQt6.QtCore import Qt
import pyqtgraph as pg


class PVCaptureController:
    def __init__(self):
        self.data = self.Data(self)
        self.ui = self.UI(self)

        # Update the UI with relevant setup data.

    def get_data(self):
        return [self.data, "PV Capture"]

    def get_ui(self):
        return [self.ui, "PV Capture"]

    class Data:
        def __init__(self, parent):
            self.parent = parent
            self.test_data_instance = {"file": None, "pv_type": None, "pv_id": None}
            self.curve_tracer_instance = {
                "com_port": None,
                "baud_rate": None,
                "pv_type": None,
                "pv_id": None,
            }

        def go(self):
            # Pressing the GO button.
            success = False
            data = {
                "error_str": "UNPOPULATED",
                "series_voltage": [],
                "series_current": [],
                "series_power": [],
                "v_oc": None,
                "i_sc": None,
                "v_mpp": None,
                "i_mpp": None,
                "p_mpp": None,
                "ff_pct": None,
            }

            if (
                self.test_data_instance["file"] is not None
                and self.test_data_instance["pv_type"] is not None
                and self.test_data_instance["pv_id"] is not None
            ):
                # Load I-V, P-V Curve data
                # Calculate characteristics
                # Return stuff
                pass
            elif (
                self.curve_tracer_instance["com_port"] is not None
                and self.curve_tracer_instance["baud_rate"] is not None
                and self.curve_tracer_instance["pv_type"] is not None
                and self.curve_tracer_instance["pv_id"] is not None
            ):
                # Open serial port
                # Send command
                # Wait for data to be transmitted
                # Load I-V, P-V Curve data
                # Calculate characteristics
                # Save into file
                # Return stuff
                pass

            return [success, data]

        def reset(self):
            self.test_data_instance = {"file": None, "pv_type": None, "pv_id": None}
            self.curve_tracer_instance = {
                "com_port": None,
                "baud_rate": None,
                "pv_type": None,
                "pv_id": None,
            }

            data = {
                "error_str": "UNPOPULATED",
                "series_voltage": [],
                "series_current": [],
                "series_power": [],
                "v_oc": 0.00,
                "i_sc": 0.00,
                "v_mpp": 0.00,
                "i_mpp": 0.00,
                "p_mpp": 0.00,
                "ff_pct": 0.00,
            }
            return data

        # Pull Data From Curve Tracer
        def get_available_com_ports(self):
            # use pyserial to get available ports.
            return []

        def set_com_port(self, com_port):
            self.curve_tracer_instance.com_port
            pass

        def get_available_baud_rates(self):
            return []

        def set_baud_rate(self, baud_rate):
            pass

        def get_available_pv_types(self):
            return []

        def set_pv_type(self, pv_type):
            pass

        def set_pv_id(self, id):
            # Check if a file under this name already exists.
            return False

        # Load Test Data From File
        def set_test_data_file(self, file_path):
            # Check to see if file exists.
            return False

        # Compare Against Model
        def get_available_pv_models(self):
            return ["Nonideal Model", "Ideal Model"]

        def set_pv_model(self, pv_model):
            pass

        def publish_pv_models(self, pv_model_selector):
            pass
            # print(self.parent.ui)#update_pv_model_selector(pv_model_selector, self.get_available_pv_models())

        def normalize_data(self, series_voltage, series_current):
            # Normalize to 25C and 1000 W/m^2 (G)
            data = {
                "error_str": "UNPOPULATED",
                "series_voltage": [],
                "series_current": [],
                "series_power": [],
                "v_oc": None,
                "i_sc": None,
                "v_mpp": None,
                "i_mpp": None,
                "p_mpp": None,
                "ff_pct": None,
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

    class UI(QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            main_layout = QGridLayout()
            self.setLayout(main_layout)

            sublayout_new_pv = self.add_sublayout_pull_data()
            main_layout.addLayout(sublayout_new_pv, 0, 0, 16, 34)

            sublayout_load_pv = self.add_sublayout_load_data()
            main_layout.addLayout(sublayout_load_pv, 0, 34, 16, 16)

            sublayout_char_pv = self.add_sublayout_char_data()
            main_layout.addLayout(sublayout_char_pv, 16, 0, 16, 50)

            sublayout_compare_pv = self.add_sublayout_compare_pv()
            main_layout.addLayout(sublayout_compare_pv, 32, 0, 10, 50)

            sublayout_analyze_pv = self.add_sublayout_analyze_pv()
            main_layout.addLayout(sublayout_analyze_pv, 42, 0, 10, 50)

            sublayout_console = self.add_sublayout_console()
            main_layout.addLayout(sublayout_console, 52, 0, 12, 50)

            [
                self.display,
                [iv_curve, ff_dist, pmpp_dist, iv_curve_ranked],
            ] = self.add_sublayout_graphs()
            main_layout.addLayout(self.display, 0, 50, 64, 70)

        def add_sublayout_pull_data(self):
            sublayout_display = QGridLayout()

            title = QLabel("Pull Data From Curve Tracer")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            com_port_selector = QComboBox()
            baud_rate_selector = QComboBox()
            pv_type_selector = QComboBox()
            id_input = QTextEdit()

            sublayout_display.addWidget(title, 0, 0, 1, 2)
            sublayout_display.addWidget(com_port_selector, 1, 0, 1, 1)
            sublayout_display.addWidget(baud_rate_selector, 2, 0, 1, 1)
            sublayout_display.addWidget(pv_type_selector, 1, 1, 1, 1)
            sublayout_display.addWidget(id_input, 2, 1, 1, 1)

            return sublayout_display

        def add_sublayout_load_data(self):
            sublayout_display = QGridLayout()

            title = QLabel("Load Test Data From File")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            file_selector = QPushButton("Select PV Log File")

            sublayout_display.addWidget(title, 0, 0, 1, 1)
            sublayout_display.addWidget(file_selector, 1, 0, 1, 1)

            return sublayout_display

        def add_sublayout_char_data(self):
            sublayout_display = QGridLayout()

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

            sublayout_display.addWidget(title, 0, 0, 1, 3)
            sublayout_display.addWidget(v_oc, 1, 0, 1, 1)
            sublayout_display.addWidget(i_sc, 2, 0, 1, 1)
            sublayout_display.addWidget(v_mpp, 1, 1, 1, 1)
            sublayout_display.addWidget(i_mpp, 2, 1, 1, 1)
            sublayout_display.addWidget(p_mpp, 1, 2, 1, 1)
            sublayout_display.addWidget(ff, 2, 2, 1, 1)

            return sublayout_display

        def add_sublayout_compare_pv(self):
            sublayout_display = QGridLayout()

            title = QLabel("Compare Against Model")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            pv_model_selector = QComboBox()
            normalize_iv_curve_button = QPushButton("Normalize irradiance and temperature.")
            superimpose_iv_curve_button = QPushButton("Superimpose on Curve")

            sublayout_display.addWidget(title, 0, 0, 1, 3)
            sublayout_display.addWidget(pv_model_selector, 1, 0, 1, 1)
            sublayout_display.addWidget(normalize_iv_curve_button, 1, 1, 1, 1)
            sublayout_display.addWidget(superimpose_iv_curve_button, 1, 2, 1, 1)

            return sublayout_display

        def add_sublayout_analyze_pv(self):
            sublayout_display = QGridLayout()

            title = QLabel("Analyze Data Against Others")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            name_range_specifier = QTextEdit("Hi")
            percentile_display = QLabel("0.00%")
            display_dist_button = QPushButton("Display Distribution")
            display_dist_button.clicked.connect(self.set_ranking_display)

            sublayout_display.addWidget(title, 0, 0, 1, 3)
            sublayout_display.addWidget(name_range_specifier, 1, 0, 1, 1)
            sublayout_display.addWidget(percentile_display, 1, 1, 1, 1)
            sublayout_display.addWidget(display_dist_button, 1, 2, 1, 1)

            return sublayout_display

        def set_ranking_display(self):
            self.display.setCurrentIndex(1)

        def add_sublayout_console(self):
            sublayout_console = QGridLayout()

            # Left widget is the status console
            status_console = QTextEdit()
            status_console.setText("Hello World!")
            status_console.setReadOnly(True)

            # Right widget is a pair of buttons, GO and RESET
            go_button = QPushButton("GO")
            go_button.setStyleSheet("background-color: green")
            go_button.clicked.connect(self.parent.data.go)
            reset_button = QPushButton("RESET")
            reset_button.setStyleSheet("background-color: red")
            reset_button.clicked.connect(self.parent.data.reset)

            sublayout_console.addWidget(status_console, 0, 0, 2, 8)
            sublayout_console.addWidget(go_button, 0, 8, 1, 3)
            sublayout_console.addWidget(reset_button, 1, 8, 1, 3)

            return sublayout_console

        def add_sublayout_graphs(self):
            # Stacked layout on right side of screen for the display
            sublayout_display = QStackedLayout()

            # Top page is graph_iv_curve
            top_display, [iv_curve] = self.add_subwindow_graph_iv_curve()

            # Next page is a gridlayout of other graphs
            bottom_display, [
                ff_dist,
                pmpp_dist,
                iv_curve_ranked,
            ] = self.add_subwindow_graph_ranking()

            sublayout_display.addWidget(top_display)
            sublayout_display.addWidget(bottom_display)

            return [sublayout_display, [iv_curve, ff_dist, pmpp_dist, iv_curve_ranked]]

        def add_subwindow_graph_iv_curve(self):
            # Wrap the widget around the layout which holds the plot widget :)
            parent_widget = QWidget()
            layout = QVBoxLayout()
            iv_curve = pg.PlotWidget()
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
