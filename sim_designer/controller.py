"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Sim Designer Controller. 
@version    3.0.0
@date       2022-09-11
"""

from PyQt6.QtWidgets import QLabel


class SimDesignerController:
    def __init__(self):
        self.window = QLabel("Sim Designer.")

    def get_tab(self):
        return [self.window, "Sim Designer"]

    class SimDesignerControllerWindow:
        def __init__(self):
            super().__init__()
            # Setup window
