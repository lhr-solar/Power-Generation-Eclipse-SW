"""
UIController.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/17/20
Last Modified: 11/24/20

Description: The UIController class is a class that builds the GUI for the
PVSim. It uses the PyQT backend to create a set of viewable and interactable
graphs for the simulator. In addition, it allows the user to control properties
of the simulation and execute it in real time.

The simulator should have at least two tabs (and maybe three) representing
different types of simulation:
- Source Simulator: This tab allows us to view the IV characteristics of the
  PVSource models over various environmental conditions.
- MPPT Simulator: This tab allows us to view the MPPT decisions over time
  relative to the source output.
- Thermal Simulator: What this will look like or whether it will be instantiated
  is up for discussion.
"""
# Library Imports.
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)
import signal
import sys

# Custom Imports.
from ArraySimulation.Controller.MPPTView import MPPTView
from ArraySimulation.Controller.SourceView import SourceView
from ArraySimulation.Controller.DataController import DataController


class UIController:
    """
    The UIController class is a class that builds the GUI for the PVSim. It
    uses the PyQT backend to create a set of viewable and interactable graphs for
    the simulator. In addition, it allows the user to control properties of the
    simulation and execute it in real time.
    """

    def __init__(self):
        self._framerate = 30
        self.sourceSimData = None
        self.MPPTSimData = None

    def startup(self, windowWidth=1920, windowHeight=1080):
        """
        The setup routine performs any data and UI operations required to get
        the PVSim app operational. In particular it looks to do the following,
        in order:

        1. Startup the application UI runtime. This allows us to build and
           display any UI objects henceforth.
        2. Setup the View classes corresponding to each tab in the UI.
        3. Setup data structures for ingesting data. The main PVSim routines
           access these data structures to update the Display UI.
        4. Setup the main tabbed pane window. This generates a top level layout
           that contains and manages the individual Views.

        Parameters
        ----------
        windowWidth: int
            Width of the window. Defaults to 1080p.
        windowHeight: int
            Height of the window. Defaults to 720p.
        """
        # 1. Setup data structures for ingesting data and managing the
        #    simulation execution pipeline.
        self.dataController = DataController()

        # 2. Startup the application UI runtime.
        self.app = QApplication(sys.argv)
        # TODO: set PYQT stylesheet

        # 3. Setup the View classes corresponding to each tab in the UI.
        self.sourceView = SourceView(self.dataController, self._framerate)
        self.MPPTView = MPPTView(self.dataController, self._framerate)

        # 4. Setup the main tabbed pane window.
        self.win = QMainWindow()
        self.win.setGeometry(0, 0, windowWidth, windowHeight)
        self.win.setWindowTitle("PVSimulator 2020")
        self.win.tabWidget = self._createTabbedPaneWidget()
        self.win.setCentralWidget(self.win.tabWidget)
        self.win.show()

        # 5. Set up timer to enable CTRL+C sigints.
        signal.signal(signal.SIGINT, self.shutdown)
        timer = QTimer()
        timer.timeout.connect(lambda: None)
        timer.start(100)

        self.exe = self.app.exec_()

    def shutdown(self, *args):
        """
        Cleans up the main window and associated Views and shuts down the
        application.

        Handler for the SIGINT signal.
        """
        sys.stderr.write("\r")
        if (
            QMessageBox.question(
                None,
                "",
                "Are you sure you want to quit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            == QMessageBox.Yes
        ):
            QApplication.quit()

    def _createTabbedPaneWidget(self):
        widget = QWidget()
        widget.layout = QVBoxLayout(widget)

        # Initialize tab screen.
        widget.tabs = QTabWidget()

        # Add Views.
        try:
            sourceLayout = self.sourceView.getLayout()
            widget.tabs.addTab(sourceLayout, "Source Simulator")
            MPPTLayout = self.MPPTView.getLayout()
            widget.tabs.addTab(MPPTLayout, "MPPT Simulator")
        except Exception as e:
            print("[LOG][_createTabbedPaneWidget] ", e)

        widget.tabs.resize(300, 200)  # TODO: remove magic numbers
        widget.layout.addWidget(widget.tabs)
        widget.setLayout(widget.layout)

        return widget
