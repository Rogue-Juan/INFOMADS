# this is the file where we implement the ILP solver algorithm

from array import array
from logging import exception
import scipy
import numpy as np
from scipy import optimize
#from scipy.optimize import milp


def solve_ilp(images, blocks):
    if not (isinstance(images,np.ndarray) or isinstance(blocks,np.ndarray)):
        images = np.array(images); blocks = np.array(blocks)

    sizes = images 
    values = sizes
    
    bounds = optimize.Bounds(0,1)
    integrality = np.full_like(values, True)
    
    capacity = blocks
    constraints = optimize.LinearConstraint(A = sizes, lb = 0, ub = 30)
    
    res = scipy.optimize.milp(c = -values, constraints = constraints, integrality = integrality, bounds = bounds)
    
    return res

res = solve_ilp([5,3,4], [20,5])
print(res.x)
    