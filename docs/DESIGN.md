# DESIGN README

Eclipse consists of four, semi-connected modules:

- PV Capture
- PV Characterization
- Sim Designer
- Power Gen Sim

## PV Capture

PV Capture is a module that allows for the capture and visualization of
different photovoltaics (PVs).

### PV Capture Functionality

1. Define the type of photovoltaic that will be captured by the application.
   We specify the following:
   1. The type of photovoltaic that will be measured (CELL [0-1V], MODULE
      [0-10V], ARRAY [0-100V]). This determines some predetermined test
      parameters, which can be adjusted:
      1. The sample range [0 - 1, in increments of .001]
      2. The step size [0 - 1, in increments of .001]
      3. The number of sample iterations
      4. The settling time per sample

   Given these parameters, we can determine the following:

   - The number of steps (range / step size)
   - The total number of samples collected (num steps * num iterations)
   - The duration of the experiment (total samples * settling time)
2. Define the configuration that is used to interface with the PV Curve Tracer
   PCB to perform PV capture. We specify the following:
   1. COM port
   2. baud rate
   3. parity bit
   4. encoding scheme
3. Define the name of the photovoltaic in order to later generate a capture
   file.
4. Interact with the PV Curve Tracer board to perform a capture. This involves
   checking whether the communication scheme is valid, configuring the Curve
   Tracer, and receiving data from the Curve Tracer until an end point is
   reached.
5. Validate, filter, plot, and characterize Curve Tracer results. The module
   should parse the results from the Curve Tracer, plot it on the GUI, and
   update a board listing characterization results including but limited to
   `V_OC`, `I_SC`, `V_MPP`, `I_MPP`, `P_MPP`, and `FF`. It should also generate
   a best fit curve for the data as data points are being added.
6. Generate a capture file when a valid capture has been obtained.
7. Save an image of the current GUI canvas on demand.

## PV Characterization

PV Characterization is a module that allows for the comparison and modelling of
different PVs.

### PV Characterization Functionality

1. Specify a model or PV (object) to be loaded onto the canvas. The following
   should be specifiable:
   1. A model, either a cached file or class name using the interface defined by
      PVModel
   2. A capture file generated from the PV Capture module
   3. A set of capture files generated from the PV Capture module or equivalent

   The module should support different versions of capture file, as defined by
   the PVCapture class.
2. Clear all objects from the GUI canvas on demand.
3. Save an image of the current GUI canvas on demand.
4. Update a table of characterization results when an object has been loaded.
5. Update a set of distributions including, but not limited to the fill factor
   and p_mpp. Clicking on an entry in the table should highlight the particular
   object in the distribution and plots.
6. Have a "normalize irrad & temp" checkbox or button that temporarily modifies
   the object to match standard conditions (1000 G and 25 C).

## Simulation Designer

The simulation designer allows for the creation of PV arrays from building
blocks. It also allows for the creation of environmental profiles (irradiance,
temperature, load) over a specified time scale.

### Simulation Designer Functionality

1. Define the name of the simulation that should be created. Or load from file a
   given simulation project file.
2. Specify, add, and move a module around the canvas. The module should specify
   the following:
   1. Bypass diode model used (if any)
   2. The cell model used for simulation
   3. The number of cells in the module
   4. The efficiency/FF of the module
3. Alternatively, specify a layout that auto-adds modules to the canvas in a
   specific pattern.
4. Clicking on a module (this could be from the canvas or from a table) should
   update a sub-display specifying environmental conditions such as irradiance,
   temperature, and so on.
5. An image representing the load can also update the load voltage at various
   points of time.


## Power Generation Simulator

### Power Generation Simulator Functionality
