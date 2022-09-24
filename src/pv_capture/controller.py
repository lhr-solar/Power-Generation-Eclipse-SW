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

    class UI(QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            main_layout = QGridLayout()
            self.setLayout(main_layout)

            pv_config_display = self.add_sublayout_pv_config()
            main_layout.addWidget(pv_config_display, 0, 0, 3, 3)

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

            title = QLabel("PV Config")
            layout.addWidget(title, 0, 0, 1, 2)
            display.setLayout(layout)
            return display

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