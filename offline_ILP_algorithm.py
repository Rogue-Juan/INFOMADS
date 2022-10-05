# this is the file where we implement the ILP solver algorithm

import scipy
import numpy as np
from scipy import optimize
#from scipy.optimize import milp


def solve_ilp(images, blocks):
    sizes = images 
    values = sizes
    
    bounds = optimize.Bounds(0,1)
    integrality = np.full_like(values, True)
    
    capacity = blocks
    constraints = optimize.LinearConstraint(A = sizes, lb = 0, ub = 30)
    
    res = scipy.optimize.milp(c = -values, constraints = constraints, integrality = integrality, bounds = bounds)
    
    return res

res = solve_ilp(np.array([5,3,4]), np.array([20,5]))
print(res.x)
    