"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Sim Designer Controller. 
@version    3.0.0
@date       2022-09-14
"""

from tkinter import HORIZONTAL
from types import CellType
from PyQt6.QtWidgets import ( #copying all widget imports from pv_cap temporarily, remove unecessary later
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QTextEdit,
    QHBoxLayout,
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
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt6.QtCore import Qt, QAbstractTableModel #also copied from pv_cap
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
import pyqtgraph as pg
from datetime import datetime
from array import *

class PVModule: #TODO: figure out how a class in python for this case is actually supposed to look
    # modID = "defaultID"
    # bypassDiode = "defaultBD"
    # cellModel = "defaultCM"
    # cellEfficiency = "defaultEfficiency"
    # irradTemp_overTime = [[0 for i in range(1000)] for j in range(2)]
    # modType = 0 
    
    def __init__(self, modID):
        self.modID = modID
        self.bypassDiode = "defaultBD"
        self.cellModel = "defaultCM"
        self.cellEfficiency = "defaultEfficiency"
        self.irradTemp_overTime = [[0 for j in range(2)] for i in range(1000)]
        self.modType = 0

class TableModel(QAbstractTableModel): 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
    
    #TODO: FIGURE THIS OUT 
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[index.row()][index.column()]
            return value
    
    def setData(self, index, value, role):
        if index.column() == 0 and int(value) > 1000:
            self._data[index.row()][0] = 1000
        elif index.column() == 0 and int(value) < 0:
            self._data[index.row()][0] = 0
        elif index.column() == 1 and int(value) > 150:
            self._data[index.row()][1] = 150
        elif index.column() == 1 and int(value) < 0:
            self._data[index.row()][1] = 0
        self._data[index.row()][index.column()] = value
        return True
    
    def rowCount(self, index):
        value = len(self._data)
        return value
    
    def columnCount(self, index):
        value = len(self._data[0])
        return value
    
    # def setHeaderData(self, section, orientation, value, role):
    #     if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
    #         self.horizontalHeaders[section] = value
    #         return True
    #     return super().setHeaderData(section, orientation, value, role)
    
    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable|Qt.ItemFlag.ItemIsEnabled|Qt.ItemFlag.ItemIsEditable
    
    

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
            
            moduleconfig = self.add_sublayout_moduleconfig()
            main_layout.addWidget(moduleconfig, 0, 0, 0, 0)
            
            # viewfinder = self.add_sublayout_viewfinder()
            # main_layout.addWidget(viewfinder, 46, 4, 16, 50)
            
            # saveReset = self.add_sublayout_S_R()
            # main_layout.addWidget(saveReset, 64, 26, 4, 26)
        
        def add_sublayout_moduleconfig(self):
            display = QFrame()
            layoutDisplay = QGridLayout()
            
            moduleArray = [PVModule("Default Module")]
            
            moduleIDLabel = QLabel("Module ID")
            moduleID = QLineEdit()
            moduleID.setPlaceholderText("2x4 Test 1")
            
            orLabel = QLabel("OR")
            orLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.tableModel = TableModel(moduleArray[0].irradTemp_overTime)
            # self.tableModel.setHeaderData(0, Qt.Orientation.Horizontal, "Irrad", Qt.ItemDataRole.DisplayRole)
            # self.tableModel.setHeaderData(1, Qt.Orientation.Horizontal, "Temp", Qt.ItemDataRole.DisplayRole)
            table = QTableView()
            table.setModel(self.tableModel)
            
            bypassDiodeLabel = QLabel("Bypass Diode")
            bypassDiode = QComboBox()
            #Add the bypass diode types
            # bypassDiode.addItems(["No bypass diode", ])
            
            cellTypeLabel = QLabel("Cell Type")
            cellType = QComboBox()
            #Add the cell types
            # cellType.addItems(["No bypass diode", ])
            
            localEfficiencyLabel = QLabel("Local Efficiency")
            localEfficiency = QLineEdit()
            localEfficiency.setPlaceholderText(".75")
            
            layoutDisplay.addWidget(moduleIDLabel, 0, 0, 1, 2)
            layoutDisplay.addWidget(moduleID, 1, 0, 1, 2)
            layoutDisplay.addWidget(orLabel, 2, 0, 1, 2)
            layoutDisplay.addWidget(table, 5, 0, 4, 1)
            
            
            display.setLayout(layoutDisplay)
            
            return display
        
        # def add_sublayout_pvconfig(self):
        #     display = QFrame()
        #     layoutDisplay = QGridLayout()

        #     # fileSelectorLabel = QLabel("PV Config File Selector")
        #     # fileSelectorLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #     fileSelector = QPushButton("PV Config File Selector")
        #     fileSelector.clicked.connect
        
        # def add_sublayout_viewfinder(self):
        #     display = QFrame()
        #     layoutDisplay = QGridLayout()
            
        #     viewfinder = QLabel("Viewfinder")
        #     viewfinder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        #     colorID = QPushButton("Color Based on ID")
        #     #colorID.setCheckable(True)
        #     colorID.setStyleSheet("QPushButton"
        #                           "{"
        #                           "color : white; background-color : darkgray"
        #                           "}"
        #                           "QPushButton:pressed"
        #                           "{"
        #                           "background-color : gray"
        #                           "}")
        #     colorID.setSizePolicy(
        #         QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        #     )
            
        #     colorTemp = QPushButton("Color Based on Temp")
        #     #colorTemp.setCheckable(True)
        #     colorTemp.setStyleSheet("QPushButton"
        #                             "{"
        #                             "color : white; background-color : darkgray"
        #                             "}"
        #                             "QPushButton::pressed"
        #                             "{"
        #                             "background-color : gray"
        #                             "}")
        #     colorTemp.setSizePolicy(
        #         QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        #     )
            
        #     colorIrrad = QPushButton("Color Based on Irradiance")
        #     #colorIrrad.setCheckable(True)
        #     colorIrrad.setStyleSheet("QPushButton"
        #                              "{"
        #                              "color : white; background-color : darkgray"
        #                              "}"
        #                              "QPushButton::pressed"
        #                              "{"
        #                              "background-color : gray"
        #                              "}")
        #     colorIrrad.setSizePolicy(
        #         QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        #     )
            
        #     timeStepLabel = QLabel("Time Step")
        #     timeStepLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        #     timeStep = QSlider()
        #     timeStep.setMinimum(0)
        #     timeStep.setMaximum(1000)
        #     timeStep.setSingleStep(1)
        #     timeStep.setOrientation(Qt.Orientation.Horizontal)
            
        #     timeStepMin = QLabel(str(timeStep.minimum()))
        #     timeStepMin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #     timeStepMax = QLabel(str(timeStep.maximum()))
        #     timeStepMax.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        #     layoutDisplay.addWidget(viewfinder, 0, 0, 1, 18)
        #     layoutDisplay.addWidget(colorID, 1, 1, 2, 4)
        #     layoutDisplay.addWidget(colorTemp, 1, 7, 2, 4)
        #     layoutDisplay.addWidget(colorIrrad, 1, 13, 2, 4)
            
        #     layoutDisplay.addWidget(timeStepLabel, 3, 8, 1, 2)
        #     layoutDisplay.addWidget(timeStep, 4, 2, 1, 14)
        #     layoutDisplay.addWidget(timeStepMin, 4, 0, 1, 2)
        #     layoutDisplay.addWidget(timeStepMax, 4, 16, 1, 2)
            
        #     display.setLayout(layoutDisplay)
            
        #     return display
            
        
        # def add_sublayout_S_R(self):
        #     display = QFrame()
        #     layout_display = QGridLayout()
            
        #     #widget is the save button and the reset button
            
        #     saveButton = QPushButton("SAVE")
        #     saveButton.setStyleSheet("QPushButton"
        #                              "{"
        #                              "background-color: green"
        #                              "}"
        #                              "QPushButton::pressed"
        #                              "{"
        #                              "background-color : darkgreen"
        #                              "}")
        #     saveButton.setSizePolicy(
        #         QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        #     )
            
        #     resetButton = QPushButton("RESET")
        #     resetButton.setStyleSheet("QPushButton"
        #                               "{"
        #                               "background-color : red"
        #                               "}"
        #                               "QPushButton::pressed"
        #                               "{"
        #                               "background-color : darkred"
        #                               "}")
        #     resetButton.setSizePolicy(
        #         QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        #     )
            
        #     #make buttons do stuff
            
        #     layout_display.addWidget(saveButton, 0, 4, 1, 3)
        #     layout_display.addWidget(resetButton, 0, 0, 1, 3)
            
        #     display.setLayout(layout_display)
            
        #     return display
