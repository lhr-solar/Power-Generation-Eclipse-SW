"""_summary_
@file       pv_curve_tracer_controller.py
@author     Roy Mor () and Matthew Yu (matthewjkyu@gmail.com)
@brief      Talks to the PV Curve Tracer.
@version    0.0.1
@data       2022-09-22
"""

from curses import baudrate
import serial
import argparse
from datetime import datetime


class PVCurveTracerController:
    def __init__(self) -> None:
        self.serial_instance = None
        self.file_hook = None

    def list_ports(self):
        return serial.tools.list_ports.comports()

    def connect_to_curve_tracer(self, com_port, baud_rate, parity):
        self.serial_instance = serial.Serial(
            port=com_port, baudrate=baud_rate, parity=parity
        )

    def hook_in_file(self, file_name):
        if self.file_hook is not None:
            self.file_hook.close()
        self.file_hook = open(
            f"{file_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log", "w+"
        )

    def send_command(self, command_str):
        if self.file_hook is not None:
            self.file_hook.write(f"{command_str}\n")
        self.serial_instance.write(f"{command_str}\n")

    def receive_data(self):
        data = self.serial_instance.readline().decode("utf-8").strip()
        if self.file_hook is not None:
            self.file_hook.write(f"{data}\n")
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("port", type=str, help="port to read from")
    args = parser.parse_args()
    port = args.port

    controller = PVCurveTracerController()
    controller.connect_to_curve_tracer(
        com_port=port, baud_rate=115200, parity=serial.PARITY_NONE
    )
    while True:
        file_name = input("Specify cell ID then press ENTER:")
        controller.hook_in_file(file_name)
        line = controller.receive_data()
        while line != "TERMINATE SCAN MODE":
            line = controller.receive_data()
            print(line)
        print("Done reading file!")
        input("Press [ENTER] to continue...")
