# MPPT System
The MPPT System is broken up into three different sections:
- Global MPPT Algorithms
- Local MPPT Algorithms
- Stride Algorithms

## Global MPPT Algorithms
The Global Algorithm is necessary because in conditions of partial shading, the power voltage curve of a solar array can have many local maxima, and local algorithms can get stuck at these local maxima. 
The goal of the global algorithm is to find the restricted domain that contains only one local maximum, with the maximum being the global maximum. 
Currently, three Global MPPT Algorithms have been implemented:
- Voltage Sweep
- Simulated Annealing
- Particle Swarm Optimization

## Local MPPT Algorithms
The goal of local MPPT algorithms is, given a restricted domain, find the local maximum in that region. This can be done by the Global algorithm as well, but local algorithms have had far more success in robustness, such that when the curve shifts to the left or right, the algorithm is still able to follow the direction the curve travels. There are two types of local algorithms that we have explored:
- Hill-Climbing Algorithms
- Divide and Conquer Algorithms
### Hill Climbing Algorithms
Hill Climbing Algorithms take on a simple rule: move in the direction that is uphill. More specifically, we make an incremental change to the x value and measure the y value. If the change in y was negative, then we are moving down hill and we need to move the other direction. If the change in y was positive, then we are moving uphill and we need to keep moving in that direciton. Hill climbing has advantages in ease of implementation and robustness against changing environmental conditions. They have disadvantages in convergence time. Current Hill Climbing algorithms that have been implemented are:
- PandO (Perturb and Observe)
- Incremental Conductance (IC)
- dP/dV feedback (FC)

### Divide and Conquer Algorithms
Divide and Conquer Algorithms work to cut the search area of the curve until it reaches a peak convergence. This involves moving goal posts towards the peak of the curve. Divide and Conquer Algorithms have advantages in convergence time but disadvantages in robustness and ease of implementation. Current Divide and Conquer algorithms that have been implemented are:
- Bisection Search
- Golden Search
- Ternary Search

## Stride Algorithms
Stride algorithms are algorithms specific to the hill-climbing algorithms that helps us calculate the magnitude of stride we want to take in whichever direction we are going. This can help us optimize precision and convergence time of the hill climbing algorithms. We have three types of stride algorithms:
- Adaptive Stride
- Optimal Stride
- Bisection Stride

A combination of all three of these algorithms are used to find the Global Maximum Power Point of an array's power-voltage curve.
