
            main_layout = QGridLayout()
            self.setLayout(main_layout)

            [
                widget_new_pv,
                [
                    self.com_port_selector,
                    self.baud_rate_selector,
                    self.pv_type_selector,
                    self.pv_id_input,
                ],
            ] = self.add_sublayout_pull_data()
            main_layout.addWidget(widget_new_pv, 0, 0, 16, 34)

            [widget_load_pv, self.file_selector] = self.add_sublayout_load_data()
            main_layout.addWidget(widget_load_pv, 0, 34, 16, 16)

            [
                widget_char_pv,
                [self.v_oc, self.i_sc, self.v_mpp, self.i_mpp, self.p_mpp, self.ff],
            ] = self.add_sublayout_char_data()
            main_layout.addWidget(widget_char_pv, 16, 0, 16, 50)

            [
                widget_compare_pv,
                [self.pv_model_selector],
            ] = self.add_sublayout_compare_pv()
            main_layout.addWidget(widget_compare_pv, 32, 0, 10, 50)

            [
                widget_analyze_pv,
                [self.name_range_specifier, self.percentile_display],
            ] = self.add_sublayout_analyze_pv()
            main_layout.addWidget(widget_analyze_pv, 42, 0, 10, 50)

            [widget_console, [self.console]] = self.add_sublayout_console()
            main_layout.addWidget(widget_console, 52, 0, 12, 50)

            [
                widget_display,
                [self.iv_curve, self.ff_dist, self.pmpp_dist, self.iv_curve_ranked],
            ] = self.add_sublayout_graphs()
            main_layout.addWidget(widget_display, 0, 50, 64, 70)

            self.load_selector(
                self.com_port_selector, self.parent.data.get_available_com_ports()
            )
            self.load_selector(
                self.baud_rate_selector, self.parent.data.get_available_baud_rates()
            )
            self.load_selector(
                self.pv_type_selector, self.parent.data.get_available_pv_types()
            )
            self.load_selector(
                self.pv_model_selector, self.parent.data.get_available_pv_models()
            )

        def add_sublayout_pull_data(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Pull Data From Curve Tracer")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout_com_port = QFormLayout()
            com_port_label = QLabel("COM Port")
            com_port_selector = QComboBox()
            com_port_selector.addItem("NULL")
            layout_com_port.addRow(com_port_label, com_port_selector)

            layout_baud_rate = QFormLayout()
            baud_rate_label = QLabel("Baud Rate")
            baud_rate_selector = QComboBox()
            layout_baud_rate.addRow(baud_rate_label, baud_rate_selector)

            layout_pv_type = QFormLayout()
            pv_type_label = QLabel("PV Type")
            pv_type_selector = QComboBox()
            layout_pv_type.addRow(pv_type_label, pv_type_selector)

            layout_id = QFormLayout()
            id_label = QLabel("PV ID")
            id_input = QLineEdit()
            id_input.setPlaceholderText("cell_rp001")
            layout_id.addRow(id_label, id_input)
            # TODO: 09_15_2022 Deal with validator, verify cell exists.

            layout_display.addWidget(title, 0, 0, 1, 2)
            layout_display.addLayout(layout_com_port, 1, 0, 1, 1)
            layout_display.addLayout(layout_baud_rate, 2, 0, 1, 1)
            layout_display.addLayout(layout_pv_type, 1, 1, 1, 1)
            layout_display.addLayout(layout_id, 2, 1, 1, 1)

            display.setLayout(layout_display)

            return [
                display,
                [com_port_selector, baud_rate_selector, pv_type_selector, id_input],
            ]

        def add_sublayout_load_data(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Load Test Data From File")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            file_selector = QPushButton("Select PV Log File")
            file_selector.clicked.connect(self.get_test_data_file_from_dialog)

            layout_display.addWidget(title, 0, 0, 1, 1)
            layout_display.addWidget(file_selector, 1, 0, 2, 1)

            display.setLayout(layout_display)

            return [display, file_selector]

        def add_sublayout_char_data(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Characterize Data")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            v_oc = QLabel("V_OC = 0.00V")
            v_oc.setAlignment(Qt.AlignmentFlag.AlignCenter)

            i_sc = QLabel("I_SC = 0.00A")
            i_sc.setAlignment(Qt.AlignmentFlag.AlignCenter)

            v_mpp = QLabel("V_MPP = 0.00V")
            v_mpp.setAlignment(Qt.AlignmentFlag.AlignCenter)

            i_mpp = QLabel("I_MPP = 0.00A")
            i_mpp.setAlignment(Qt.AlignmentFlag.AlignCenter)

            p_mpp = QLabel("P_MPP = 0.00W")
            p_mpp.setAlignment(Qt.AlignmentFlag.AlignCenter)

            ff = QLabel("FF = 0.00%")
            ff.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout_display.addWidget(title, 0, 0, 1, 3)
            layout_display.addWidget(v_oc, 1, 0, 1, 1)
            layout_display.addWidget(i_sc, 2, 0, 1, 1)
            layout_display.addWidget(v_mpp, 1, 1, 1, 1)
            layout_display.addWidget(i_mpp, 2, 1, 1, 1)
            layout_display.addWidget(p_mpp, 1, 2, 1, 1)
            layout_display.addWidget(ff, 2, 2, 1, 1)

            display.setLayout(layout_display)

            return [display, [v_oc, i_sc, v_mpp, i_mpp, p_mpp, ff]]

        def add_sublayout_compare_pv(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Compare Against Model")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout_pv_model = QFormLayout()
            pv_model_label = QLabel("PV Model Type")
            pv_model_selector = QComboBox()
            layout_pv_model.addRow(pv_model_label, pv_model_selector)

            normalize_iv_curve_button = QPushButton(
                "Normalize irradiance and temperature"
            )
            normalize_iv_curve_button.clicked.connect(self.normalize_data)
            superimpose_iv_curve_button = QPushButton("Superimpose on Curve")
            superimpose_iv_curve_button.clicked.connect(self.superimpose_model)

            layout_display.addWidget(title, 0, 0, 1, 3)
            layout_display.addLayout(layout_pv_model, 1, 0, 1, 1)
            layout_display.addWidget(normalize_iv_curve_button, 1, 1, 1, 1)
            layout_display.addWidget(superimpose_iv_curve_button, 1, 2, 1, 1)

            display.setLayout(layout_display)

            return [display, [pv_model_selector]]

        def add_sublayout_analyze_pv(self):
            display = QFrame()
            layout_display = QGridLayout()

            title = QLabel("Analyze Data Against Others")
            title.setAlignment(Qt.AlignmentFlag.AlignCenter)

            layout_name_range = QFormLayout()
            name_range_label = QLabel("PV Range")
            name_range_specifier = QLineEdit()
            layout_name_range.addRow(name_range_label, name_range_specifier)
            name_range_label.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            name_range_specifier.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            percentile_display = QLabel("Top 0.00% Percentile")
            percentile_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
            percentile_display.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            display_dist_button = QPushButton("Display Distribution")
            display_dist_button.clicked.connect(self.set_ranking_display)
            display_dist_button.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )

            layout_display.addWidget(title, 0, 0, 1, 3)
            layout_display.addLayout(layout_name_range, 1, 0, 1, 1)
            layout_display.addWidget(percentile_display, 1, 1, 1, 1)
            layout_display.addWidget(display_dist_button, 1, 2, 1, 1)

            display.setLayout(layout_display)

            return [display, [name_range_specifier, percentile_display]]

        def add_sublayout_console(self):
            display = QFrame()
            layout_display = QGridLayout()

            # Left widget is the status console
            status_console = QTextEdit()
            status_console.setReadOnly(True)

            # Right widget is a pair of buttons, GO and RESET
            go_button = QPushButton("GO")
            go_button.setStyleSheet("background-color: green")
            go_button.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            go_button.clicked.connect(self.generate_data)

            reset_button = QPushButton("RESET")
            reset_button.setStyleSheet("background-color: red")
            reset_button.setSizePolicy(
                QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            )
            reset_button.clicked.connect(self.reset_data)

            layout_display.addWidget(status_console, 0, 0, 2, 8)
            layout_display.addWidget(go_button, 0, 8, 1, 3)
            layout_display.addWidget(reset_button, 1, 8, 1, 3)

            display.setLayout(layout_display)

            return [display, [status_console]]

        def set_ranking_display(self):
            self.display.setCurrentIndex(1)

        def add_sublayout_graphs(self):
            display = QFrame()
            layout_display = QStackedLayout()

            # Top page is graph_iv_curve
            top_display, [iv_curve] = self.add_subwindow_graph_iv_curve()

            # Next page is a gridlayout of other graphs
            bottom_display, [
                ff_dist,
                pmpp_dist,
                iv_curve_ranked,
            ] = self.add_subwindow_graph_ranking()

            layout_display.addWidget(top_display)
            layout_display.addWidget(bottom_display)

            display.setLayout(layout_display)

            return [display, [iv_curve, ff_dist, pmpp_dist, iv_curve_ranked]]

        def add_subwindow_graph_iv_curve(self):
            # Wrap the widget around the layout which holds the plot widget :)
            parent_widget = QWidget()
            layout = QVBoxLayout()
            iv_curve = pg.PlotWidget()
            iv_curve.setTitle("I-V Characteristics")
            iv_curve.setLabel("left", "Current (A)")
            iv_curve.setLabel("bottom", "Voltage (V)")
            iv_curve.setLabel("right", "Power (W)")
            iv_curve.showGrid(x=True, y=True)
            layout.addWidget(iv_curve)
            parent_widget.setLayout(layout)
            return [parent_widget, [iv_curve]]

        def add_subwindow_graph_ranking(self):
            # Wrap the widget around the layout which holds the plot widgets :)
            parent_widget = QWidget()
            layout = QGridLayout()
            ff_dist = pg.PlotWidget()
            pmpp_dist = pg.PlotWidget()
            iv_curve = pg.PlotWidget()
            layout.addWidget(ff_dist, 0, 0, 1, 1)
            layout.addWidget(pmpp_dist, 0, 1, 1, 1)
            layout.addWidget(iv_curve, 1, 0, 1, 2)
            parent_widget.setLayout(layout)
            return [parent_widget, [ff_dist, pmpp_dist, iv_curve]]

        def load_selector(self, selector_widget, items):
            selector_widget.clear()
            for item in items:
                selector_widget.addItem(item)

        def get_selector_value(self, selector_widget):
            return selector_widget.currentText()

        def populate_field(self, widget, text):
            widget.setText(text)

        def print_console(self, text):
            self.console.append(text)

        def get_test_data_file_from_dialog(self):
            file_path = QFileDialog.getOpenFileName(self, "Open File:", "./", "")
            self.file_path = file_path
            # TODO: Update button with new text
            # self.file_selector.setText(file_path)

        def generate_data(self):
            # Run data generation function
            self.parent.print("LOG", "Starting Eclipse PV Capture execution...")

            # Load data from sublayout_pull_data
            device_selection = {
                "com_port": self.com_port_selector.currentText(),
                "baud_rate": self.baud_rate_selector.currentText(),
                "pv_type": self.pv_type_selector.currentText(),
                "pv_id": self.id_input.text()
            }

            file_selection = {
                "file_path": self.file_path

            }
            print(device_selection)

            [success, data] = self.parent.data.go()
            if success:
                self.parent.print("LOG", "Plotting data on main canvas...")
                self.plot_graph_iv_curve(data)
                self.parent.print("LOG", "Updating labels...")
                self.update_char_data_fields(data)
                self.parent.print("LOG", "Done!")
            else:
                self.parent.print("LOG", data)

        def normalize_data(self):
            # TODO: Get data from parent
            self.parent.print("LOG", "Normalizing data...")
            data = self.parent.data.normalize_data(data)
            self.parent.print("LOG", "Updating display...")
            self.clear_graph_iv_curve()
            self.plot_graph_iv_curve(data)
            self.parent.print("LOG", "Done!")

        def superimpose_model(self):
            data = self.parent.data.load_pv_model(self.pv_model_selector.currentText())
            self.parent.print("LOG", "Plotting data on main canvas...")
            self.plot_graph_iv_curve(data)
            self.parent.print("LOG", "Done!")

        def update_char_data_fields(self, data):
            self.populate_field(self.v_oc, f"V_OC = {data['v_oc']:.2f} V")
            self.populate_field(self.i_sc, f"I_SC = {data['i_sc']:.2f} A")
            self.populate_field(self.v_mpp, f"V_MPP = {data['v_mpp']:.2f} V")
            self.populate_field(self.i_mpp, f"I_MPP = {data['i_mpp']:.2f} A")
            self.populate_field(self.p_mpp, f"P_MPP = {data['p_mpp']:.2f} W")
            self.populate_field(self.ff, f"FF = {data['ff']*100:.2f} %")

        def plot_graph_iv_curve(self, data):
            pen_iv = pg.mkPen(color=(0, 0, 255), width=3)
            pen_pv = pg.mkPen(color=(255, 0, 0), width=3)
            self.iv_curve.plot(data["voltage"], data["current"], pen=pen_iv, symbol="t")
            self.iv_curve.plot(data["voltage"], data["power"], pen=pen_pv, symbol="t1")

        def clear_graph_iv_curve(self):
            self.iv_curve.clear()

        def reset_data(self):
            self.parent.print("LOG", "Resetting the display...")
            data = self.parent.data.reset()
            self.parent.print("LOG", "Clearing data on main canvas...")
            self.clear_graph_iv_curve()
            self.parent.print("LOG", "Updating labels...")
            self.update_char_data_fields(data)
            self.parent.print("LOG", "Done!")
