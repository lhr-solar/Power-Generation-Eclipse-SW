"""_summary_
@file       controller.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Sim Designer Controller. 
@version    3.0.0
@date       2022-09-14
"""

from PyQt6.QtWidgets import QWidget


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
