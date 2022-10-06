# this is the file where we implement the ILP solver algorithm

from array import array
from logging import exception
from turtle import pen
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
    penalty_scores = penalty_scores.flatten()
   # print(penalty_scores)
    
    bounds = optimize.Bounds(0,1)
    integrality = np.full_like(penalty_scores, True)
    
    bigA = np.ndarray( shape = (len(block_capacities), len(image_sizes)) )
    for i in range(len(block_capacities)):
        bigA[i] = image_sizes

    flat_A = bigA.flatten('F')  # 'F' represents column-major ordering

    bigA = np.full_like(a = np.ndarray(shape=(len(block_capacities), len(flat_A)))
                       , fill_value=0)
    for i in range(len(block_capacities)):
        for j in range(len(flat_A)):
            if j % len(block_capacities) == i:
                bigA[i][j] = flat_A[j]

#    print(bigA)

    constraint1 = optimize.LinearConstraint(A = bigA, lb = 0, ub = block_capacities)

    bigB = np.zeros((len(image_sizes),len(block_capacities)*len(image_sizes)))

    count = 0
    for j in range(len(block_capacities)*len(image_sizes)):
        bigB[count][j] = 1
        if (j+1) % len(block_capacities) == 0:
            count += 1

    #print(bigB)
    constraint2 = optimize.LinearConstraint(A = bigB, lb = 1, ub = 1)
    
    res = scipy.optimize.milp(c = penalty_scores
                             , constraints = [constraint1,constraint2]
                             , integrality = integrality
                             , bounds = bounds)
    
    return res

res = solve_ilp([5,3,4], [5,5,5])
print("Result is:\n",res.x)
    