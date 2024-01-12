"""_summary_
@file       PVCell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Abstract class representing photovoltaic cell modeling functions.
@version    0.4.0
@date       2023-05-17
"""
import math as m
import random
import sys

import numpy as np
import pandas as pd
import pyqtgraph as pg
from lmfit import Parameters, fit_report, minimize
from PySide6 import QtWidgets
from scipy.interpolate import interp1d as scipy_interp1d

sys.path.extend(["."])

from common.graph import Graph
from common.utils import update


class PVCell:
    k_b = 1.381e-23  # Boltzmann's constant (J/K).
    q = 1.602e-19  # Electron charge (C).
    NUM_SAMPLES = 500
    BOUNDS_GUARD = 0.0005
    STD = 0.1

    def __init__(self, geometry, parameters, cell_data_fp=None) -> None:
        self.geometry = geometry
        self.parameters = parameters
        self.data = None

        if cell_data_fp is not None:
            self.load_file(cell_data_fp)

    def load_file(self, cell_data_fp):
        # Load our target cell, strip the gate column, and convert to [[V,
        # I, P], ...] ndarray format.
        df = pd.read_csv(cell_data_fp, header=1)
        df = df.drop(columns=["Gate (V)"])
        self.data = df.to_numpy()

    def get_current(self, voltage, irradiance, temperature):
        raise NotImplementedError

    def get_voltage_curves(self, irradiance, temperature):
        g_ref = self.parameters["reference_irrad"]
        v_oc_ref = self.parameters["reference_voc"]
        n = self.parameters["ideality_factor"]

        g = irradiance
        t = temperature

        # Thermal voltage
        v_t = n * PVCell.k_b * t / PVCell.q  # 26mV

        # Predicted VOC at our particular irrad and temp
        v_oc = v_oc_ref + v_t * m.log(g / g_ref + 1)

        points = np.asarray(
            [
                [v, self.get_current(v, g, t), v * self.get_current(v, g, t)]
                for v in np.arange(0.01, v_oc + 0.01, 0.005)
            ]
        )

        df = pd.DataFrame(points, columns=["Voltage (V)", "Current (A)", "Power (W)"])

        # Filter out only valid 1st quadrant entries
        df = df[(df["Current (A)"] >= 0.0)]

        return df.to_numpy()

    def get_edge_characteristics(self, irradiance, temperature):
        points = self.get_voltage_curves(irradiance, temperature)
        df = pd.DataFrame(points, columns=["Voltage (V)", "Current (A)", "Power (W)"])

        v_oc = df.nlargest(1, "Voltage (V)").iloc[0]["Voltage (V)"]
        i_sc = df.nlargest(1, "Current (A)").iloc[0]["Current (A)"]

        mpp = df.nlargest(1, "Power (W)")
        v_mpp = mpp.iloc[0]["Voltage (V)"]
        i_mpp = mpp.iloc[0]["Current (A)"]
        p_mpp = mpp.iloc[0]["Power (W)"]

        return (v_oc, i_sc), (v_mpp, i_mpp, p_mpp)

    def get_parameters(self):
        return self.parameters

    def update_parameters(self, parameters):
        self.parameters = update(self.parameters, parameters)

    def normalize_data(data):
        def groupby_mean(a):
            # Sort array by groupby column
            b = a[a[:, 0].argsort()]

            # Get interval indices for the sorted groupby col
            idx = np.flatnonzero(np.r_[True, b[:-1, 0] != b[1:, 0], True])

            # Get counts of each group and sum rows based on the groupings & hence averages
            counts = np.diff(idx)
            avg = (
                np.add.reduceat(b[:, 1:], idx[:-1], axis=0)
                / counts.astype(float)[:, None]
            )

            # Finally concatenate for the output in desired format
            return np.c_[b[idx[:-1], 0], avg]

        # Sort by voltage and delete dups
        data = groupby_mean(data[data[:, 0].argsort()])

        # Sample subset of data
        num_samples = PVCell.NUM_SAMPLES
        if len(data) < num_samples:
            num_samples = len(data)
        data = np.random.permutation(data)[:num_samples]

        # x, y, z = np.transpose(data)

        # # Get index of our max power, use associated voltage as our mean
        # mpp_idx = z.argmax(axis=0)
        # mean = x[mpp_idx]

        # # Generate an interolation function
        # f_interp = scipy_interp1d(x, y, kind="slinear")
        # resolution = PVCell.BOUNDS_GUARD
        # interp = np.asarray(
        #     [
        #         [sample, f_interp(sample)[()], sample * f_interp(sample)[()]]
        #         for sample in np.random.normal(mean, PVCell.STD, PVCell.NUM_SAMPLES)
        #         if sample > min(x) + resolution and sample < max(x) - resolution
        #     ]
        # )

        # # Join existing samples with the interpolated samples.
        # data = np.concatenate((data, interp), axis=0)
        # data = groupby_mean(data[data[:, 0].argsort()])

        return data

    def _set_params_and_fit(self, data, fitting_parameters, residual):
        optimizer_parameters = Parameters()
        for key, value in fitting_parameters.items():
            if value["given"]:
                optimizer_parameters.add(
                    key,
                    min=value["min"] * 1e-7,
                    value=value["val"] * 1e-7,
                    max=value["max"] * 1e-7,
                    vary=False,
                )
            else:
                optimizer_parameters.add(
                    key,
                    min=value["min"] * 1e-7,
                    value=value["stc"] * 1e-7,
                    max=value["max"] * 1e-7,
                    vary=True,
                )

        res = minimize(
            residual,
            optimizer_parameters,
            args=(data, self),
            method="powell",
        )
        print(fit_report(res))

        for key, value in fitting_parameters.items():
            value["val"] = res.params[key].value * 1e7

        return fitting_parameters

    def fit_parameters(self, data, irradiance=None, temperature=None):
        # Generate a smaller set of representative points more uniformly
        # distributed across the I-V, P-V curve
        data = PVCell.normalize_data(data)

        fitting_parameters = {
            "irradiance": {
                "min": 100,
                "stc": 1000,
                "max": 1100,
                "val": irradiance,
                "given": irradiance is not None,
            },
            "temperature": {
                "min": 273.15,
                "stc": 298.15,
                "max": 398.15,
                "val": temperature,
                "given": temperature is not None,
            },
        }

        return data, fitting_parameters

    def get_fill_factor(v_oc, i_sc, v_mpp, i_mpp):
        return (v_mpp * i_mpp) / (v_oc * i_sc)

    def visualize_cell(self, irradiance, temperature, cell_data_fp=None):
        if cell_data_fp is not None:
            self.load_file(cell_data_fp)

        data = self.data
        if data is None:
            raise Exception("No data file has been set!")
        norm_data = None
        pred_data = None
        try:
            norm_data = PVCell.normalize_data(data)
            norm_data = np.transpose(norm_data)
            pred_data = self.get_voltage_curves(irradiance, temperature)
            pred_data = np.transpose(pred_data)
        except:
            pass
        finally:
            data = np.transpose(data)

            if not QtWidgets.QApplication.instance():
                app = QtWidgets.QApplication(sys.argv)
            else:
                app = QtWidgets.QApplication.instance()

            win = QtWidgets.QMainWindow()
            win.setGeometry(0, 0, 720, 480)
            win.setWindowTitle("I-V/P-V Sweep")

            # Setup graph
            graph = Graph(
                "PVCell", "Voltage (V)", "Current (A) | Power (W)", use_gl=False
            )
            graph.add_series(
                {
                    "IV Data (A)": {
                        "x": data[0],
                        "y": data[1],
                        "color": (255, 0, 0, 10),
                    },
                    "PV Data (W)": {
                        "x": data[0],
                        "y": data[2],
                        "color": (0, 255, 0, 10),
                    },
                },
                "scatter",
            )

            if norm_data is not None:
                graph.add_series(
                    {
                        "IV Norm Data (A)": {
                            "x": norm_data[0],
                            "y": norm_data[1],
                            "color": (255, 0, 0, 200),
                        },
                        "PV Norm Data (W)": {
                            "x": norm_data[0],
                            "y": norm_data[2],
                            "color": (0, 255, 0, 200),
                        },
                    },
                    "scatter",
                )

            if pred_data is not None:
                graph.add_series(
                    {
                        "IV Pred Data (A)": {
                            "x": pred_data[0],
                            "y": pred_data[1],
                            "color": (255, 0, 0, 255),
                        },
                        "PV Pred Data (W)": {
                            "x": pred_data[0],
                            "y": pred_data[2],
                            "color": (0, 255, 0, 255),
                        },
                    },
                    "line",
                )

            # Run the application
            win.setCentralWidget(graph.get_graph())
            win.show()
            exe = app.exec()

    def visualize_sweep(
        self,
        graphs=None,
        ref=None,
        irradiance_range=None,
        temperature_range=None,
        return_widget=False,
    ):
        def init_graph(container_layout, graph, ref):
            graph["graph"] = Graph(
                graph["title"], "Voltage (V)", "Current (A) | Power (W)", use_gl=False
            )
            if ref is not None:
                # With target keypoints
                graph["graph"].add_series(
                    {
                        "I_MPP": {
                            "x": [ref["v_mpp"]],
                            "y": [ref["i_mpp"]],
                            "color": (0, 255, 0),
                        },
                        "P_MPP": {
                            "x": [ref["v_mpp"]],
                            "y": [ref["p_mpp"]],
                            "color": (255, 0, 0),
                        },
                    },
                    "scatter",
                )
                graph["graph"].set_graph_range(
                    ref["v_range"],
                    [
                        min(ref["i_range"][0], ref["p_range"][0]),
                        max(ref["i_range"][1], ref["p_range"][1]),
                    ],
                )

            # Set the first iteration
            data = self.get_voltage_curves(1000, 298.15)
            data = np.transpose(data)
            graph["graph"].add_series(
                {
                    "iv": {"x": data[0], "y": data[1], "color": (0, 255, 0)},
                    "pv": {"x": data[0], "y": data[2], "color": (255, 0, 0)},
                },
                "line",
            )

            container_layout.addWidget(graph["graph"].get_graph(), *graph["position"])

        def update_graphs():
            for key, graph in self._graphs.items():
                if key == "IRRAD_SWEEP":
                    data = self.get_voltage_curves(graph["cur_val"], 298.15)
                elif key == "TEMP_SWEEP":
                    data = self.get_voltage_curves(1000, graph["cur_val"])
                else:
                    self.parameters[key] = graph["cur_val"]
                    data = self.get_voltage_curves(1000, 298.15)

                data = data.transpose()
                graph["graph"].update_series(
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

                graph["cur_val"] += graph["range"][2]
                if graph["cur_val"] > graph["range"][1]:
                    graph["cur_val"] = graph["range"][0]

        if graphs is None:
            graphs = {}
        graphs["IRRAD_SWEEP"] = {
            "title": "Irradiance Sweep (W/m^2)",
            "widget": None,
            "range": [250, 1250, 10],
            "cur_val": 250,
            "position": [0, 0],
        }
        graphs["TEMP_SWEEP"] = {
            "title": "Temperature Sweep (K)",
            "widget": None,
            "range": [273.15, 398.15, 0.1],
            "cur_val": 298.15,
            "position": [0, 1],
        }

        if irradiance_range is not None:
            graphs["IRRAD_SWEEP"]["range"] = irradiance_range
        if temperature_range is not None:
            graphs["TEMP_SWEEP"]["range"] = temperature_range

        self._graphs = graphs

        container = QtWidgets.QWidget()
        container_layout = QtWidgets.QGridLayout()
        container.setLayout(container_layout)

        # Add all widgets
        for graph in graphs.values():
            init_graph(container_layout, graph, ref)

        # Setup timer for updating graphs
        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update_graphs)

        if return_widget:
            return container, timer
        else:
            if not QtWidgets.QApplication.instance():
                app = QtWidgets.QApplication(sys.argv)
            else:
                app = QtWidgets.QApplication.instance()

            win = QtWidgets.QMainWindow()
            win.setGeometry(0, 0, 1920, 1080)
            win.setWindowTitle("I-V/P-V Sweep")
            win.setCentralWidget(container)

            timer.start(100)

            # Run the application
            win.show()
            exe = app.exec()


if __name__ == "__main__":
    random.seed(0)
    # Get a specific cell's fill factor. This should be roughly 0.818.
    fill_factor = PVCell.get_fill_factor(0.721, 6.15, 0.621, 5.84)
    print(fill_factor)

    # Load generic cell.
    cell = PVCell(None, None, cell_data_fp="photovoltaic/rp_test.log")
    cell.visualize_cell(1000, 298.15)
