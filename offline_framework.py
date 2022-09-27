# this is the file where we input the situation and get the output solution

import numpy as np
import offline_ILP_algorithm

with open('testInstance.txt') as f:
    number_of_images = int(f.readline())
    images = np.empty(number_of_images)
    
    for i in range(number_of_images):
        images[i] = int(f.readline())
    
    number_of_interruptions = int(f.readline())
    interruptions = []
    
    for i in range(number_of_interruptions):
        line = f.readline()
        start_time, length = line.strip().split(', ')
        interruptions.append((int(start_time),int(length)))
    
    print("images:",images)
    print("interruptions:",interruptions)
        