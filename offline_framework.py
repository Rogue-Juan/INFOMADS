# this is the file where we input the situation and get the output solution

from cmath import inf
import numpy as np
#from offline_ILP_algorithm import solve_ilp



# acquire data from txt file
number_of_images = 0

with open('testInstance1.txt') as f:
    try:
        number_of_images = int(f.readline())
    except:
        raise ValueError("Wrongful input for number of images")
    finally:
        images = np.empty(number_of_images)
    
    for i in range(number_of_images):
        try:
            image = float(f.readline())
        except:
            raise ValueError("Wrongful input for image size")
        finally:
            images[i] = image
    
    number_of_interruptions = int(f.readline())
    interruptions = []
    
    infinite_interruption = False
    
    for i in range(number_of_interruptions):
        line = f.readline()
        start_time, length = line.strip().split(', ')
        
        try:
            start_time = float(start_time)
        except:
            raise ValueError("Wrongful input for interruption start time")
        
        try:
            length = float(length)
        except:
            if length in ["infinity","inf"]:
                infinite_interruption = True
                length = np.Inf
            else:
                raise ValueError("Wrongful input for interruption length")
        finally:
            interruptions.append((start_time,length))
    
    images = np.sort(images)        # sorts from smallest to largest
    print("images:",images)
    print("interruptions:",interruptions)
    
    interruptions = sorted(interruptions, key=lambda x: x[0])
    print("interruptions:",interruptions)


    if infinite_interruption == True:
        number_of_blocks = number_of_interruptions
    else:
        number_of_blocks = number_of_interruptions + 1


# calculate capacity of each block

    blocks = np.zeros(number_of_blocks)
    blockstart = 0
    
    assert len(interruptions) == number_of_interruptions
    
    for i in range(number_of_blocks):           
        if i < number_of_interruptions:
            blocks[i] = blockstart + interruptions[i][1]
            blockstart = interruptions[i][0] + interruptions[i][1]
        else:
            blocks[i] = np.Inf
            
    print("block capacities:")
    print(blocks)
            
# blocks = [capacity1, capacity2, capacity3]; index is the block number, length is total number of blocks
    

# create 2D matrix of block prices: the price of image i in block j

    block_price = np.zeros([number_of_images,number_of_blocks])
    
    
    
    for image in range(len(block_price)):
        for block in range(len(block_price[0])):
            block_price[image,block] = images[image] * (block+1)
            
    print("block prices:")
    print(block_price)
    
    
   # solve_ilp(images) --> scipy.optimize.milp(c, *, integrality=None, bounds=None, constraints=None, options=None)
   # returns a scipy.optimize.OptimizeResult object having the following attributes:
   #    status: 0 = optimal s found, 1 = iteration/time limit reached, 2 = problem infeasible
   #             3= problem unbounded and 4 = other
   #    success: T/F
   #    message: exit status description
   #    x (ndarray): values of decision variables 
   #    fun: optimal value
    solution = solve_ilp(images)     

   # Parsing ILP solution to required solution format

for i in range(number_of_images*number_of_blocks):
    if solution.x[i] == 1:
        whichImage = int(i / number_of_blocks) # index starts from 0
        whichBlock = i % number_of_blocks # in case of 6 blocks: goes from 0 to 5
        imageStarts[whichImage] = blockStarts[whichBlock]
        print(imageStarts[whichImage])
        blockStarts[whichBlock] += images[whichImage]

    image_starting_times = [0] * number_of_images
    t = 0
    k = 0
    for j in range(number_of_blocks):
        for i in range(number_of_images):
            if solution.x[i * number_of_blocks + j] == 1:
                image_starting_times[i] = t
                t += images[i]
        
        if k >= number_of_interruptions: pass
        next_interruption = interruptions[k]
        
        if next_interruption[1] == np.inf: pass
        t = next_interruption[0] + next_interruption[1]
        k += 1
    
    #output format: endtime, then n lines with start times of images (in input order)
    with open("solution.txt", 'w') as f:
        f.write(t)
        for i in range(number_of_images):
            f.write("\n" + image_starting_times[i])
   
   

    
    
    
    
    
    
    
    
    
    
    
    
    
    