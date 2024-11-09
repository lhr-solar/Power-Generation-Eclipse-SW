import psycopg2
from psycopg2.extras import Json
from datetime import datetime

class DatabaseManager:
    def __init__(self, host, port, dbname, user, password):
        """
        Initialize the DatabaseManager with connection parameters.
        """
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()

    def insert_simulation_metadata(self, config, description=""):
        """
        Insert simulation metadata into the database.
        
        Args:
            config (dict): Simulation configuration as a dictionary.
            description (str): Optional description of the simulation.
        
        Returns:
            int: The ID of the inserted metadata row.
        """
        query = """
            INSERT INTO simulation_metadata (config, description)
            VALUES (%s, %s) RETURNING id
        """
        self.cursor.execute(query, (Json(config), description))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def insert_simulation_result(self, voltage, current, power, mppt_algorithm, simulation_id):
        """
        Insert simulation result into the database.
        
        Args:
            voltage (float): The voltage value.
            current (float): The current value.
            power (float): The power value.
            mppt_algorithm (str): The MPPT algorithm used.
            simulation_id (int): The ID of the simulation metadata row.
        """
        query = """
            INSERT INTO simulation_results (timestamp, voltage, current, power, mppt_algorithm, simulation_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (datetime.now(), voltage, current, power, mppt_algorithm, simulation_id))
        self.connection.commit()

    def fetch_simulation_results(self, simulation_id):
        """
        Fetch all results for a specific simulation.
        
        Args:
            simulation_id (int): The ID of the simulation metadata row.
        
        Returns:
            list: A list of rows containing simulation results.
        """
        query = """
            SELECT * FROM simulation_results WHERE simulation_id = %s
        """
        self.cursor.execute(query, (simulation_id,))
        return self.cursor.fetchall()

    def log_error(self, error_message):
        """
        Log an error message into the error_logs table.
        
        Args:
            error_message (str): The error message to log.
        """
        query = """
            INSERT INTO error_logs (timestamp, error_message)
            VALUES (%s, %s)
        """
        self.cursor.execute(query, (datetime.now(), error_message))
        self.connection.commit()

    def close(self):
        """
        Close the database connection.
        """
        self.cursor.close()
        self.connection.close()
