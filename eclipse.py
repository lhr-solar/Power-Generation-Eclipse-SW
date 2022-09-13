"""_summary_
@file       eclipse.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Entry point for the Eclipse photovoltaic characterization and
            simulation application.
@version    0.3.0
@date       2022-09-11
"""

import sys
from screeninfo import get_monitors
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow,
    QTabWidget,
    QWidget,
    QProgressBar,
    QGridLayout
)

from pv_capture.ui_controller import PVCaptureController
from sim_designer.ui_controller import SimDesignerController
from power_gen_sim.ui_controller import PowerGenSimController

class Eclipse():
    """_summary_
    The main class instance, Eclipse, holds three controllers, one for each
    module. These controllers manage their own data and are independent of each
    other.
    """

    def __init__(self, window_width=1920, window_height=1080, frame_rate=30):
        self.window_width           = window_width
        self.window_height          = window_height
        self.frame_rate             = frame_rate

        # Setup the main window.
        self.app = QApplication(sys.argv)
        self.window = self.EclipseWindow()
        self.window.setFixedSize(QSize(self.window_width, self.window_height))
        self.window.show()

        # Generate instances of each module.
        self.pv_capture_instance    = PVCaptureController()
        self.sim_designer           = SimDesignerController()
        self.power_gen_sim          = PowerGenSimController()

        # Set window tabs.
        self.window.add_tab_subwindows([
            self.pv_capture_instance.get_tab(),
            self.sim_designer.get_tab(),
            self.power_gen_sim.get_tab()
        ])

    def run(self):
        self.exe = self.app.exec()
    
    def stop(self):
        QApplication.quit()

    class EclipseWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Eclipse")
            self.layout = QGridLayout()
            self.eclipse_widget = QTabWidget()
            self.eclipse_widget.setLayout(self.layout)
            self.setCentralWidget(self.eclipse_widget)

        def add_tab_subwindows(self, tabs):
            for (tab_widget, tab_name) in tabs:
                self.eclipse_widget.addTab(tab_widget, tab_name)
            self.layout.addWidget(self.eclipse_widget, 0, 0)

if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    
    # Get the primary monitor.
    monitors = get_monitors()
    eclipse = Eclipse(monitors[0].width, monitors[0].height)
    eclipse.run()
    
    print("Hello world!")
