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

import numpy as np
import matplotlib.pyplot as plt
import math
import constraint # https://stackabuse.com/constraint-programming-with-python-constraint/
import src.source_file


# Creating figure
fig = plt.figure(figsize = (10, 7))
ax = fig.add_subplot(111, projection='3d')

"""
3rd Plot. A 2D graph (with 3 overlapping datasets) representing the min
current as a function of THREE independent module voltages.
The color of the points represent the current magnitude and the two
axes represent a subset of the 3 independent modules.
Voltage range is constrained by the constraint function.
"""
# Main Generation Code
points_x    = []
points_y    = []
points_z    = []
points_mag  = []

# Independent axis constraint
problem_3 = constraint.Problem()
v_total = 2.6 # at most v_max*(v1_scaling+v2_scaling+v3_scaling)
v_max = .8
v1_scaling = 1
v2_scaling = 1
v3_scaling = 1
resolution_digits = 2.3 # Up to 2.3 for the sim to generate in a reasonable amount of time
error = 1/(10**resolution_digits) # modify the numerator to adjust error proportion

problem_3.addVariable('x1', np.arange(0.0, v_max*v1_scaling, 1/(10**resolution_digits)))
problem_3.addVariable('x2', np.arange(0.0, v_max*v2_scaling, 1/(10**resolution_digits)))
problem_3.addVariable('x3', np.arange(0.0, v_max*v3_scaling, 1/(10**resolution_digits)))

def constraint_func_3(x1, x2, x3):
    x1 = round(x1, math.ceil(resolution_digits))
    x2 = round(x2, math.ceil(resolution_digits))
    x3 = round(x3, math.ceil(resolution_digits))
    if ((x1 + x2 + x3) <= v_total*(1+error) and (x1 + x2 + x3) >= v_total*(1-error)):
        return True

problem_3.addConstraint(constraint_func_3, ['x1', 'x2', 'x3'])
solutions = problem_3.getSolutions()

# Print solutions and add them to the graph
print("3 Module Candidates")
for index, solution in enumerate(solutions):
    points_x.append(solution['x1'])
    points_y.append(solution['x2'])
    points_z.append(solution['x3'])
    # We can do a simple model of the IV curve as X^2 + Y^2 = 1.
    # This time, we take the minimum of the two modules.
    current = min(
        math.sqrt(v_max**2*v1_scaling - solution['x1']**2),
        math.sqrt(v_max**2*v2_scaling - solution['x2']**2),
        math.sqrt(v_max**2*v3_scaling - solution['x3']**2)
    )
    points_mag.append(current)

    # print("Candidate: ({},{},{}) = {}".format(
    #     round(solution['x1'], math.ceil(resolution_digits)),
    #     round(solution['x2'], math.ceil(resolution_digits)),
    #     round(solution['x3'], math.ceil(resolution_digits)),
    #     round(current, 2))
    # )

# Filter out solutions for the best one(s).
m = max(points_mag)
max_pos = [i for i, j in enumerate(points_mag) if j == m]
for pos in max_pos:
    print("Best candidate: ({},{},{}) = {}".format(
        round(points_x[pos], 2),
        round(points_y[pos], 2),
        round(points_z[pos], 2),
        round(points_mag[pos], 2)
    ))

# Creating plot
ax.scatter3D(points_x, points_y, points_z, c=points_mag, cmap=plt.get_cmap("YlOrRd"))
plt.title("3 modules.")

plt.show()

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