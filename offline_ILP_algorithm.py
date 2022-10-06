# this is the file where we implement the ILP solver algorithm

from array import array
from logging import exception
import scipy
import numpy as np
from scipy import optimize
#from scipy.optimize import milp


def solve_ilp(image_sizes,
              block_capacities
              ):
    if not (isinstance(image_sizes,np.ndarray) or isinstance(block_capacities,np.ndarray)):
        image_sizes = np.array(image_sizes)
        block_capacities = np.array(block_capacities)

    # create 2D matrix of block prices: the price of image i in block j

    penalty_scores = np.zeros([len(image_sizes),len(block_capacities)])
    
    for image in range(len(penalty_scores)):
        for block in range(len(penalty_scores[0])):
            penalty_scores[image,block] = image_sizes[image] * (block+1)
    print(penalty_scores)
    
    bounds = optimize.Bounds(0,1)
    integrality = np.full_like(image_sizes, True)
    
    bigA = np.ndarray( shape = (len(block_capacities), len(image_sizes)) )
    for i in range(len(block_capacities)):
        bigA[i] = image_sizes

    #print(bigA)
    constraints = optimize.LinearConstraint(A = bigA, lb = 0, ub = block_capacities)
    
    res = scipy.optimize.milp(c = -image_sizes
                             , constraints = constraints
                             , integrality = integrality
                             , bounds = bounds)
    
    return res

res = solve_ilp([5,3,4], [20,5])
print("Result is:\n",res.x)
    