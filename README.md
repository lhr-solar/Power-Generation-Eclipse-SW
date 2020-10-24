# Array Simulator

Created on 5/24/20 by Matthew Yu, Solar Array Lead (2020) of the UT Solar Vehicles Team.

This repository contains an in-development simulation of various components of the solar array subsystems, including the following:

- Solar Array
- DC-DC Converter
- MPPT
- Load (Kinda)

Additionally, this simulator also can simulate the source properties of solar cells.

---

## Python Source and MPPT Simulator

To install dependencies, run `pip3 install -r requirements.txt`.
To run the MPPT Simulator, call `python3 main.py`.
To run the Solar cell model Simulator, call `python3 source_main.py`.

---

## Dependencies

Install these dependencies or use the requirements.txt to install.
- python3
- sys
- matplotlib
- numpy
- bisect
- math
- pyqtgraph

Install dependencies using `pip3 install -r requirements.txt`

---

## Using the Simulator

After installing dependencies, run the main application with the following command:
`python3 main.py`

You can also run the source simulator with the following command:
`python3 source_main.py`

---

## Papers and sites I haven't used yet but are promising

[Modeling Solar Cells](https://sites.google.com/site/banuphotovoltaic/pv/pv-arrays)

[Irradiance and PV Performance Optimization](e-education.psu.edu/ae868/node/877)

[Factors affecting PV Performance](file:///home/matthew/Downloads/FactorsAffectingPVperformance.pdf)

[Maxeon Gen II Solar Cells](file:///home/matthew/Documents/Uni/UTSVT/sp-gen3-solar-cell-ds-en-a4-160-507816f.pdf)

[Exploration of MPPT Algorithms](https://web.wpi.edu/Pubs/E-project/Available/E-project-030617-131157/unrestricted/AN_EXPLORATION_OF_MAXIMUM_POWER_POINT_TRACKING_ALGORITHMS.pdf)

[PandO with confined search space](https://www.sciencedirect.com/science/article/pii/S101836391730380X)

[PandO](http://www.actapress.com/Abstract.aspx?paperId=23133)

[Analysis and Optimization of maximum power point tracking algorithms in the presence of noise (Latham et al.)](https://cpb-us-e1.wpmucdn.com/sites.dartmouth.edu/dist/f/1307/files/2017/06/Analysis-and-Optimization-of-Maximum-Power-Point-Tracking-Algorithms-in-the-Presence-of-Noise-qc3ej8.pdf)

[Gradient Descent, possibly on power transformation](https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote07.html)

[A new maximum power point control algorithm of photovoltaic generation system (Bian et al.)](https://www.tandfonline.com/doi/full/10.1080/21642583.2018.1558419)

[On global extrmum seeking in the presence of local extrema](https://www-sciencedirect-com.ezproxy.lib.utexas.edu/science/article/pii/S0005109808004147)

[Advances in solar photovoltaic power plants (Islam et al.)](https://books.google.com/books?id=nPh6DAAAQBAJ&pg=PA91&lpg=PA91&dq=discrete+newton+method+mppt&source=bl&ots=qXRTL0UCqg&sig=ACfU3U2qzhM4SR83wCpQYoiPg1QgVhoQ-g&hl=en&sa=X&ved=2ahUKEwjjt6W69dnpAhUJa80KHVs1ACkQ6AEwB3oECAwQAQ#v=onepage&q=discrete%20newton%20method%20mppt&f=false)

[Accurate Simulation of MPPT Methods Performance When Applied to Commercial Photovoltaic Panels (Cubas et al.)](https://www.hindawi.com/journals/tswj/2015/914212/)
