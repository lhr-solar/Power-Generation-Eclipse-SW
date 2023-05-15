import pandas as pd
import numpy as np
import random
import sys
from perlin_noise import PerlinNoise
import pyqtgraph as pg

from PySide6 import QtWidgets
from common.graph import Graph

COL_G = "IRRAD (W/m^2)"
COL_T = "TEMP (C)"

class Environment:
    def __init__(self, env_fp=None, spatial_units="mm", temporal_units="s") -> None:
        if env_fp is not None:
            self.df = self.load_env(env_fp)
        else:
            # Default X, Y resolution is in dm, default T resolution is in s
            # Contains dummy frame.
            self.df = pd.DataFrame(
                data={
                    "X": [np.nan],
                    "Y": [np.nan],
                    "T": [np.nan],
                    "IRRAD (W/m^2)": [np.nan],
                    "TEMP (C)": [np.nan],
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
            self.np, columns=["X", "Y", "T", "IRRAD (W/m^2)", "TEMP (C)"]
        )
        self.df.to_csv(env_fp, index=None)

    def add_hypervoxel(self, row) -> None:
        self.np = np.vstack((self.np, list(row.values())))

    def add_hypervoxels(self, rows) -> None:
        self.np = np.vstack((self.np, np.array(list(rows.values())).transpose()))

    def generate_hypervoxels(self, func) -> None:
        self.np = np.vstack((self.np, func()))

    def visualize_hypervoxels(self, image_fp=None) -> None:
        # Setup application window
        app = QtWidgets.QApplication()
        win = QtWidgets.QMainWindow()
        win.setGeometry(0, 0, 720, 480)
        win.setWindowTitle("Environment")

        def get_voxel_slice(data, timestamp, interest_idx) -> tuple:
            # Reshape by y axis
            indices = np.argwhere(data[:, 2] == timestamp).flatten()
            slice = np.take(data, indices, axis=0)
            slice = slice[:, [0, 1, interest_idx]]  # Look at irradiance data
            return slice

        slice = get_voxel_slice(self.np, 0, 4)

        # Generate the graph and apply it
        graph = Graph.Graph("Environment", "X (m)", "Y (m)", use_gl=True)
        graph.add_series(
            {
                "irradiance": {
                    "voxels": slice,
                    "colormap": pg.colormap.get("CET_L3", source="colorcet"),
                    "size": 5
                }
            },
            "3dscatter"
        )

        # Run the application
        win.setCentralWidget(graph.get_graph())
        win.show()
        exe = app.exec()


if __name__ == "__main__":
    # TODO: bug loading in existing csv
    env = Environment()
    # env.add_hypervoxel({"X": 0, "Y": 0, "T": 0, COL_G: 1000, COL_T: 25})
    # env.add_hypervoxels(
    #     {"X": [0, 0], "Y": [0, 1], "T": [0, 0], COL_G: [1000, 1000], COL_T: [25, 25]}
    # )

    def generator() -> list:
        noise = PerlinNoise(octaves=5, seed=1)
        rows, columns = 1000, 1000
        time = 1

        def get_irrad(x, y, t):
            # Gets stronger as we go east, fluctuate over time
            return 1.0 #noise([y / rows, x / columns, t / time]) * 1000

        def get_temp(x, y, t):
            return random.gauss(10, 5)

        return [
            [x, y, t, get_irrad(x, y, t), get_temp(x, y, t)]
            for t in range(time)
            for y in range(columns)
            for x in range(rows)
        ]

    # print(min(timeit.Timer(generator).repeat(3, 10))/10)
    env.generate_hypervoxels(generator)
    env.visualize_hypervoxels()
    # env.save_env("./test.csv")
