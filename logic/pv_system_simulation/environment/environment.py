"""_summary_
@file       environment.py
@author     Matthew Yu (matthewjkyu@gmail.com)
@brief      Models the external environment for the photovoltaics.
@version    0.4.0
@date       2023-05-17
"""
import random
import sys

import numpy as np
import pandas as pd
import pyqtgraph as pg
from PySide6 import QtWidgets

COL_G = "IRRAD (W/m^2)"
COL_T = "TEMP (C)"
FPS = 30


class Environment:
    def __init__(self, env_fp=None, spatial_units="m", temporal_units="s") -> None:
        if env_fp is not None:
            self.df = self.load_env(env_fp)
        else:
            # Default X, Y resolution is in dm, default T resolution is in s
            # Contains dummy frame.
            self.df = pd.DataFrame(
                data={
                    "X": [],
                    "Y": [],
                    "T": [],
                    "IRRAD (W/m^2)": [],
                    "TEMP (C)": [],
                }
            )

        # Represented in numpy ndarray for fast processing
        self.np = self.df.to_numpy()
        self.sp_u = spatial_units
        self.te_u = temporal_units

    def load_env(self, env_fp) -> pd.DataFrame:
        return pd.read_csv(env_fp)
        # return pd.read_csv(env_fp, engine="pyarrow")

    def save_env(self, env_fp) -> None:
        self.df = pd.DataFrame(
            self.np,
            columns=[
                f"X ({self.sp_u})",
                f"Y ({self.sp_u})",
                f"T ({self.te_u})",
                "IRRAD (W/m^2)",
                "TEMP (K)",
            ],
        )
        self.df.to_csv(env_fp, index=None)

    def add_hypervoxel(self, row) -> None:
        self.np = np.vstack((self.np, list(row.values())))

    def add_hypervoxels(self, rows) -> None:
        self.np = np.vstack((self.np, np.array(list(rows.values())).transpose()))

    def generate_hypervoxels(self, func) -> None:
        self.np = np.vstack((self.np, func()))

    def visualize_hypervoxels(self) -> None:
        def get_timeslice(data, timestamp) -> tuple:
            # Reshape by y axis
            indices = np.argwhere(data[:, 2] == timestamp).flatten()
            time_slice = np.take(data, indices, axis=0)

            matrix = time_slice
            matrix_tp = np.transpose(matrix)
            x_max = int(np.max(matrix_tp[0]))
            y_max = int(np.max(matrix_tp[1]))
            x, y = np.mgrid[slice(0, x_max + 1 + 1, 1), slice(0, y_max + 1 + 1, 1)]
            irrad = np.empty((x_max + 1, y_max + 1))
            temp = np.empty((x_max + 1, y_max + 1))

            for hypervoxel in matrix:
                x_idx = int(hypervoxel[0])
                y_idx = int(hypervoxel[1])
                irrad[x_idx, y_idx] = hypervoxel[3]
                temp[x_idx, y_idx] = hypervoxel[4]

            return x, y, irrad, temp

        if not QtWidgets.QApplication.instance():
            app = QtWidgets.QApplication(sys.argv)
        else:
            app = QtWidgets.QApplication.instance()

        win = QtWidgets.QMainWindow()
        win.setGeometry(0, 0, 1080, 480)
        win.setWindowTitle("Environment")

        x, y, irrad, temp = get_timeslice(self.np, 0)

        view = pg.GraphicsLayoutWidget()
        plot_irrad = view.addPlot()
        mesh_irrad = pg.PColorMeshItem(
            x, y, irrad, levels=(0, 1000), enableAutoLevels=False
        )
        plot_irrad.addItem(mesh_irrad, row=0, col=0, rowspan=1, colspan=4)

        plot_temp = view.addPlot()
        mesh_temp = pg.PColorMeshItem(
            x, y, temp, levels=(273.15, 398.15), enableAutoLevels=False
        )
        plot_temp.addItem(mesh_temp)

        def update():
            update.time_idx += 1
            if update.time_idx > update.max_time_idx:
                update.time_idx = 0

            x, y, irrad, temp = get_timeslice(self.np, update.time_idx)
            mesh_irrad.setData(x, y, irrad)
            mesh_temp.setData(x, y, temp)

        update.time_idx = 0
        update.max_time_idx = int(np.max(np.transpose(self.np)[2]))

        timer = pg.QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(1000 / FPS)

        # Run the application
        win.setCentralWidget(view)
        win.show()
        exe = app.exec()


if __name__ == "__main__":
    env = Environment(spatial_units="dm")
    # env.add_hypervoxel({"X": 0, "Y": 0, "T": 0, COL_G: 1000, COL_T: 25})
    # env.add_hypervoxels(
    #     {"X": [0, 0], "Y": [0, 1], "T": [0, 0], COL_G: [1000, 1000], COL_T: [25, 25]}
    # )

    def generator() -> list:
        rows, columns = 25, 40
        time = 500

        matrix_irrad = [
            [100, 100, 200, 200, 300],
            [100, 100, 200, 200, 300],
            [50, 50, 100, 100, 150],
            [50, 50, 100, 100, 150],
            [50, 50, 100, 100, 100],
        ]
        matrix_temp = [
            [298.15, 318.15, 338.15, 338.15, 338.15],
            [298.15, 318.15, 318.15, 338.15, 338.15],
            [298.15, 298.15, 318.15, 338.15, 338.15],
            [298.15, 298.15, 318.15, 318.15, 318.15],
            [298.15, 298.15, 318.15, 318.15, 318.15],
        ]

        def get_irrad(x, y, t):
            irrad = x * y
            return max(0, min(irrad, 1000))

        def get_temp(x, y, t):
            temp = 298.15 + random.gauss(x * y * t / 500, 1)
            return max(273.15, min(temp, 398.15))

        return [
            [x, y, t, get_irrad(x, y, t), get_temp(x, y, t)]
            for t in range(time)
            for y in range(rows)
            for x in range(columns)
        ]

    env.generate_hypervoxels(generator)
    env.visualize_hypervoxels()
    env.save_env("./test.csv")
