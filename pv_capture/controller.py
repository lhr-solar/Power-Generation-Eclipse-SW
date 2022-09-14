"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      PV Capture Controller. 
@version    3.0.0
@date       2022-09-11
"""

from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout


class PVCaptureController:
    def __init__(self):
        self.window = self.PVCaptureControllerWindow()

    def get_tab(self):
        return [self.window, "PV Capture"]

    class PVCaptureControllerWindow(QWidget):
        def __init__(self):
            super().__init__()

            layout = QGridLayout()
            self.setLayout(layout)

            widget = QLabel("1")
            widget2 = QLabel("2")
            widget3 = QLabel("3")
            widget4 = QLabel("4")
            layout.addWidget(widget, 0, 0)
            layout.addWidget(widget2, 31, 0)
            layout.addWidget(widget3, 0, 17)
            layout.addWidget(widget4, 31, 17)
