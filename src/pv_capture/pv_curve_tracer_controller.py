"""_summary_
@file       pv_curve_tracer_controller.py
@author     Roy Mor (roymor.102@gmail.com), Matthew Yu (matthewjkyu@gmail.com), and Connor Shen (connor.lishen@gmail.com)
@brief      Talks to the PV Curve Tracer.
@version    0.2.0
@data       2023-02-06
"""

import os
import sys
import time
import json
import glob
from datetime import datetime

import serial
import serial.tools.list_ports
from PyQt6.QtCore import QObject
from src.DatabaseManager import DatabaseManager

class PVCurveTracerController (QObject):
    def __init__(self) -> None:
        self.serial_instance = None
        self.cwd = os.getcwd()
        self.db = DatabaseManager()

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
        file_path = os.path.join(self.cwd, "data/com_confs/config.json")

        if not os.path.exists(file_path):
            # Return default config if file does not exist
            return {
                "com_port": self.list_ports()[0] if self.list_ports() else None,
                "baud_rate": 115200,
                "parity_bit": serial.PARITY_NONE,
            }

        with open(file_path, "r") as config_file:
            return json.load(config_file)
        
    def save_com_config(self, com_conf):
        file_path = os.path.join(self.cwd, "data/com_confs/config.json")
        
        with open(file_path, "w") as config_file:
            json.dump(com_conf, config_file, indent=4)

        print(f"Communication config saved to {file_path}")

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
        file_path = os.path.join(self.cwd, "data/capture_confs/config.json")

        if not os.path.exists(file_path):
            return {
                "sample_range": [0.0, 1.0],
                "step_size": 0.01,
                "num_iters": 10,
                "settling_time": 1000,
                "pv_type": "CELL",
                "pv_id": "DEFAULT_PV",
            }

        with open(file_path, "r") as config_file:
            return json.load(config_file)
        
    def save_capture_config(self, capture_conf):
        """Saves capture settings to a JSON file"""
        file_path = os.path.join(self.cwd, "data/capture_confs/config.json")

        with open(file_path, "w") as config_file:
            json.dump(capture_conf, config_file, indent=4)

        print(f"Capture config saved to {file_path}")

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

    def set_baud_rate(self, new_baud_rate):
        """Changes the baud rate dynamically"""
        if self.serial_instance:
            self.serial_instance.baudrate = new_baud_rate
            print(f"Baud Rate Changed to: {new_baud_rate}")

            # Inform the Curve Tracer about the change
            baud_command = f"{new_baud_rate}\r\n"
            self.serial_instance.write(baud_command.encode("utf-8"))

            # Wait for acknowledgment from the Curve Tracer
            while True:
                serial_in = self.serial_instance.readline().decode("utf-8").strip()
                if serial_in == f"Baud Rate Updated: {new_baud_rate}":
                    print("Baud rate change acknowledged.")
                    break

    def save_capture_file(self, capture_data):
        # TODO: save a dict of info into a capture file format.
        file_path = os.path.join(
            self.cwd, "data", "captures",
            f"PV_Capture_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        )

        with open(file_path, "w") as capture_file:
            json.dump(capture_data, capture_file, indent=4)

        print(f"Capture data saved to {file_path}")

    def ok_handshake(self):
        self.serial_instance.write("OK\r\n".encode('utf-8'))
        while True:
            serialIn = self.serial_instance.readline().decode('utf-8').strip()
            print(serialIn)
            if serialIn == "READY_FOR_HANDSHAKE":
                print("Handshake initiated. Sending OK...")
                self.serial_instance.write("OK\r\n".encode("utf-8"))
            if serialIn == "OK_RECEIVED\r\n":
                print("proceed")
                break

    def receive_frontend_command(self, command: str):
        if not self.serial_instance:
            print("ERROR: Serial connection not initialized")
            return
        
        if command.startswith("SET"):
            try:
                voltage = float(command.split(" ")[1])
                formatted_command = f"SET {voltage:.3f}\r\n"
                self.serial_instance.write(formatted_command.encode("utf-8"))
                print(f"Sent voltage command: {formatted_command.strip()}")
            except ValueError:
                print("ERROR: Invalid voltage command format")
        
        elif command == "RESET":
            self.serial_instance.write("RESET\r\n".encode("utf-8"))
            print("Sent RESET command")
            
        elif command.startswith("BAUD"):
            try:
                new_baud_rate = int(command.split(" ")[1])
                if new_baud_rate in self.list_baud_rates():
                    self.set_baud_rate(new_baud_rate)
                else:
                    print(f"ERROR: Unsupported baud rate {new_baud_rate}")
            except ValueError:
                print("ERROR: Invalid baud rate format.")
        
        else:
            print(f"ERROR: Unrecognized command '{command}'")

    def request_capture_conf(self):
        if not self.serial_instance:
            print("ERROR: Serial connection not initialized")
            return
        
        self.serial_instance.write("GET_CAPTURE_CONFIG\r\n".encode("utf-8"))
        
        serial_in = self.serial_instance.readline().decode("utf-8").strip()
        
        try:
            capture_conf = json.loads(serial_in)
            print("Received Capture Config:", capture_conf)
            self.save_capture_config(capture_conf)
        except json.JSONDecodeError:
            print(f"ERROR: Invalid capture config: {serial_in}")

    def capture(self, com_conf, capture_conf):
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
        self.request_capture_conf()
        self.save_capture_config(capture_conf)
        
        read_data = {
            "gate": [],
            "voltage": [],
            "current": [],
            "power": []
        }

        #Open serial connection
        self.serial_instance = serial.Serial(
            com_conf["com_port"],
            com_conf["baud_rate"],
            bytesize=serial.EIGHTBITS,
            parity=com_conf["parity_bit"],
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
        )
        
        #Wait for ready signal
        while True:
            serialIn = self.serial_instance.readline().decode('utf-8').strip()
            print(serialIn)
            if serialIn == "READY_FOR_TRANSMISSION\r\n":
                print("Ready for transmission\n")
                break
        
        #Send handshake
        self.ok_handshake()
        
        while True:
            serial_in = self.serial_instance.readline().decode("utf-8").strip()
            if serial_in == "END_SCAN":
                print("Scan complete")
                break
            try:
                gate, voltage, current, power = map(float, serial_in.split(","))
                data = {
                    "gate": gate,
                    "voltage": voltage,
                    "current": current,
                    "power": power,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                
                read_data["gate"].append(gate)
                read_data["voltage"].append(voltage)
                read_data["current"].append(current)
            
            except ValueError:
                print(f"Invalid data received: {serial_in}")
                
        return read_data
        
"""         baudCheck = True
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
        return read_data """
        
if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")

    controller = PVCurveTracerController()

    com_conf = controller.load_com_config()
    capture_conf = controller.load_capture_config()

    if not com_conf["com_port"]:
        print("No available serial ports detected.")
        sys.exit(1)

    print("Starting Curve Tracer Controller...")
    capture_data = controller.capture(com_conf)
    controller.save_capture_file(capture_data)

