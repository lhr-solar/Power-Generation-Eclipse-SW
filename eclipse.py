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
from PyQt6.QtWidgets import QApplication
# from PyQt6.QtWidgets import QApplication, QLabel, QWidget

# from pv_capture.ui_controller import PVCaptureController
# from sim_designer.ui_controller import SimDesignerController
# from power_gen_sim.ui_controller import PowerGenSimController

class Eclipse:
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
        # self.window = QtWidget()
        # self.window.show()

        # Generate instances of each module.
        # self.pv_capture_instance    = PVCaptureController()
        # self.sim_designer           = SimDesignerController()
        # self.power_gen_sim          = PowerGenSimController()

    def run(self):
        # self.exe = self.app.exec()
        pass
    
    def stop(self):
        QApplication.quit()
        pass

if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    
    # Get the primary monitor.
    monitors = get_monitors()
    eclipse = Eclipse(monitors[0].width, monitors[1].height)
    eclipse.run()
    
    print("Hello world!")
