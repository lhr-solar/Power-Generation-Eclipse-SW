"""
Author: Matthew Yu
Last Modified: 10/14/20
Organization: UTSVT Solar Array Subteam
File Description:
This is a visualization of the solution space to the surface constraint problem.
We have a set of modules where the current for each module can be modeled very
loosely given the voltage as V^2 + I^2 = 1 (1st quadrant of the unit circle).
We find the list of N-dimensional coordinate candidates that match the following
constraint functions:

F(V1, V2, ..., Vn) = V1 + V2 + ... + Vn = V_total
Additionally, Vk <= V_max.

In layman terms, we want to find the set of solutions where the individual
voltages sum to V_total and visualize their minimum current output (the reason
being that a set of modules in series is current limited by the worst module).
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import math
import constraint # https://stackabuse.com/constraint-programming-with-python-constraint/

pg.setConfigOptions(  # TODO: set to white background with black text
    antialias=True,
    background=pg.mkColor(0, 0, 0),
    foreground=pg.mkColor(255, 255, 255),
)

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.resize(800,800)
view = pg.GraphicsLayoutWidget(border=(100, 100, 100))
mw.setCentralWidget(view)
mw.show()
mw.setWindowTitle("Module Surface Visualization")

# 1 Module
# w1 = view.addPlot()
# w1.setLimits(xMin=0, xMax=1, yMin=0, yMax=1)
# s1 = pg.ScatterPlotItem(
#     size=3,
#     pen=pg.mkPen(None),
#     brush=pg.mkBrush(255, 255, 255, 120)
# )
# 2 Modules
w2 = view.addPlot()
w2.setLimits(xMin=0, xMax=1, yMin=0, yMax=1)
s2 = pg.ScatterPlotItem(
    size=3,
    pen=pg.mkPen(None),
    brush=pg.mkBrush(255, 255, 255, 120)
)
# 3 Modules
# w3 = view.addPlot()
# w3.setLimits(xMin=.3, xMax=.72, yMin=.3, yMax=.72)
# s3 = pg.ScatterPlotItem(
#     size=5,
#     pen=pg.mkPen(None),
#     brush=pg.mkBrush(255, 255, 255, 120)
# )

"""
1st Plot. a 2D graph representing the min current as a function
of ONE independent module voltage.
Voltage range is constrained by the constraint function.
"""
# # Main Generation Code
# points_x    = []
# points_y    = []
# points_mag  = []

# # Independent axis constraint
# problem = constraint.Problem()
# v_total = 1
# v_max = 1
# resolution = .01
# problem.addVariable('x', np.arange(0.0, v_total, resolution))

# def constraint_func_1(x):
#     if x <= v_total and x <= v_max:
#         return True

# problem.addConstraint(constraint_func_1, ['x'])
# solutions = problem.getSolutions()

# # Print solutions and add them to the graph
# print("Single Module Candidates")
# for index, solution in enumerate(solutions):
#     # We can do a simple model of the IV curve as X^2 + Y^2 = 1.
#     points_x.append(solution['x'])
#     current = math.sqrt(1 - solution['x']**2)
#     points_y.append(current)
#     points_mag.append(10)
#     # print("Candidate: ({}) = {}".format(
#     #     round(solution['x'], 2),
#     #     round(current, 2))
#     # )


# # Wrapping up the points and throwing them into the scatter plot.
# points = []
# zip_points = list(zip(points_x, points_y, points_mag))
# for item in zip_points:
#     points.append(
#         {'pos': [item[0], item[1]], 'data': item[2], 'size': item[2]}
#     )


"""
2nd Plot. A 2D graph representing the min current as a function
of TWO independent module voltages.
The color of the points represent the current magnitude.
Voltage range is constrained by the constraint function.
"""
# Main Generation Code
points_x    = []
points_y    = []
points_mag  = []

# Independent axis constraint
problem_2 = constraint.Problem()
v_total = 1.0           # Voltage applied over the entire series
v_max = .8              # Max voltage per cell
v1_scaling = .75          # Effective voltage of cell 1
v2_scaling = 1          # Effective voltage of cell 2
resolution_digits = 3.0 # Step resolution per cell voltage
error = 1/(10**resolution_digits) # modify the numerator to adjust error proportion

problem_2.addVariable('x1', np.arange(0.0, v_max*v1_scaling, 1/(10**resolution_digits)))
problem_2.addVariable('x2', np.arange(0.0, v_max*v2_scaling, 1/(10**resolution_digits)))

def constraint_func_2(x1, x2):
    x1 = round(x1, math.ceil(resolution_digits))
    x2 = round(x2, math.ceil(resolution_digits))
    if ((x1 + x2) <= v_total*(1+error) and (x1 + x2) >= v_total*(1-error)):
        return True

problem_2.addConstraint(constraint_func_2, ['x1', 'x2'])
solutions = problem_2.getSolutions()

# Print solutions and add them to the graph
print("2 Module Candidates")
for index, solution in enumerate(solutions):
    points_x.append(solution['x1'])
    points_y.append(solution['x2'])
    # We can do a simple model of the IV curve as X^2 + Y^2 = 1.
    # This time, we take the minimum of the two modules.
    current = min(
        math.sqrt(v_max**2*v1_scaling - solution['x1']**2),
        math.sqrt(v_max**2*v2_scaling - solution['x2']**2)
    )
    points_mag.append(current)

    # print("Candidate: ({},{}) = {}".format(
    #     round(solution['x1'], 2),
    #     round(solution['x2'], 2),
    #     round(current, 2))
    # )

# Filter out solutions for the best one(s).
m = max(points_mag)
max_pos = [i for i, j in enumerate(points_mag) if j == m]
for pos in max_pos:
    print("Best candidate: ({},{}) = {}".format(
        round(points_x[pos], math.ceil(resolution_digits)),
        round(points_y[pos], math.ceil(resolution_digits)),
        round(points_mag[pos], math.ceil(resolution_digits))
    ))

# Wrapping up the points and throwing them into the scatter plot.
points_2 = []
zip_points = zip(points_x, points_y, points_mag)
for item in zip_points:
    points_2.append({
        'pos': [item[0], item[1]],
        'data': item[2],
        'pen': pg.mkPen(
            (122, 0, item[2]*255),
            width=5
        )
    })


"""
3rd Plot. A 2D graph (with 3 overlapping datasets) representing the min
current as a function of THREE independent module voltages.
The color of the points represent the current magnitude and the two
axes represent a subset of the 3 independent modules.
Voltage range is constrained by the constraint function.
"""
# Main Generation Code
# points_x    = []
# points_y    = []
# points_z    = []
# points_mag  = []

# # Independent axis constraint
# problem_3 = constraint.Problem()
# v_total = 1.8
# v_max = .72
# resolution = .01
# problem_3.addVariable('x1', np.arange(0.0, v_total, resolution))
# problem_3.addVariable('x2', np.arange(0.0, v_total, resolution))
# problem_3.addVariable('x3', np.arange(0.0, v_total, resolution))

# def constraint_func_3(x1, x2, x3):
#     if (x1 + x2 + x3) == v_total and x1 <= v_max and x2 <= v_max and x3 <= v_max:
#         return True

# problem_3.addConstraint(constraint_func_3, ['x1', 'x2', 'x3'])
# solutions = problem_3.getSolutions()

# # Print solutions and add them to the graph
# print("3 Module Candidates")
# for index, solution in enumerate(solutions):
#     points_x.append(solution['x1'])
#     points_y.append(solution['x2'])
#     points_z.append(solution['x3'])
#     # We can do a simple model of the IV curve as X^2 + Y^2 = 1.
#     # This time, we take the minimum of the two modules.
#     current = min(
#         math.sqrt(1 - solution['x1']**2),
#         math.sqrt(1 - solution['x2']**2),
#         math.sqrt(1 - solution['x3']**2)
#     )*2-1 # Scaling correction to give more color range
#     points_mag.append(current)

#     # print("Candidate: ({},{},{}) = {}".format(
#     #     round(solution['x1'], 2),
#     #     round(solution['x2'], 2),
#     #     round(solution['x3'], 2),
#     #     round(current, 2))
#     # )

# # Filter out solutions for the best one(s).
# m = max(points_mag)
# max_pos = [i for i, j in enumerate(points_mag) if j == m]
# for pos in max_pos:
#     print("Best candidate: ({},{},{}) = {}".format(
#         round(points_x[pos], 2),
#         round(points_y[pos], 2),
#         round(points_z[pos], 2),
#         round(points_mag[pos], 2)
#     ))

# # Wrapping up the points and throwing them into the scatter plot.
# points_3 = []
# points_4 = []
# points_5 = []
# zip_points = zip(points_x, points_y, points_z, points_mag)
# for item in zip_points:
#     points_3.append({
#         'pos': [item[0], item[1]],
#         'data': item[3],
#         'pen': pg.mkPen(
#             (item[3]*255, 0, 0, 50),
#             width=5
#         )
#     })
#     points_4.append({
#         'pos': [item[0], item[2]],
#         'data': item[3],
#         'pen': pg.mkPen(
#             (0, item[3]*255, 0, 50),
#             width=5
#         )
#     })
#     points_5.append({
#         'pos': [item[1], item[2]],
#         'data': item[3],
#         'pen': pg.mkPen(
#             (0, 0, item[3]*255, 50),
#             width=5
#         )
#     })

# s1.addPoints(points)
# w1.addItem(s1)
s2.addPoints(points_2)
w2.addItem(s2)
# s3.addPoints(points_3)
# s3.addPoints(points_4)
# s3.addPoints(points_5)
# w3.addItem(s3)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

# NOTE: if you want to do pretty printing of solutions for debugging, try the
# following:
"""
length = len(solutions)
print("(x1, x2) ∈ {", end="")
for index, solution in enumerate(solutions):
    if index == length - 1:
        print("({},{})".format(
            round(solution['x1'], 3),
            round(solution['x2'], 3)),
            end=""
        )
    else:
        print("({},{}),".format(
            round(solution['x1'], 3),
            round(solution['x2'], 3)),
            end=""
        )

    points_x.append(solution['x1'])
    points_y.append(solution['x2'])
    # We can do a simple model of the IV curve as X^2 + Y^2 = 1.
    # This time, we take the minimum of the two modules.
    current = min(math.sqrt(1 - solution['x1']**2), math.sqrt(1 - solution['x2']**2))
    points_mag.append(current*10)
print("}")
"""