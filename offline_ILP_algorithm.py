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
    
    bounds = optimize.Bounds(0,1)
    integrality = np.full_like(image_sizes, True)
    
    bigA = np.ndarray( shape = (len(block_capacities), len(image_sizes)) )
    for i in range(len(block_capacities)):
        bigA[i] = image_sizes

    print(bigA)
    constraints = optimize.LinearConstraint(A = bigA, lb = 0, ub = block_capacities)
    
    res = scipy.optimize.milp(c = -image_sizes
                             , constraints = constraints
                             , integrality = integrality
                             , bounds = bounds)
    
    return res

res = solve_ilp([5,3,4], [20,5])
print("Result is:\n",res.x)
    