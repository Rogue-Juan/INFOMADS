# this is the file where we implement the ILP solver algorithm

from array import array
from logging import exception
import scipy
import numpy as np
from scipy import optimize
#from scipy.optimize import milp


def solve_ilp(image_sizes,
              block_capacities
              # penalty_scores
              ):
    if not (isinstance(image_sizes,np.ndarray) or isinstance(block_capacities,np.ndarray)):
        image_sizes = np.array(image_sizes); block_capacities = np.array(block_capacities)

    sizes = image_sizes 
    values = sizes
    
    bounds = optimize.Bounds(0,1)
    integrality = np.full_like(values, True)
    
    capacity = block_capacities
    constraints = optimize.LinearConstraint(A = sizes, lb = 0, ub = 30)
    
    res = scipy.optimize.milp(c = -values, constraints = constraints, integrality = integrality, bounds = bounds)
    
    return res

res = solve_ilp([5,3,4], [20,5])
print(res.x)
    