import psycopg2
class DatabaseManager:
    """
    DatabaseManager handles logging simulation data into a PostgreSQL database.
    """

    def __init__(self, db_config):
        """
        Initialize connection to PostgreSQL database.

        Parameters
        ----------
        db_config: dict
            A dictionary containing database configuration (host, dbname, user, password).
        """
        self.conn = psycopg2.connect(**db_config)
        self.cursor = self.conn.cursor()

    def setup_tables(self):
        """
        Create necessary tables for logging simulation data.
        """
        table_creation_queries = [
            # Simulation Runs Table
            """
            CREATE TABLE IF NOT EXISTS simulation_runs (
                run_id SERIAL PRIMARY KEY,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """,
            # Source Simulations Table
            """
            CREATE TABLE IF NOT EXISTS source_simulations (
                source_id SERIAL PRIMARY KEY,
                run_id INT NOT NULL,
                cycle_number INT NOT NULL,
                num_cells INT NOT NULL,
                voltage FLOAT NOT NULL,
                irradiance FLOAT NOT NULL,
                temperature FLOAT NOT NULL,
                voc FLOAT NOT NULL,
                isc FLOAT NOT NULL,
                vmp FLOAT NOT NULL,
                imp FLOAT NOT NULL,
                current FLOAT NOT NULL,
                iv_curve TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                FOREIGN KEY (run_id) REFERENCES simulation_runs(run_id)
            );
            """,
            # MPPT Simulations Table
            """
            CREATE TABLE IF NOT EXISTS mppt_simulations (
                mppt_id SERIAL PRIMARY KEY,
                run_id INT NOT NULL,
                cycle_number INT NOT NULL,
                reference_voltage FLOAT NOT NULL,
                pulse_width FLOAT NOT NULL,
                max_cycles INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                FOREIGN KEY (run_id) REFERENCES simulation_runs(run_id)
            );
            """
        ]
        for query in table_creation_queries:
            self.cursor.execute(query)
        self.conn.commit()

    def log_simulation_run(self, description=""):
        """
        Logs a new simulation run.

        Parameters
        ----------
        description: str
            A brief description of the simulation run.

        Returns
        -------
        int
            The generated run_id for this simulation run.
        """
        self.cursor.execute(
            "INSERT INTO simulation_runs (description) VALUES (%s) RETURNING run_id;",
            (description,)
        )
        run_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return run_id

    def log_source_simulation(
        self,
        run_id,
        cycle_number,
        num_cells,
        voltage,
        irradiance,
        temperature,
        voc,
        isc,
        vmp,
        imp,
        current,
        iv_curve,
    ):
        """
        Log data for a single source simulation cycle.

        Parameters
        ----------
        run_id: int
            The ID of the simulation run.
        cycle_number: int
            The simulation cycle number.
        num_cells: int
            Number of cells in the source.
        voltage: float
            Voltage applied to the source.
        irradiance: float
            Irradiance (W/m^2).
        temperature: float
            Temperature (C).
        voc: float
            Open-circuit voltage (V).
        isc: float
            Short-circuit current (A).
        vmp: float
            Voltage at max power (V).
        imp: float
            Current at max power (A).
        current: float
            Output current (A).
        iv_curve: list
            List of voltage-current tuples representing the I-V curve.
        """
        # Serialize the IV curve as a string for storage.
        iv_curve_str = ";".join([f"({v},{i})" for v, i in iv_curve])

        self.cursor.execute(
            """
            INSERT INTO source_simulations (
                run_id, cycle_number, num_cells, voltage, irradiance, temperature,
                voc, isc, vmp, imp, current, iv_curve
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (run_id, cycle_number, num_cells, voltage, irradiance, temperature,
             voc, isc, vmp, imp, current, iv_curve_str),
        )
        self.conn.commit()

    def log_mppt_simulation(
        self,
        run_id,
        cycle_number,
        reference_voltage,
        pulse_width,
        max_cycles
    ):
        """
        Log data for a single MPPT simulation cycle.

        Parameters
        ----------
        run_id: int
            The ID of the simulation run.
        cycle_number: int
            The simulation cycle number.
        reference_voltage: float
            Reference voltage set by MPPT (V).
        pulse_width: float
            Pulse width of the DC-DC converter.
        max_cycles: int
            Maximum number of cycles for this run.
        """
        self.cursor.execute(
            """
            INSERT INTO mppt_simulations (
                run_id, cycle_number, reference_voltage, pulse_width, max_cycles
            ) VALUES (%s, %s, %s, %s, %s);
            """,
            (run_id, cycle_number, reference_voltage, pulse_width, max_cycles),
        )
        self.conn.commit()

    def fetch_source_simulations(self, run_id):
        """
        Fetch all source simulation data for a specific run.

        Parameters
        ----------
        run_id: int
            The ID of the simulation run.

        Returns
        -------
        list
            A list of all source simulations for the specified run.
        """
        self.cursor.execute("SELECT * FROM source_simulations WHERE run_id = %s;", (run_id,))
        return self.cursor.fetchall()

    def fetch_mppt_simulations(self, run_id):
        """
        Fetch all MPPT simulation data for a specific run.

        Parameters
        ----------
        run_id: int
            The ID of the simulation run.

        Returns
        -------
        list
            A list of all MPPT simulation cycles for the specified run.
        """
        self.cursor.execute("SELECT * FROM mppt_simulations WHERE run_id = %s;", (run_id,))
        return self.cursor.fetchall()

    def close_connection(self):
        """
        Closes the database connection.
        """
        self.cursor.close()
        self.conn.close()