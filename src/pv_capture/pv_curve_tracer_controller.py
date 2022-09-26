"""_summary_
@file       pv_curve_tracer_controller.py
@author     Roy Mor () and Matthew Yu (matthewjkyu@gmail.com)
@brief      Talks to the PV Curve Tracer.
@version    0.0.1
@data       2022-09-22
"""

import argparse
import glob
import os
import sys
from curses import baudrate
from datetime import datetime

import serial
import serial.tools.list_ports
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo


class PVCurveTracerController:
    def __init__(self) -> None:
        self.serial_instance = None
        self.cwd = os.getcwd()

    # Communication configuration

    def list_ports(self):
        # Modified from https://stackoverflow.com/a/14224477
        if sys.platform.startswith("win"):
            ports = ["COM%s" % (i + 1) for i in range(256)]
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob("/dev/tty[A-Za-z]*")
            ports = [port for port in ports if "ACM" in port or "USB" in port]
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")
        else:
            ports = []
        return ports

    def list_baud_rates(self):
        return [4800, 9600, 19200, 38400, 57600, 115200]

    def list_parity(self):
        return [
            "PARITY_NONE",
            "PARITY_EVEN",
            "PARITY_ODD",
            "PARITY_MARK",
            "PARITY_SPACE",
        ]

    def list_encoding_schemes(self):
        # TODO: load from folder any files containing encoding schemes
        return ["NONE"]

    def list_com_config_files(self):
        obj = os.scandir(path=self.cwd + "/data/com_confs")
        com_conf_files = [
            entry.name
            for entry in obj
            if entry.is_file() and entry.name.endswith(".com_conf")
        ]
        return com_conf_files

    def load_com_config(self, file_path):
        # TODO: load from config file comm scheme.
        config = {
            "com_port": "COM10",
            "baud_rate": 9600,
            "parity_bit": "PARITY_EVEN",
            "enc_scheme": "NONE",
        }
        return config

    # PV Capture configuration

    def list_capture_files(self):
        obj = os.scandir(path=self.cwd + "/data/captures")
        capture_files = [
            entry.name
            for entry in obj
            if entry.is_file() and entry.name.endswith(".capture")
        ]
        return capture_files

    def load_capture_config(self, file_path):
        # TODO: load from config file capture scheme.
        pass

    def list_capture_config_files(self):
        obj = os.scandir(path=self.cwd + "/data/capture_confs")
        capture_conf_files = [
            entry.name
            for entry in obj
            if entry.is_file() and entry.name.endswith(".capture_conf")
        ]
        return capture_conf_files

    def load_capture_file(self, file_path):
        # TODO: load from capture file the capture.
        capture = {
            "version": "v0.0.0",
            "file_name": "example.capture",
            "brief": "Example PV Characterization Capture Log.",
            "author": "Matthew Yu",
            "generation_time": "2022_09_25_00_00_00",
            "pv_id": "TEST000",
            "pv_type": "CELL",
            "irradiance": 1000,
            "temperature": 25,
            "voltage": [
                0.00,
                0.10,
                0.50,
                0.84,
                1.49,
                2.12,
                2.99,
                3.56,
                4.14,
                5.00,
                5.13,
                6.59,
                7.21,
            ],
            "current": [
                6.15,
                6.00,
                5.68,
                5.30,
                4.88,
                4.23,
                3.66,
                3.20,
                1.65,
                1.13,
                1.00,
                0.32,
                0.00,
            ],
        }
        return capture

    def save_capture_file(self, capture):
        # TODO: save a dict of info into a capture file format.
        pass

    # Talk to Curve Tracer

    def capture(self, com_conf, capture_conf, ui_signal):
        """
        com_conf = {
            "com_port": COM_PORT,
            "baud_rate": BAUD_RATE,
            "parity_bit": PARITY_BIT,
            "enc_scheme": ENC_SCHEME
        }

        capture_conf = {
            "sample_range": [LOW_RANGE, HIGH_RANGE],
            "step_size": STEP_SIZE,
            "num_iters": NUM_ITERS,
            "settling_time": SETTLING_TIME_MS,
            "pv_type": PV_TYPE
        }

        """
        # Open up a serial instance to the curve tracer using com_conf.
        serial_instance = QSerialPort()
        self.serial_instance = serial_instance
        serial_instance.setPortName(com["com_port"])
        serial_instance.setBaudRate(com["baud_rate"])
        serial_instance.setParity(com["parity_bit"])
        serial_instance.open(QSerialPort.ReadWrite)

        # TODO: Transmit message to set encoding scheme.

        # TODO: Transmit message to set capture configuration.

        # TODO: Gather data while emitting updates to ui_signal.

        # TODO: Return completed capture.
