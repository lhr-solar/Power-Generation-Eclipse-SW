# Global Maximum Power Point Tracking Algorithms
## Voltage Sweep
The voltage sweep algorithm is a novel algorithm used to find the global maximum power point of a power voltage curve. It is very precise an accurate, however, it is extremely inefficient and computationally expensive.
The algorithm is as follows:

Incrementally increase the voltage value from $0V$ to $V_{oc}$. We track whether the power value is increasing or decreasing. If the power value transitions from increasing to decreasing, we have found a local peak. If the power value transitions from decreasing to increasing, then we have found a local trough.
We store the power and voltage value of the local peaks, and we store the voltage values of the local troughs. After sweeping through the voltage values, we then find the voltage value with the highest power peak. This is where we will jump to and perform our local algorithms.