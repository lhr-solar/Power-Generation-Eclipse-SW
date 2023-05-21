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
    df = pd.read_csv("photovoltaic/rp_test.log", header=1)
    df = df.drop(columns=["Gate (V)"])
    data = df.to_numpy()

    # Extract the cell parameters
    norm_data, fitting_parameters = cell.fit_parameters(data)
    print(fitting_parameters)
    predicted_data = cell.get_voltage_curves(
        fitting_parameters["irradiance"]["val"],
        fitting_parameters["temperature"]["val"],
    )

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
                "ivn": {
                    "x": norm_data[0],
                    "y": norm_data[1],
                    "color": (255, 0, 0, 150),
                },
                "pvn": {
                    "x": norm_data[0],
                    "y": norm_data[2],
                    "color": (0, 255, 0, 150),
                },
                "ivn": {
                    "x": predicted_data[0],
                    "y": predicted_data[1],
                    "color": (255, 0, 0, 255),
                },
                "pvn": {
                    "x": predicted_data[0],
                    "y": predicted_data[2],
                    "color": (0, 255, 0, 255),
                },
            },
            "scatter",
        )

        # Run the application
        win.setCentralWidget(graph.get_graph())
        win.show()
        exe = app.exec()

    plot(data, norm_data, predicted_data)
