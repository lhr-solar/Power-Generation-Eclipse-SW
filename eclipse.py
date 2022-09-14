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
    QGridLayout,
)

from pv_capture.controller import PVCaptureController
from sim_designer.controller import SimDesignerController
from power_gen_sim.controller import PowerGenSimController
from about.controller import AboutController


class Eclipse:
    """_summary_
    The main class instance, Eclipse, holds four controllers, one for each
    module. These controllers manage their own data and are independent of each
    other.
    """

    def __init__(self, window_width=1920, window_height=1080, frame_rate=30):
        self.window_width = window_width
        self.window_height = window_height
        self.frame_rate = frame_rate

        # Setup the main window.
        self.app = QApplication(sys.argv)
        self.window = self.EclipseWindow()
        self.window.setFixedSize(QSize(720, 480))
        self.window.show()

        # Generate instances of each module.
        self.instances = [
            AboutController(),
            PVCaptureController(),
            SimDesignerController(),
            PowerGenSimController(),
        ]

        # Get tabs for each instance.
        tabs = [instance.get_tab() for instance in self.instances]

        # Set window tabs.
        self.window.add_tab_subwindows(tabs)

    def run(self):
        self.exe = self.app.exec()

    def stop(self):
        QApplication.quit()

    class EclipseWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Eclipse")
            self.eclipse_widget = QTabWidget()
            self.setCentralWidget(self.eclipse_widget)

        def add_tab_subwindows(self, tabs):
            # Add all tabs to the main window.
            for (idx, (tab_widget, tab_name)) in enumerate(tabs):
                self.eclipse_widget.addTab(tab_widget, tab_name)
                # About page is set as the active page on startup.
                if tab_name == "About":
                    self.eclipse_widget.setCurrentIndex(idx)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    # Get the primary monitor.
    monitors = get_monitors()
    eclipse = Eclipse(monitors[0].width, monitors[0].height)
    eclipse.run()

    print("Hello world!")
