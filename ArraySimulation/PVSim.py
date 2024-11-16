"""
PVSim.py

Author: Matthew Yu, Array Lead (2020).
Contact: matthewjkyu@gmail.com
Created: 11/17/20
Last Modified: 11/24/20

Description: The PVSim file is the entry point to the application. It
coordinates the data pipeline and display output and allows users to provide
input commands.

The data pipeline looks something like the following:

              PVEnvironment                                 PVSource
      Generates a Source Definition     --->      Ingests the Source Definition
    for the current simulation cycle.           and spits out IV characteristics.

                   ^                                           |
                   |                                           V
    
         Advance the cycle time                               MPPT
     and feed new setpoint voltage                Intakes IV characteristics to
        into the PVEnvironment.                 determine a new setpoint voltage.
                                                
                   ^                                           |
                   |                                           V
                   |
                   |                                    DC-DC Converter
                   .-------------------         Takes the setpoint voltage and
                                             does the appropriate power balancing.


                                    Application
                                       /   \
                                      /     \
                                     /       \
                                    /         \
                                   /           \
                                  /             \
                                 /               \
                UI Controller                       Data Controller
            The controller manages the      The data controller captures data
            visual display of data for      output across the above data
            the models. Internal widgets    pipeline and stores it in objects
            call functions in the data      retrievable by the controller.
            controller to activate the      It also exposes a command API
            pipeline.                       that UI objects in the controller
                                            can call to stimulate the pipeline.
"""
# Library Imports.
import sys

sys.path.append("../")

# Custom Imports.
from ArraySimulation.Controller.UIController import UIController
from ArraySimulation.DatabaseManager import DatabaseManager

if __name__ == "__main__":
    if sys.version_info[0] < 3:
        raise Exception("This program only supports Python 3.")
    
    # Database configuration
    db_config = {
        'host': 'localhost',
        'dbname': 'ArraySimulation',
        'user': 'connorshen',
        'password': 'postgres'
    }

    # Initialize DatabaseManager
    db_manager = DatabaseManager(db_config)
    db_manager.setup_tables()

    # Start a new simulation run
    run_id = db_manager.log_simulation_run(description=input("Describe the Conditions of the Simulation"))

    # Initialize the UIController
    try:
        controller = UIController(db_manager=db_manager, run_id=run_id)
        controller.startup()
    finally:
        # Ensure the database connection is closed
        db_manager.close_connection()
