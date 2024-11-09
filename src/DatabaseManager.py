import psycopg2
import re
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.file = None
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname="Array Simulation",
                user="connorshen",
                password="postgres",
                host="locahost",
                port=5432
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("Connection Successful")
        except Exception as e:
            print(f"Error: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")

    def create_tables(self):
        # Create PV_Capture table with environmental data arrays
        create_pv_capture_table = """
        CREATE TABLE IF NOT EXISTS PV_Capture (
            capture_id SERIAL PRIMARY KEY,
            pv_id VARCHAR(50) NOT NULL,
            pv_type VARCHAR(50),
            generation_time TIMESTAMP,
            author VARCHAR(100),
            brief TEXT,
            irradiance FLOAT[], -- Array of irradiance values
            temperature FLOAT[], -- Array of temperature values
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        # Create Capture_Data table for voltage and current readings
        create_capture_data_table = """
        CREATE TABLE IF NOT EXISTS Capture_Data (
            data_id SERIAL PRIMARY KEY,
            capture_id INT REFERENCES PV_Capture(capture_id) ON DELETE CASCADE,
            voltage FLOAT,
            current FLOAT
        );
        """
        self.cursor.execute(create_pv_capture_table)
        self.cursor.execute(create_capture_data_table)
        print("Tables created successfully.")

    def add_data(self, file):
        """Parse a .capture file and insert data with environmental arrays into the database."""
        self.file = file
        try:
            with open(self.file, 'r') as file:
                content = file.read()

            # Parse metadata
            metadata_match = re.search(
                r"__version: (.+)\n__file: (.+)\n__brief: (.+)\n__author: (.+)\n__generation_time: (.+)\n__pv_id: (.+)\n__pv_type: (.+)",
                content
            )
            
            if metadata_match:
                version = metadata_match.group(1)
                file_name = metadata_match.group(2)
                brief = metadata_match.group(3)
                author = metadata_match.group(4)
                generation_time = datetime.strptime(metadata_match.group(5), '%Y_%m_%d_%H_%M_%S')
                pv_id = metadata_match.group(6)
                pv_type = metadata_match.group(7)
            else:
                print("Failed to parse metadata.")
                return

            # Parse environmental data arrays (assuming multiple entries for each)
            irradiance_matches = re.findall(r"irradiance \(G\) (\d+)", content)
            temperature_matches = re.findall(r"temperature \(C\) (\d+)", content)
            
            if irradiance_matches and temperature_matches:
                irradiance_array = [float(g) for g in irradiance_matches]
                temperature_array = [float(c) for c in temperature_matches]
            else:
                print("Failed to parse environmental data arrays.")
                return

            # Insert metadata and environmental data as arrays into PV_Capture table
            insert_capture_query = """
            INSERT INTO PV_Capture (pv_id, pv_type, generation_time, author, brief, irradiance, temperature)
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING capture_id;
            """
            self.cursor.execute(insert_capture_query, (pv_id, pv_type, generation_time, author, brief, irradiance_array, temperature_array))
            capture_id = self.cursor.fetchone()[0]

            # Parse test data for voltage and current readings
            data_matches = re.findall(r"(\d+\.\d+),(\d+\.\d+)", content)
            insert_data_query = """
            INSERT INTO Capture_Data (capture_id, voltage, current)
            VALUES (%s, %s, %s);
            """
            for match in data_matches:
                voltage = float(match[0])
                current = float(match[1])
                self.cursor.execute(insert_data_query, (capture_id, voltage, current))

            print(f"Inserted capture data from file with capture_id {capture_id}.")

        except Exception as e:
            print(f"Error processing file: {e}")

# Usage example
if __name__ == "__main__":
    db_manager = DatabaseManager(
        dbname="Array Simulation",
        user="connorshen",
        password="postgres",
        host="localhost",
        port=5432
    )

    db_manager.connect()
    db_manager.create_tables()

    # Insert data from a .capture file
    db_manager.add_data()

    db_manager.close()
