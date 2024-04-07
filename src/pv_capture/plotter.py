import numpy as np
import time

import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QUrl, QObject, Signal, Slot, QPointF
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView

import threading

sys.path.append('src/pv_capture')
from pv_curve_tracer_controller import PVCurveTracerController

class Plotter(QObject):
    new_point = Signal(QPointF)
    re_scale = Signal(float, float, float, float)
    sig_res = Signal(list)

    def __init__(self):
        super().__init__()
    
    # @Slot()
    # def plot(self):
    #     print("READ_START\n")
    #     controller = PVCurveTracerController()
    #     capture_conf = {
    #         "sample_range": [.25, .5],
    #         "step_size": .01,
    #         "num_iters": 5,
    #         "settling_time": 5,
    #         "pv_type": "CELL",
    #         "pv_id": "ok"
    #     }
    #     readData = controller.capture(controller.load_com_config(), capture_conf, self.sig_res, 0, 0, 0)
    #     controller.save_capture_file(capture_conf, readData)

    def capture(self, condition):
        with condition:
            print("Inside capture thread.")
            condition.wait()
            controller = PVCurveTracerController()
            capture_conf = {
                "sample_range": [.25, .5],
                "step_size": .01,
                "num_iters": 5,
                "settling_time": 5,
                "pv_type": "CELL",
                "pv_id": "ok"
            }
            readData = controller.capture(controller.load_com_config(), capture_conf, self.sig_res, 0, 0, 0)
            controller.save_capture_file(capture_conf, readData)
    
    @Slot()
    def plot(self):
        condition = threading.Condition()

        capture_thread = threading.Thread(target=self.capture, args=(condition,))
        capture_thread.start()
        
        print("notifying the pv capture thread.")
        with condition:
            condition.notify()

        print("READ_START\n")

    # ''' 
    # the idea is the capture function (that captures all the IV, PV info) will call the following two 
    # functions for each data point collected. 
    # these two will emit the information needed by the QML end to make changes to the plot.
    # '''
    @Slot(float, float) # probably not needed 
    def add_new_point(self, x, y):
        point = QPointF(x, y)
        print("new point works")
        self.new_point.emit(point)
    
    # @Slot(list, list) # probably not needed
    # def scale_axis(self, list_x, list_y): 
    #     yMax = max(list_y)
    #     yMin = min(list_y)
    #     xMax = max(list_x)
    #     xMin = min (list_x)
    #     self.re_scale.emit(yMax, yMin, xMax, xMin)
    
    # @Slot(float, float, float, float)
    # def scale_axis(self, minx, maxx, miny, maxy): 
    #     print(f"rescale? {miny}, {maxy}, {minx}, {maxx}")
    #     self.re_scale.emit(maxy, miny, maxx, minx)
    
    # @Slot(list, list)
    # def plot(self, x, y):
    #     for i in np.arange(len(x)):
    #         plot.add_new_point(x[i], y[i])
    #         # plot.scale_axis(x[:i+1], y[:i+1])
    #         # time.sleep(0.2)