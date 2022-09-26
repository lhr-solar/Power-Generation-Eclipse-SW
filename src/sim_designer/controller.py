"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Sim Designer Controller. 
@version    3.0.0
@date       2022-09-14
"""

from datetime import datetime

import pyqtgraph as pg
from PyQt6.QtCore import Qt  # also copied from pv_cap
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtWidgets import (  # copying all widget imports from pv_cap temporarily, remove unecessary later
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
    QSlider,
    QStackedLayout,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SimDesignerController:
    def __init__(self):
        self.data = self.Data(self)
        self.ui = self.UI(self)

        # Update the UI with relevant setup data.

    def get_data(self):
        return [self.data, "Sim Designer"]

    def get_ui(self):
        return [self.ui, "Sim Designer"]

    class Data:
        def __init__(self, parent):
            self.parent = parent

    class UI(QWidget):
        def __init__(self, parent):
            super().__init__()
            self.parent = parent

            main_layout = QGridLayout()
            self.setLayout(main_layout)

            viewfinder = self.add_sublayout_viewfinder()
            main_layout.addWidget(viewfinder, 46, 4, 16, 50)

            saveReset = self.add_sublayout_S_R()
            main_layout.addWidget(saveReset, 64, 26, 4, 26)

        # def add_sublayout_pvconfig(self):
        #     display = QFrame()
        #     layoutDisplay = QGridLayout()

        #     # fileSelectorLabel = QLabel("PV Config File Selector")
        #     # fileSelectorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #     fileSelector = QPushButton("PV Config File Selector")
        #     fileSelector.clicked.connect

        def add_sublayout_viewfinder(self):
            display = QFrame()
            layoutDisplay = QGridLayout()

            viewfinder = QLabel("Viewfinder")
            viewfinder.setAlignment(Qt.AlignmentFlag.AlignCenter)

            colorID = QPushButton("Color Based on ID")
            # colorID.setCheckable(True)
            colorID.setStyleSheet(
                "QPushButton"
                "{"
                "color : white; background-color : darkgray"
                "}"
                "QPushButton:pressed"
                "{"
                "background-color : gray"
                "}"
            )
            colorID.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            colorTemp = QPushButton("Color Based on Temp")
            # colorTemp.setCheckable(True)
            colorTemp.setStyleSheet(
                "QPushButton"
                "{"
                "color : white; background-color : darkgray"
                "}"
                "QPushButton::pressed"
                "{"
                "background-color : gray"
                "}"
            )
            colorTemp.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            colorIrrad = QPushButton("Color Based on Irradiance")
            # colorIrrad.setCheckable(True)
            colorIrrad.setStyleSheet(
                "QPushButton"
                "{"
                "color : white; background-color : darkgray"
                "}"
                "QPushButton::pressed"
                "{"
                "background-color : gray"
                "}"
            )
            colorIrrad.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            timeStepLabel = QLabel("Time Step")
            timeStepLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

            timeStep = QSlider()
            timeStep.setMinimum(0)
            timeStep.setMaximum(1000)
            timeStep.setSingleStep(1)
            timeStep.setOrientation(Qt.Orientation.Horizontal)

            timeStepMin = QLabel(str(timeStep.minimum()))
            timeStepMin.setAlignment(Qt.AlignmentFlag.AlignCenter)
            timeStepMax = QLabel(str(timeStep.maximum()))
            timeStepMax.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layoutDisplay.addWidget(viewfinder, 0, 0, 1, 18)
            layoutDisplay.addWidget(colorID, 1, 1, 2, 4)
            layoutDisplay.addWidget(colorTemp, 1, 7, 2, 4)
            layoutDisplay.addWidget(colorIrrad, 1, 13, 2, 4)

            layoutDisplay.addWidget(timeStepLabel, 3, 8, 1, 2)
            layoutDisplay.addWidget(timeStep, 4, 2, 1, 14)
            layoutDisplay.addWidget(timeStepMin, 4, 0, 1, 2)
            layoutDisplay.addWidget(timeStepMax, 4, 16, 1, 2)

            display.setLayout(layoutDisplay)

            return display

        def add_sublayout_S_R(self):
            display = QFrame()
            layout_display = QGridLayout()

            # widget is the save button and the reset button

            saveButton = QPushButton("SAVE")
            saveButton.setStyleSheet(
                "QPushButton"
                "{"
                "background-color: green"
                "}"
                "QPushButton::pressed"
                "{"
                "background-color : darkgreen"
                "}"
            )
            saveButton.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            resetButton = QPushButton("RESET")
            resetButton.setStyleSheet(
                "QPushButton"
                "{"
                "background-color : red"
                "}"
                "QPushButton::pressed"
                "{"
                "background-color : darkred"
                "}"
            )
            resetButton.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            # make buttons do stuff

            layout_display.addWidget(saveButton, 0, 4, 1, 3)
            layout_display.addWidget(resetButton, 0, 0, 1, 3)

            display.setLayout(layout_display)

            return display
