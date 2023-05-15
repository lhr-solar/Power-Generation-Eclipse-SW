"""_summary_
@file       PVCell.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Abstract class representing photovoltaic cell modeling functions.
@version    0.4.0
@date       2023-05-13
"""
import numpy as np
import pandas as pd
import math as m
import random
from scipy.interpolate import interp1d as scipy_interp1d

from PySide6 import QtWidgets
import sys

sys.path.extend([".."])

from common.graph import Graph
from common.utils import update


class PVCell:
    k_b = 1.381e-23  # Boltzmann's constant (J/K).
    q = 1.602e-19  # Electron charge (C).
    NUM_SAMPLES = 300
    BOUNDS_GUARD = 0.0005
    STD = 0.25

    def __init__(self, geometry, parameters) -> None:
        self.geometry = geometry
        self.parameters = parameters

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
                for v in np.arange(0.01, v_oc + 0.01, 0.001)
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
            b = a[a[:,0].argsort()]

            # Get interval indices for the sorted groupby col
            idx = np.flatnonzero(np.r_[True,b[:-1,0]!=b[1:,0],True])

            # Get counts of each group and sum rows based on the groupings & hence averages
            counts = np.diff(idx)
            avg = np.add.reduceat(b[:,1:],idx[:-1],axis=0)/counts.astype(float)[:,None]

            # Finally concatenate for the output in desired format
            return np.c_[b[idx[:-1],0],avg]

        # Sample subset of data
        num_samples = PVCell.NUM_SAMPLES
        if len(data) < num_samples:
            num_samples = len(data)
        data = np.random.permutation(data)[:num_samples]

        # Sort by voltage and delete dups
        data = groupby_mean(data[data[:, 0].argsort()])
        x, y, z = np.transpose(data)

        # Get index of our max power, use associated voltage as our mean
        mpp_idx = z.argmax(axis=0)
        mean = x[mpp_idx]

        # Generate an interolation function
        f_interp = scipy_interp1d(x, y, kind="slinear")
        resolution = PVCell.BOUNDS_GUARD
        interp = np.asarray([
            [sample, f_interp(sample)[()], sample * f_interp(sample)[()]]
            for sample in np.random.normal(mean, PVCell.STD, PVCell.NUM_SAMPLES)
            if sample > min(x) + resolution and sample < max(x) - resolution
        ])

        # Join existing samples with the interpolated samples.
        data = np.concatenate((data, interp), axis=0)
        data = groupby_mean(data[data[:, 0].argsort()])

        return data

    def fit_parameters(self, data, irradiance, temperature):
        # Generate a smaller set of representative points more uniformly
        # distributed across the I-V, P-V curve
        data = PVCell.normalize_data(data)

        # TODO: Two optimizing parameters, irradiance and temperature

        return data, {}

    def get_fill_factor(v_oc, i_sc, v_mpp, i_mpp):
        return (v_mpp * i_mpp) / (v_oc * i_sc)


if __name__ == "__main__":
    random.seed(0)
    # Get a specific cell's fill factor. This should be roughly 0.818.
    fill_factor = PVCell.get_fill_factor(0.721, 6.15, 0.621, 5.84)
    print(fill_factor)

    # Load generic cell.
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

    cell = PVCell(geometry, parameters)

    # Load our target cell, strip the gate column, and convert to [[V, I, P],
    # ...] ndarray format.
    df = pd.read_csv("rp_test.log", header=1)
    df = df.drop(columns=["Gate (V)"])
    data = df.to_numpy()
    norm_data = PVCell.normalize_data(data)

    def plot(data, norm_data):
        data = data.transpose()
        norm_data = norm_data.transpose()
        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()

        win = QtWidgets.QMainWindow()
        win.setGeometry(0, 0, 720, 480)
        win.setWindowTitle("I-V/P-V Sweep")

        # Setup graph
        graph = Graph("PVCell", "Voltage (V)", "Current (A) | Power (W)", use_gl=False)
        graph.set_graph_range([0, 0.65], [0, 3])
        graph.add_series(
            {
                "iv": {"x": data[0], "y": data[1], "color": (0, 255, 0, 10)},
                "pv": {"x": data[0], "y": data[2], "color": (255, 0, 0, 10)},
                "ivn": {"x": norm_data[0], "y": norm_data[1], "color": (255, 0, 0, 255)},
                "pvn": {"x": norm_data[0], "y": norm_data[2], "color": (0, 255, 0, 255)},
            },
            "scatter",
        )

        # Run the application
        win.setCentralWidget(graph.get_graph())
        win.show()
        exe = app.exec()

    plot(data, norm_data)
