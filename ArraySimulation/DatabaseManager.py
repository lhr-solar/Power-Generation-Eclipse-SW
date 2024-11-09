import psycopg2
from psycopg2.extras import Json
from datetime import datetime
class DatabaseManager:
    def __init__(self, host, port, dbname, user, password):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()
        
    def fetch_metadata(self, metadata_id, table):
        query = f"""
            SELECT config, description, timestamp
            FROM {table}
            WHERE id = %s
        """
        self.cursor.execute(query, (metadata_id,))
        row = self.cursor.fetchone()

        if not row:
            raise ValueError(f"No metadata found with ID {metadata_id} in table {table}")

        return {
            "config": row[0],
            "description": row[1],
            "timestamp": row[2]
        }

    # --- Source Simulator Methods ---
    def insert_source_metadata(self, config, description=""):
        query = """
            INSERT INTO source_simulation_metadata (config, description)
            VALUES (%s, %s) RETURNING id
        """
        self.cursor.execute(query, (Json(config), description))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def insert_source_result(self, voltage, current, power, temperature, sunlight, metadata_id):
        query = """
            INSERT INTO source_simulation_results (timestamp, voltage, current, power, temperature, sunlight, metadata_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (datetime.now(), voltage, current, power, temperature, sunlight, metadata_id))
        self.connection.commit()

    def fetch_source_results(self, metadata_id):
        query = """
            SELECT * FROM source_simulation_results WHERE metadata_id = %s
        """
        self.cursor.execute(query, (metadata_id,))
        return self.cursor.fetchall()

    # --- MPPT Simulator Methods ---
    def insert_mppt_metadata(self, config, description=""):
        query = """
            INSERT INTO mppt_simulation_metadata (config, description)
            VALUES (%s, %s) RETURNING id
        """
        self.cursor.execute(query, (Json(config), description))
        self.connection.commit()
        return self.cursor.fetchone()[0]

    def insert_mppt_result(self, voltage, current, power, mppt_algorithm, step, metadata_id):
        query = """
            INSERT INTO mppt_simulation_results (timestamp, voltage, current, power, mppt_algorithm, step, metadata_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (datetime.now(), voltage, current, power, mppt_algorithm, step, metadata_id))
        self.connection.commit()

    def fetch_mppt_results(self, metadata_id):
        query = """
            SELECT * FROM mppt_simulation_results WHERE metadata_id = %s
        """
        self.cursor.execute(query, (metadata_id,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
