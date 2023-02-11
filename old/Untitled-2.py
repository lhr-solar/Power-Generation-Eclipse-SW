
        def go(self):
            """_summary_
            Loads in characterization data for the PV.

            Returns:
                [False, str]: An error and an error string
                [True, dict]: A success and data corresponding to the characterized PV in the form:
                    {
                        "irradiance": float,
                        "temperature": float,
                        "voltage":  [float],
                        "current":  [float],
                        "power":    [float],
                        "v_oc":     float,
                        "i_sc":     float,
                        "v_mpp":    float,
                        "i_mpp":    float,
                        "p_mpp":    float,
                        "ff":       float,
                        "eff":      float
                    }
            """
            # Pressing the GO button.
            if (
                self.test_data_instance["file_path"] is not None
                and self.test_data_instance["loader"] is not None
                and self.test_data_instance["data"] is not None
            ):
                self.parent.print("LOG", "Characterizing data...")

                # Calculate characteristics
                data = self.parent.pv_char.characterize_data(
                    self.test_data_instance["data"]
                )
                return [True, data]

            elif (
                self.curve_tracer_instance["com_port"] is not None
                and self.curve_tracer_instance["baud_rate"] is not None
                and self.curve_tracer_instance["pv_type"] is not None
                and self.curve_tracer_instance["pv_id"] is not None
            ):
                self.parent.print("LOG", "Communicating with PV Curve Tracer...")
                # Open serial port
                # Send command
                # Wait for data to be transmitted
                # Load I-V, P-V Curve data
                # Calculate characteristics
                # Save into file
                # Return stuff
                return [False, "UNIMPLEMENTED"]
            else:
                return [False, "Nothing can be run."]

        def reset(self):
            """_summary_
            Resets characterization data for the PV.

            Returns:
                dict: An empty data dict corresponding to a nonexistent PV in the same format as go.
            """
            self.test_data_instance = {"file_path": None, "loader": None, "data": None}
            self.curve_tracer_instance = {
                "com_port": None,
                "baud_rate": None,
                "pv_type": None,
                "pv_id": None,
            }

            return {
                "irradiance": 0.00,
                "temperature": 0.00,
                "voltage": [],
                "current": [],
                "power": [],
                "v_oc": 0.00,
                "i_sc": 0.00,
                "v_mpp": 0.00,
                "i_mpp": 0.00,
                "p_mpp": 0.00,
                "ff": 0.00,
                "eff": 0.00,
            }

        def get_available_com_ports(self):
            """_summary_
            Returns a list of currently connected COM ports.

            Returns:
                [str]: Port Names.
            """
            port_options = ["-"]
            ports = QSerialPortInfo().availablePorts()
            if len(ports) != 0:
                port_options.extend([port.portName() for port in ports])
            return port_options

        def set_com_port(self, com_port):
            """_summary_
            Sets the current COM port of the device.

            Args:
                com_port (str): The com port to set.
            """
            self.curve_tracer_instance["com_port"] = com_port

        def get_available_baud_rates(self):
            """_summary_
            Returns a list of baud rates for talking to the device.

            Returns:
                [str]: Baud rates.
            """
            baud_options = ["-"]
            bauds = QSerialPortInfo().standardBaudRates()
            baud_options.extend([str(baud) for baud in bauds])
            return baud_options

        def set_baud_rate(self, baud_rate):
            """_summary_
            Sets the current baud rate of the device.

            Args:
                baud_rate (str): The baud rate to set.
            """
            self.curve_tracer_instance["baud_rate"] = baud_rate

        def get_available_pv_types(self):
            """_summary_
            Returns a list of PV types that the device could measure.

            Returns:
                [str]: List of PV types
            """
            return ["Cell", "Module", "Array"]

        def set_pv_type(self, pv_type):
            """_summary_
            Sets the current PV type that the device is measuring.

            Args:
                pv_type (str): The PV type to measure.
            """
            self.curve_tracer_instance["pv_type"] = pv_type

        def set_pv_id(self, id):
            """_summary_
            Sets the ID representing the PV to be tested. This is used later for
            generating a characterization file.

            Args:
                id (str): ID of the PV tested.

            Returns:
                bool: Whether the ID is valid. It could fail based on the following reasons:
                - The file already exists.
                - The name has spaces in it.
            """
            self.curve_tracer_instance["pv_id"] = id
            # Check if a file under this name already exists.
            return True

        def load_pv_char_file(self, file_path):
            """_summary_
            Load a historical PV characterization file. Select the
            correct loader associated with the file version and load in the file contents.

            Args:
                file_path (str): File to load.
            """
            self.parent.print(
                "LOG", f"Loading PV characterization file at {file_path}..."
            )
            [result, loader_or_err] = self.parent.pv_char.get_version_loader_from_path(
                file_path
            )

            if result is False:
                self.parent.print("ERROR", loader_or_err)
            else:
                self.test_data_instance["file_path"] = file_path
                self.test_data_instance["loader"] = loader_or_err
                self.parent.print(
                    "LOG", "Found valid loader version, extracting file..."
                )
                self.test_data_instance["data"] = loader_or_err.load_file(file_path)
                self.parent.print("LOG", "Loaded in data.")

        def save_pv_char_file(self):
            """_summary_
            Save a PV characterization into a file.
            """
            self.curve_tracer_instance["loader"].store_file(
                f"./data/{self.curve_tracer_instance['pv_id']}.log",
                self.curve_tracer_instance["data"],
            )

        def normalize_data(self, data):
            """_summary_
            Normalize the PV data to 25 C and 1000 W/m^2.

            Args:
                data Data to normalize.

            Returns:
                dict: data corresponding to the characterized PV in the form:
                    {
                        "irradiance": float,
                        "temperature": float,
                        "voltage":  [float],
                        "current":  [float],
                        "power":    [float],
                        "v_oc":     float,
                        "i_sc":     float,
                        "v_mpp":    float,
                        "i_mpp":    float,
                        "p_mpp":    float,
                        "ff":       float,
                        "eff":      float
                    }
            """
            return self.parent.pv_char.normalize_data(data)

        def get_available_pv_models(self):
            """_summary_
            Returns a list of PV models that can be compared against the PV
            characterization data.

            Returns:
                [str]: List of PV models.
            """
            return self.parent.pv_model.list_models()

        def load_pv_model(self, model_name):
            """_summary_
            Sets the current PV model to be compared against the PV
            characterization data.

            Args:
                pv_model (str): Model name.
            """
            self.parent.print("LOG", f"Loading PV Model {model_name}...")
            [result, model_or_err] = self.parent.pv_model.get_model(model_name)

            if result is False:
                self.parent.print("ERROR", model_or_err)
            else:
                self.model_instance["pv_model"] = model_or_err
                self.model_instance["data"] = model_or_err.generate_model()
                self.parent.print("LOG", "Loaded in data.")
            return self.model_instance["data"]

        # Analyze Data Against Others
        def set_test_data_file_range(self, range):
            # Check to see if some subset of files exist under the range specifier
            self.data_set = None
            return False

        def get_analysis(self, test_data):
            # Return several things:
            #    - A headline number indicating the percentile of the cell
            #      to the set. This may be calculated arbitrarily.
            #    - A Fill Factor distribution [bin_size in %, [array of a PMF],
            #      index our PV data is associated with].
            #    - A P_MPP distribution [bin_size in mW, [array of a PMF],
            #      index our PV data is associated with].
            #    - I-V curve set (ordered array for each PV in the test set,
            #      against the test_data).
            return None

        def publish_pv_models(self, pv_model_selector):
            pass
            # print(self.parent.ui)#update_pv_model_selector(pv_model_selector, self.get_available_pv_models())
