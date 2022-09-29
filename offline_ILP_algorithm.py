# this is the file where we implement the ILP solver algorithm

import scipy
import numpy as np
from scipy import optimize
#from scipy.optimize import milp


def solve_ilp(images):
    sizes = images 
    values = sizes
    
    bounds = optimize.Bounds(0,1)
    integrality = np.full_like(values, True)
    
    capacity = 10
    constraints = optimize.LinearConstraint(A = sizes, lb = 0, ub = capacity)
    
    res = scipy.optimize.milp(c = -values, constraints = constraints, integrality = integrality, bounds = bounds)
    
    return res

solve_ilp([5,3,4])
    