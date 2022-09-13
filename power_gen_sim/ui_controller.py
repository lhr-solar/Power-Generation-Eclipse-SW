"""_summary_
@file       ui_controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      UI Controller for managing the Power Gen Sim Controller. 
@version    0.3.0
@date       2022-09-11
"""

from PyQt6.QtWidgets import (
    QLabel
)

class PowerGenSimController:
    def __init__(self):
        self.window = QLabel("Power Gen Sim")

    def get_tab(self):
        return [self.window, "Power Gen Sim"]

    class PowerGenSimControllerWindow():
        def __init__(self):
            super().__init__()
            # Setup window