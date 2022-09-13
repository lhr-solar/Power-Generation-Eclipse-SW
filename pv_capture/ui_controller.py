"""_summary_
@file       ui_controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      UI Controller for managing the PV Capture Controller. 
@version    0.3.0
@date       2022-09-11
"""

from PyQt6.QtWidgets import (
    QLabel
)

class PVCaptureController:
    def __init__(self):
        self.window = QLabel("PV Capture")

    def get_tab(self):
        return [self.window, "PV Capture"]

    class PVCaptureControllerWindow():
        def __init__(self):
            super().__init__()
            # Setup window