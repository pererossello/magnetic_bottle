import copy
import numpy as np
from numba import jit

mu0 = 4*np.pi*1e-7 # magnetic constant

@jit(nopython=True)
def B_dipole(r, mu, r0=np.array([0,0,0])):

    r_ = r-r0
    r_norm = np.sqrt(np.sum(r_ ** 2))

    if r_norm == 0:
        r_norm = 1e-9

    cte = mu0 / (4.0 * np.pi)  
    dot_product = np.sum(r_ * mu)  
    
    fact1 = 3 * dot_product * r_ / r_norm**5
    fact2 = mu / r_norm**3

    B = cte * (fact1 - fact2)

    return B


def trace_field_line(B, r0, steps=1000, step_size=0.1, direction='forward', lim=10):
    path = [r0]  # Initialize path with the starting point
    r = np.array(r0, dtype=np.float64)
    r0 = copy.deepcopy(r)
    
    if direction == 'both':
        directions = ['forward', 'backward']
    else:
        directions = [direction]

    for dir in directions:
        r = r0.copy()
        sign = 1 if dir == 'forward' else -1
        for _ in range(steps):
            B_val = B(r)  # Evaluate the magnetic field at the current position
            B_norm = B_val / np.linalg.norm(B_val)  # Normalize the field vector
            
            r = r + sign* B_norm * step_size  # Move forward along the field direction

            x_bool = np.abs(r[0]) > lim
            y_bool = np.abs(r[1]) > lim
            z_bool = np.abs(r[2]) > lim

            if x_bool or y_bool or z_bool:
                break
            
            if dir == 'forward':
                path = path + [r]
            else:
                path = [r] + path
        
    return np.array(path)

def RK4_first_order(t, x, f, h, direction="forward"):
    if direction == "forward":
        k1 = h * f(t, x)
        k2 = h * f(t + h / 2, x + k1 / 2)
        k3 = h * f(t + h / 2, x + k2 / 2)
        k4 = h * f(t + h, x + k3)
        x_ = x + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    elif direction == "backward":
        k1 = -h * f(t, x)
        k2 = -h * f(t - h / 2, x + k1 / 2)
        k3 = -h * f(t - h / 2, x + k2 / 2)
        k4 = -h * f(t, x + k3)
        x_ = x + (k1 + 2 * k2 + 2 * k3 + k4) / 6

    return x_
