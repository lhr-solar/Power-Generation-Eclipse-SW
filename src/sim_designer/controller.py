"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Sim Designer Controller. 
@version    3.0.0
@date       2022-09-14
"""

from fileinput import filename
from sys import displayhook
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
import os

class PVModule: #TODO: figure out how a class in python for this case is actually supposed to look
    def __init__(self, modID):
        self.modID = modID
        self.moduleDimension = 0
        self.bypassDiode = 0
        self.cellModel = 0
        self.cellEfficiency = 0
        self.irradTemp_overTime = [[0 for j in range(2)] for i in range(1000)]

class simulation:
    def __init__(self):
        self.moduleArray = [[None for j in range(12)] for i in range(13)]

class TableModel(QAbstractTableModel): 
    def __init__(self, data):
        super(TableModel, self).__init__()
        self.headerData = ["Irrad, Temp"]
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
        else: 
            self._data[index.row()][index.column()] = value
        return True
    
    def rowCount(self, index):
        value = len(self._data)
        return value
    
    def columnCount(self, index):
        value = len(self._data[0])
        return value

    # def headerData(self, section, orientation, role):
    #     # if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
    #     #     return 
    #     return super().headerData(section, orientation, role)
    
    # def setHeaderData(self, section, orientation, value, role):
    #     if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
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

            self.moduleDimensionList = ["1x1","1x2","2x1","2x2","1x4","4x1","2x4","4x2"]
            self.bypassDiodeList = ["No Bypass Diode","DST10010S", "PMEG045V100EPD","LX2410AILD"]
            self.cellTypeList = ["C60", "E60"]


            main_layout = QGridLayout()
            self.setLayout(main_layout)
            
            simConfig = self.add_sublayout_simconfig()
            main_layout.addWidget(simConfig, 0, 0, 1, 1)
            
            moduleConfig = self.add_sublayout_moduleconfig()
            main_layout.addWidget(moduleConfig, 1, 0, 4, 2)
            
            viewfinder = self.add_sublayout_viewfinder()
            main_layout.addWidget(viewfinder, 5, 2, 2, 2)
            
            load = self.add_sublayout_load()
            main_layout.addWidget(load, 0, 1, 1, 1)

            sim = self.add_sublayout_simulation()
            main_layout.addWidget(sim, 0, 2, 5, 2)
        
        def add_sublayout_moduleconfig(self):
            display = QFrame()
            layoutDisplay = QGridLayout()
            
            # moduleArray = []
            self.currentModule = PVModule("DefaultModule")
            
            #To enter a name for the module
            self.moduleID = QLineEdit()
            self.moduleID.setPlaceholderText("Module ID")
            self.moduleID.textChanged.connect(self.updateCurrentModuleID)
            
            #To choose a preexisting module configuration
            loadModConfigFile = QPushButton("Load Module Config File")
            loadModConfigFile.clicked.connect(self.loadModConfigFile)
            
            #To display and change custom module irradiance and temperature through the course of simulation
            timeLabel = QLabel("Time")
            timeLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
            irradLabel = QLabel("Irrad")
            irradLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
            tempLabel = QLabel("Temp")
            tempLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
            self.tableModel = TableModel(self.currentModule.irradTemp_overTime)
            table = QTableView()
            table.setModel(self.tableModel)
            updateTable = lambda data, index : self.updateIrradTempTable(data, index.row(), index.col())
            self.tableModel.dataChanged.connect(updateTable)
            
            #To customize module dimensions
            moduleDimLabel = QLabel("Module Dimensions")
            moduleDimLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
            self.moduleDim = QComboBox()
            self.moduleDim.addItems(self.moduleDimensionList)

            #To display module length or total cell count of a module
            self.moduleLength = QLabel()
            self.moduleLength.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
            self.moduleDim.currentIndexChanged.connect(self.parseModuleLength)
            modLen = self.parseModuleLength(self.moduleDim.currentData())
            self.moduleLength.setText(str(modLen))
            
            #To choose type of bypass diode or lack thereof
            bypassDiodeLabel = QLabel("Bypass Diode")
            bypassDiodeLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
            self.bypassDiode = QComboBox()
            #Add the bypass diode types
            self.bypassDiode.addItems(self.bypassDiodeList)
            self.bypassDiode.currentIndexChanged.connect(self.updateBypassDiode)
            
            #To choose a cell type
            cellTypeLabel = QLabel("Cell Type")
            cellTypeLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
            self.cellType = QComboBox()
            #Add the cell types
            self.cellType.addItems(self.cellTypeList)
            self.cellType.currentIndexChanged.connect(self.updateCellModel)
            
            #To customize the fill factor or efficiency of the module
            self.localEfficiency = QLineEdit()
            self.localEfficiency.setPlaceholderText("Local EFF")
            self.localEfficiency.textChanged.connect(self.updateCellEff)

            saveButton = QPushButton("Save")
            saveButton.clicked.connect(self.saveModConfigFile)
            saveButton.setStyleSheet("QPushButton"
                                     "{"
                                     "background-color: green"
                                     "}"
                                     "QPushButton::pressed"
                                     "{"
                                     "background-color : darkgreen"
                                     "}")
            
            resetButton = QPushButton("Reset")
            resetButton.clicked.connect(self.resetModConfig)
            resetButton.setStyleSheet("QPushButton"
                                      "{"
                                      "background-color : red"
                                      "}"
                                      "QPushButton::pressed"
                                      "{"
                                      "background-color : darkred"
                                      "}")
            resetButton.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
            )

            addButton = QPushButton("Add")
            addButton.setStyleSheet("QPushButton"
                                      "{"
                                      "background-color : pink"
                                      "}"
                                      "QPushButton::pressed"
                                      "{"
                                      "background-color : purple"
                                      "}")

            modifyButton = QPushButton("Modify")
            modifyButton.setStyleSheet("QPushButton"
                                      "{"
                                      "background-color : yellow"
                                      "}"
                                      "QPushButton::pressed"
                                      "{"
                                      "background-color : orange"
                                      "}")

            layoutDisplay.addWidget(self.moduleID, 0, 0, 1, 1)

            layoutDisplay.addWidget(loadModConfigFile, 0, 1, 1, 3)
            
            layoutDisplay.addWidget(timeLabel, 1, 1, 1, 1)
            layoutDisplay.addWidget(irradLabel, 1, 2, 1, 1)
            layoutDisplay.addWidget(tempLabel, 1, 3, 1, 1)
            layoutDisplay.addWidget(table, 2, 1, 11, 3)
            
            layoutDisplay.addWidget(moduleDimLabel, 1, 0, 1, 1)
            layoutDisplay.addWidget(self.moduleDim, 2, 0, 1, 1)

            layoutDisplay.addWidget(self.moduleLength, 3, 0, 1, 1)

            layoutDisplay.addWidget(bypassDiodeLabel, 4, 0, 1, 1)
            layoutDisplay.addWidget(self.bypassDiode, 5, 0, 1, 1)

            layoutDisplay.addWidget(cellTypeLabel, 6, 0, 1, 1)
            layoutDisplay.addWidget(self.cellType, 7, 0, 1, 1)
            
            layoutDisplay.addWidget(self.localEfficiency, 8, 0, 1, 1)

            layoutDisplay.addWidget(saveButton, 9, 0, 1, 1)
            layoutDisplay.addWidget(addButton, 10, 0, 1, 1)
            layoutDisplay.addWidget(modifyButton, 11, 0, 1, 1)
            layoutDisplay.addWidget(resetButton, 12, 0, 1, 1)
            
            display.setLayout(layoutDisplay)
            
            return display
        
        def loadModConfigFile(self):
            filePath = QFileDialog.getOpenFileName(self, "Open File:", "./", "")
            filePath = str(filePath[0])
            actualFilePath = ""
            for i in range(len(filePath)):
                if i != '':
                    actualFilePath += filePath[i]
                else:
                    break
            # print(actualFilePath)
            with open(actualFilePath, "r") as module:
                currentLine=module.readline().split("\n")[0]
                self.moduleID.setText(currentLine)
                self.moduleDim.setCurrentIndex(int(module.readline()))
                self.bypassDiode.setCurrentIndex(int(module.readline()))
                self.cellType.setCurrentIndex(int(module.readline()))
                currentLine=module.readline().split("\n")[0]
                self.localEfficiency.setText(currentLine)
                for i in range(len(self.currentModule.irradTemp_overTime)):
                    line = module.readline()
                    line = line.split()
                    #print(line)
                    for j in range(len(self.currentModule.irradTemp_overTime[i])):
                        self.currentModule.irradTemp_overTime[i][j] = int(line[j])

        def updateCurrentModuleID(self, ID): 
            #print(ID)
            self.currentModule.modID = ID.strip()
            return

        def updateBypassDiode(self, index):
            self.currentModule.bypassDiode = index
            return

        def updateCellModel(self, index):
            self.currentModule.cellModel = index
            return

        def updateCellEff(self, eff):
            self.currentModule.cellEfficiency = eff.strip()
            return

        def updateIrradTempTable(self, data, row, col):
            self.currentModule.irradTemp_overTime[row][col] = int(data)
            return

        def saveModConfigFile(self):
            folderPath = QFileDialog.getExistingDirectory(self, "Open Directory:", "./", QFileDialog.Option.ShowDirsOnly|QFileDialog.Option.DontResolveSymlinks)
            fileName = self.currentModule.modID.strip("\n")
            fileName = fileName+"_"+datetime.now().strftime('%Y-%m-%d_%H-%M')+".modconfig"
            # print(fileName)
            filePath = os.path.join(folderPath, fileName)
            # print(filePath)
            module = open(filePath, "w")
            module.write(self.currentModule.modID +"\n")
            module.write(str(self.currentModule.moduleDimension) +"\n")
            module.write(str(self.currentModule.bypassDiode) +"\n")
            module.write(str(self.currentModule.cellModel) +"\n")
            module.write(str(self.currentModule.cellEfficiency) +"\n")
            for i in range(len(self.currentModule.irradTemp_overTime)):
                for j in range(len(self.currentModule.irradTemp_overTime[i])):
                    module.write(str(self.currentModule.irradTemp_overTime[i][j])+" ")
                module.write("\n")
            module.close()
            return
        
        def resetModConfig(self):
            self.moduleID.setText(None)
            self.moduleDim.setCurrentIndex(0)
            self.bypassDiode.setCurrentIndex(0)
            self.cellType.setCurrentIndex(0)
            self.localEfficiency.setText(None)
            for i in range(len(self.currentModule.irradTemp_overTime)):
                for j in range(len(self.currentModule.irradTemp_overTime[i])):
                    self.currentModule.irradTemp_overTime[i][j] = 0
            return
            
        def parseModuleLength(self, dim):
            if dim != None:
                self.currentModule.moduleDimension = dim
                #print(dim)
                dim = self.moduleDimensionList[dim]
                #print(int(dim[0])*int(dim[2]))
                self.moduleLength.setText(str(int(dim[0])*int(dim[2])))
                return
            else:
                return -1
            
        def add_sublayout_simconfig(self):
            display = QFrame()
            layoutDisplay = QGridLayout()

            simID = QLineEdit()
            simID.setPlaceholderText("Sim ID")
            simID.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))

            selectSimFile = QPushButton("Select Sim File")
            selectSimFile.clicked.connect(self.selectSimFile)
            selectSimFile.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))

            arrayShapeLabel = QLabel("Array Shape")
            arrayShape = QComboBox()

            saveSim = QPushButton("Save\nSim")
            saveSim.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))

            layoutDisplay.addWidget(simID, 0, 0, 1, 1)
            layoutDisplay.addWidget(selectSimFile, 1, 0, 1, 1)
            
            layoutDisplay.addWidget(arrayShapeLabel, 0, 1, 1, 1)
            layoutDisplay.addWidget(arrayShape, 1, 1, 1, 1)
            layoutDisplay.addWidget(saveSim, 0, 2, 2, 1)

            display.setLayout(layoutDisplay)

            return display
        
        def selectSimFile(self):
            file_path = QFileDialog.getOpenFileName(self, "Open File:", "./", "")
        
        def add_sublayout_load(self):
            display = QFrame()
            layoutDisplay = QGridLayout()

            loadLabel = QLabel("Load Placeholder")
            loadLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layoutDisplay.addWidget(loadLabel, 0, 0, 1, 1)

            display.setLayout(layoutDisplay)

            return display
        
        def add_sublayout_viewfinder(self):
            display = QFrame()
            layoutDisplay = QGridLayout()
            
            viewfinder = QLabel("Viewfinder")
            viewfinder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            colorID = QPushButton("Color Based on ID")
            #colorID.setCheckable(True)
            colorID.setStyleSheet("QPushButton"
                                  "{"
                                  "color : white; background-color : darkgray"
                                  "}"
                                  "QPushButton:pressed"
                                  "{"
                                  "background-color : gray"
                                  "}")
            colorID.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            
            colorTemp = QPushButton("Color Based on Temp")
            #colorTemp.setCheckable(True)
            colorTemp.setStyleSheet("QPushButton"
                                    "{"
                                    "color : white; background-color : darkgray"
                                    "}"
                                    "QPushButton::pressed"
                                    "{"
                                    "background-color : gray"
                                    "}")
            colorTemp.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            
            colorIrrad = QPushButton("Color Based on Irrad")
            #colorIrrad.setCheckable(True)
            colorIrrad.setStyleSheet("QPushButton"
                                     "{"
                                     "color : white; background-color : darkgray"
                                     "}"
                                     "QPushButton::pressed"
                                     "{"
                                     "background-color : gray"
                                     "}")
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
        
        def add_sublayout_simulation(self): 
            display = QFrame()
            layoutDisplay = QGridLayout()

            sim = simulation()
            
            self.simModel = TableModel(sim.moduleArray)
            self.simTable = QTableView()
            self.simTable.setModel(self.simModel)
            self.horizontal_header = self.simTable.horizontalHeader()
            self.horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            
            layoutDisplay.addWidget(self.simTable, 0, 0, 1, 1)

            display.setLayout(layoutDisplay)
            
            return display