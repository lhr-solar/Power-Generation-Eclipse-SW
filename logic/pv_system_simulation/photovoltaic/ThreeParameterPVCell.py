"""_summary_
@file       ThreeParameterPVCell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Concrete class modeling the single diode model
@version    0.4.0
@date       2023-05-13
"""
from PVCell import PVCell
import math as m
import pyqtgraph as pg
import numpy as np

from PySide6 import QtWidgets
import sys
import pandas as pd
from lmfit import Parameters, fit_report, minimize
import similaritymeasures

sys.path.extend([".."])

from common.graph import Graph


class ThreeParameterPVCell(PVCell):
    def __init__(self, geometry, parameters) -> None:
        super().__init__(geometry, parameters)

    def get_current(self, voltage, irradiance, temperature):
        if voltage == 0.0:
            raise Exception("Load voltage is too low!")
        if irradiance == 0.0:
            raise Exception("Incident irradiance is too low!")
        if temperature == 0.0:
            raise Exception("Cell temperature is too low!")

        g_ref = self.parameters["reference_irrad"]
        t_ref = self.parameters["reference_temp"]
        v_oc_ref = self.parameters["reference_voc"]
        i_sc_ref = self.parameters["reference_isc"]
        n = self.parameters["ideality_factor"]

        if n == 0.0:
            raise Exception("Cell ideality factor is too low!")

        g = irradiance
        t = temperature
        v = voltage

        # Thermal voltage
        v_t = n * PVCell.k_b * t / PVCell.q  # 26mV

        # Short circuit current
        i_sc = i_sc_ref * g / g_ref

        # Open circuit voltage
        v_oc = v_oc_ref + v_t * m.log(g / g_ref + 1)

        # Dark/reverse saturation current
        i_0 = i_sc / (m.exp(v_oc / v_t) - 1)

        # Dark/diode current
        i_d = i_0 * (m.exp(v / v_t) - 1)

        # Photocurrent
        i_pv = i_sc

        # Load current
        i_l = i_pv - i_d

        return i_l

    def fit_parameters(self, data, irradiance, temperature):
        data, params = super().fit_parameters(data, irradiance, temperature)

        params["ideality_factor"] = 0

        # One optimizing parameter (N)
        fit_params = Parameters()
        fit_params.add("ideality_factor", value=1.5 * 1e-7, min=0.1 * 1e-7, max=2.5 * 1e-7)

        # Optimize based on the procruste's distance for all points
        def residual(params, data, irradiance, temperature, self):
            values = params.valuesdict()
            self.parameters["ideality_factor"] = values["ideality_factor"] * 1e7
            print(values["ideality_factor"] * 1e7)

            # Generate an arbitrary amount of points
            points = self.get_voltage_curves(irradiance, temperature)
            # Match the size of either
            if len(data) > len(points):
                data = np.random.permutation(data)[:len(points)]
            elif len(data) < len(points):
                points = np.random.permutation(points)[:len(data)]

            # Compare similarity
            mae = similaritymeasures.mae(data, points)
            return mae

        res = minimize(
            residual,
            fit_params,
            args=(data, irradiance, temperature, self),
            method="powell",
        )

        self.parameters["ideality_factor"] = res.params["ideality_factor"].value * 1e7
        print(fit_report(res))
        print(self.parameters["ideality_factor"])

        return data, self.parameters["ideality_factor"]

if __name__ == "__main__":
    geometry = {
        "cell_width": 0.125,  # Meters
        "cell_length": 0.125,  # Meters
        "cell_area": 0.0153,  # Meters ^ 2
    }

    parameters = {
        "reference_irrad": 1000,  # Watts per Meters ^ 2
        "reference_temp": 298.15,  # Kelvin
        "reference_voc": 0.721,  # Volts
        "reference_isc": 6.15,  # Amps
        "ideality_factor": 1.70,
    }

    # Instantiate a new Cell under this model.
    cell = ThreeParameterPVCell(geometry, parameters)

    # Get the current of a solar cell of a specific load voltage, irradiance,
    # and temperature.

    # Ideally this is at 5.84 A, the I_MPP of this particular cell.
    current = cell.get_current(0.621, 1000, 298.15)
    print(current)

    # This should be a numpy array, consisting of three columns: cell load
    # voltage, output current, and output power.
    curves = cell.get_voltage_curves(1000, 298.15)

    # This should consist of two sets of data: the expected V_OC and I_SC for
    # this particular irradiance and temperature, and the MPP conditions. We
    # note that the MPP conditions differ from expected (0.621 V, 5.84 A)! This
    # is partly because the datasheet has some error, and that despite tuning
    # the ideality parameter, our model is not quite accurate.
    edge = cell.get_edge_characteristics(1000, 298.15)
    print(edge)

    # Here are examples demonstrating how to sweep across various cell
    # parameters, in particular, the ideality factor, the incident irradiance,
    # and the cell temperature. This uses the custom graph widget and pyqtgraph
    # timers.

    def run(update_func):
        global graph

        # Do not create a new instance if it exists
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()

        win = QtWidgets.QMainWindow()
        win.setGeometry(0, 0, 720, 480)
        win.setWindowTitle("I-V/P-V Sweep")

        # Setup graph
        graph = Graph(
            "ThreeParameterPVCell",
            "Voltage (V)",
            "Current (A) | Power (W)",
            use_gl=False,
        )
        # With target keypoints
        graph.add_series(
            {
                "I_MPP": {"x": [0.621], "y": [5.84], "color": (0, 255, 0)},
                "P_MPP": {"x": [0.621], "y": [3.63], "color": (255, 0, 0)},
            },
            "scatter",
        )
        graph.set_graph_range([0, 0.721], [0, 6.15])

        # Set the first iteration.
        geometry = {
            "cell_width": 0.125,  # Meters
            "cell_length": 0.125,  # Meters
            "cell_area": 0.0153,  # Meters ^ 2
        }

        parameters = {
            "reference_irrad": 1000,  # Watts per Meters ^ 2
            "reference_temp": 298.15,  # Kelvin
            "reference_voc": 0.721,  # Volts
            "reference_isc": 6.15,  # Amps
            "ideality_factor": 1.70,
        }
        cell = ThreeParameterPVCell(geometry, parameters)
        data = cell.get_voltage_curves(1000, 298.15)
        data = data.transpose()
        graph.add_series(
            {
                "iv": {"x": data[0], "y": data[1], "color": (0, 255, 0)},
                "pv": {"x": data[0], "y": data[2], "color": (255, 0, 0)},
            },
            "line",
        )

        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update_func)
        timer.start(25)

        # Run the application
        win.setCentralWidget(graph.get_graph())
        win.show()
        exe = app.exec()

    def ideality_factor_sweep():
        # Sweep the graph at different ideality factors.
        ideality_factor_sweep.i += 0.005
        if ideality_factor_sweep.i > 2.0:
            ideality_factor_sweep.i = 1.0

        parameters["ideality_factor"] = ideality_factor_sweep.i
        cell = ThreeParameterPVCell(geometry, parameters)
        data = cell.get_voltage_curves(1000, 298.15)
        data = data.transpose()
        graph.update_series(
            {
                "iv": {
                    "x": data[0],
                    "y": data[1],
                },
                "pv": {
                    "x": data[0],
                    "y": data[2],
                },
            },
        )

    ideality_factor_sweep.i = 1.0

    def irradiance_sweep():
        # Sweep the graph at different irradiances.
        irradiance_sweep.i += 2.5
        if irradiance_sweep.i > 1050:
            irradiance_sweep.i = 50

        cell = ThreeParameterPVCell(geometry, parameters)
        data = cell.get_voltage_curves(irradiance_sweep.i, 298.15)
        data = data.transpose()
        graph.update_series(
            {
                "iv": {
                    "x": data[0],
                    "y": data[1],
                },
                "pv": {
                    "x": data[0],
                    "y": data[2],
                },
            },
        )

    irradiance_sweep.i = 50

    def temperature_sweep():
        # Sweep the graph at different temperatures.
        temperature_sweep.i += 1
        if temperature_sweep.i > 398.15:
            temperature_sweep.i = 248.15

        cell = ThreeParameterPVCell(geometry, parameters)
        data = cell.get_voltage_curves(1000, temperature_sweep.i)
        data = data.transpose()
        graph.update_series(
            {
                "iv": {
                    "x": data[0],
                    "y": data[1],
                },
                "pv": {
                    "x": data[0],
                    "y": data[2],
                },
            },
        )

    temperature_sweep.i = 248.15

    # run(ideality_factor_sweep)
    # run(irradiance_sweep)
    # run(temperature_sweep)

    # Reinitialize cell
    geometry = {
        "cell_width": 0.125,  # Meters
        "cell_length": 0.125,  # Meters
        "cell_area": 0.0153,  # Meters ^ 2
    }

    parameters = {
        "reference_irrad": 1000,  # Watts per Meters ^ 2
        "reference_temp": 298.15,  # Kelvin
        "reference_voc": 0.59,  # Volts
        "reference_isc": 6.15,  # Amps
        "ideality_factor": 2.46,
    }

    # Instantiate a new Cell under this model.
    cell = ThreeParameterPVCell(geometry, parameters)

    # Load our target cell, strip the gate column, and convert to [[V, I, P],
    # ...] ndarray format.
    df = pd.read_csv("rp_test.log", header=1)
    df = df.drop(columns=["Gate (V)"])
    data = df.to_numpy()

    # Extract the cell parameters
    norm_data, _ = cell.fit_parameters(data, 375, 298.15)
    predicted_data = cell.get_voltage_curves(375, 298.15)

    def plot(data, norm_data, predicted_data):
        data = data.transpose()
        norm_data = norm_data.transpose()
        predicted_data = predicted_data.transpose()

        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()

        win = QtWidgets.QMainWindow()
        win.setGeometry(0, 0, 720, 480)
        win.setWindowTitle("I-V/P-V Sweep")

        # Setup graph
        graph = Graph("PVCell", "Voltage (V)", "Current (A) | Power (W)", use_gl=False)
        graph.set_graph_range([0, 0.721], [0, 6.15])
        graph.add_series(
            {
                "iv": {"x": data[0], "y": data[1], "color": (255, 0, 0, 10)},
                "pv": {"x": data[0], "y": data[2], "color": (0, 255, 0, 10)},
                "ivn": {"x": norm_data[0], "y": norm_data[1], "color": (255, 0, 0, 100)},
                "pvn": {"x": norm_data[0], "y": norm_data[2], "color": (0, 255, 0, 100)},
                "ivn": {"x": predicted_data[0], "y": predicted_data[1], "color": (255, 0, 0, 255)},
                "pvn": {"x": predicted_data[0], "y": predicted_data[2], "color": (0, 255, 0, 255)},
            },
            "scatter",
        )

        # Run the application
        win.setCentralWidget(graph.get_graph())
        win.show()
        exe = app.exec()

    plot(data, norm_data, predicted_data)
