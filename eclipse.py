"""_summary_
@file       eclipse.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Entry point for the Eclipse photovoltaic characterization and
            simulation application.
@version    3.0.0
@date       2022-09-14
"""

import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QApplication, QGridLayout, QMainWindow,
                             QProgressBar, QTabWidget, QWidget)
from screeninfo import get_monitors

from src.about.controller import AboutController
from src.power_gen_sim.controller import PowerGenSimController
from src.pv_capture.controller import PVCaptureController
from src.sim_designer.controller import SimDesignerController


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

        self.app.setStyleSheet(
            """
            QTabWidget {
                background: lightgray;
            }
            QFrame {
                border: 1px solid black;
            }
            QLabel, QComboBox {
                border: None;
            }
            QComboBox {
                background: white;
            }
            QWidget {
                border: 1px solid black;
            }
            QLineEdit[readOnly=\"true\"] {
                background-color: #F0F0F0;
            }
        """
        )

        self.window = self.EclipseWindow()
        self.window.setFixedSize(1080, 720)
        self.window.show()

        # Generate instances of each module.
        self.instances = [
            AboutController(),
            PVCaptureController(),
            SimDesignerController(),
            PowerGenSimController(),
        ]

        # Get tabs for each instance.
        tabs = [instance.get_ui() for instance in self.instances]

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
