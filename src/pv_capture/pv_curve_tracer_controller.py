"""_summary_
@file       pv_curve_tracer_controller.py
@author     Roy Mor (roymor.102@gmail.com) and Matthew Yu (matthewjkyu@gmail.com)
@brief      Talks to the PV Curve Tracer.
@version    0.1.0
@data       2023-02-04
"""

import argparse
from ast import Break
import glob
import os
import sys
import time
from curses import baudrate
from datetime import datetime

import serial
import serial.tools.list_ports
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QIODevice


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

    def load_com_config(self): #, file_path
        # TODO: load from config file comm scheme.
        
        config = {
            "com_port": "COM4",
            "baud_rate": 19200,
            "parity_bit": QSerialPort.Parity.EvenParity,
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

    def save_capture_file(self, capture_conf, capture_data, pv_id):
        # TODO: save a dict of info into a capture file format.
        with open(self.cwd + "/data/"+f"{pv_id['id']}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.capture", 'w') as captureFile:
            config = f"__version: v0.1.0\n\n"
            config += f"Capture Configuration\nPV ID: {pv_id['id']}\nCell Type: {capture_conf['pv_type']}\n"
            config += f"Capture Range: {capture_conf['sample_range']}\nStep Size: {capture_conf['step_size']}\nIterations: {capture_conf['num_iters']}\n"
            config += f"Settling Time: {capture_conf['settling_time']}\n\n"

            data = f"Test Data\n\n"
            for i, gate in enumerate(capture_data['gate']):
                data += f"Gate (V): {capture_data['gate'][i]:.3f}, VSense (V): {capture_data['voltage'][i]:.3f}, ISense (A): {capture_data['current'][i]:.3f}\n"

            captureFile.write(config)
            captureFile.write(data)

    def ok_handshake(self, serial_instance):
        serial_instance.write("OK\r\n".encode('utf-8'))
        while True:
            serialIn = serial_instance.readline().decode('utf-8')
            print(serialIn)
            if serialIn == "OK_RECEIVED\r\n":
                print("proceed")
                break

    # Talk to Curve Tracer

    def capture(
        self, com_conf, capture_conf, sig_res, sig_log, sig_prog, sig_finished
    ):
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
            "pv_type": PV_TYPE,
            "pv_id": PV_ID
        }

        """

        read_data = {
            "gate": [],
            "voltage": [],
            "current": [],
        }

        # Open up a serial instance to the curve tracer using com_conf.
        # with serial.Serial(port=com_conf["com_port"], baudrate=com_conf["baud_rate"]) as uart:
        #     while True:
        #         line = uart.readline()
        #         print(line)
        #         if line == "READY_FOR_TRANSMISSION\r\n":
        #             serial_instance.write("OK")#.encode(capture_conf["enc_scheme"]))
        #             break
        

        serial_instance = serial.Serial(com_conf["com_port"], 57600, 8, serial.PARITY_EVEN, serial.STOPBITS_ONE)
        self.serial_instance = serial_instance
        # serial_instance.setPortName(com_conf["com_port"])
        # serial_instance.setBaudRate(com_conf["baud_rate"])
        # serial_instance.setParity(com_conf["parity_bit"])
        # print(serial_instance.open(QIODevice.OpenModeFlag.ReadWrite))
        while True:
            serialIn = serial_instance.readline().decode('utf-8')
            print(serialIn)
            if serialIn == "READY_FOR_TRANSMISSION\r\n":
                print("ready\n")
                break
        
        baudCheck = True
        while baudCheck:
            self.ok_handshake(serial_instance)

            # while True:
            #     serialIn = serial_instance.readline().decode('utf-8')
            #     print(serialIn)
            #     if serialIn == "READY_FOR_BAUDRATE\r\n":
            #         print("Sending baudrate\n")
            #         baudPrint = f"{com_conf['baud_rate']}\r\n"    
            #         serial_instance.write(baudPrint.encode('utf-8'))
            #         print("sent")
            #         break
            #         # while True:
            #         #     serialIn = serial_instance.readline().decode('utf-8')
            #         #     print(serialIn)
            #         #     if serialIn == "1\r\n":
            #         #         break

            while True:
                serialIn = serial_instance.readline().decode('utf-8')
                print(serialIn)
                if serialIn == "BEGIN_TRANSMISSION\r\n":
                    print("beginning")
                    baudCheck = False
                    break
                elif serialIn == "SWAPPING_BAUDRATE\r\n":
                    print("Swapping bauds")
                    serial_instance.close()
                    serial_instance = serial.Serial(com_conf["com_port"], com_conf["baud_rate"], 8, serial.PARITY_EVEN, serial.STOPBITS_ONE)
                    # serial_instance.baudrate = com_conf["baud_rate"]
                    
       
       
       
        print("writing")
        if(capture_conf['pv_type']=="CELL"):
            pv_type=0
        elif(capture_conf['pv_type']=="MODULE"):
            pv_type=1
        elif(capture_conf['pv_type']=="ARRAY"):
            pv_type=2
        else:
            pv_type=3
        # settTime = capture_conf["settling_time"]*1000
        readConfig = f"type={pv_type},sr=[{capture_conf['sample_range'][0]},{capture_conf['sample_range'][1]},{capture_conf['step_size']}],ni={capture_conf['num_iters']},st_ms={capture_conf['settling_time']},enc={com_conf['enc_scheme']}\r\n"
        # readConfig = " Random string\r\n"
        print(readConfig)
        print("a\r\n")
        serial_instance.flush()
        serial_instance.write(readConfig.encode("utf-8"))
        
        while True:
            serialIn = serial_instance.readline().decode('utf-8')
            print(serialIn)
            if serialIn == "invalid config\r\n":
                print("invalid? uh oh")
            elif serialIn == "valid config\r\n":
                print("valid")
                break
        # TODO: Gather data while emitting updates to ui_signal.
        
        while True:
            serialIn = serial_instance.readline().decode('utf-8')
            print(serialIn)
            if serialIn=="END_SCAN\r\n":
                break
            else:
                if(serialIn[0:4] == "Gate"):
                    serialIn = serialIn.split(", ")
                    # print(f"{serialIn[0][10]} {serialIn[1][12]} {serialIn[2][12]}\n")
                    read_data["gate"].append(float(serialIn[0][10:15]))
                    read_data["voltage"].append(float(serialIn[1][12:17]))
                    read_data["current"].append(float(serialIn[2][12:17]))
                    dataList = [read_data["gate"][-1], read_data["voltage"][-1], read_data["current"][-1]]
                    # dataList = {read_data["gate"][-1], read_data["voltage"][-1], read_data["current"][-1]}
                    # valueCheck = f"gate={dataList[0]} | voltage={dataList[1]} | current={dataList[2]}\n"
                    # print(valueCheck)
                    sig_res.emit(dataList)
        # print(f"Gate (V): {read_data['gate'][0]}, VSense (V): {read_data['voltage'][0]}, ISense (A): {read_data['current'][0]}\n")
        # print(f"Gate (V): {read_data['gate'][4]}, VSense (V): {read_data['voltage'][4]}, ISense (A): {read_data['current'][4]}\n\n")
        sig_finished.emit()
        return read_data
        
if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    controller = PVCurveTracerController()

    capture_conf = {
        "sample_range": [.25, .5],
        "step_size": .01,
        "num_iters": 5,
        "settling_time": 5,
        "pv_type": "CELL",
        "pv_id": "ok"
    }
    print("READ_START\n")
    
    readData = controller.capture(controller.load_com_config(), capture_conf, 0, 0, 0, 0)

    controller.save_capture_file(capture_conf, readData)

