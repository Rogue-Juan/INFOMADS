# this is the file where we input the situation and get the output solution

import numpy as np
from offline_ILP_algorithm import solve_ilp



# acquire data from txt file

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
            if length == float('inf'):
                infinite_interruption = True
                print('infinite interruption present')
                length = np.Inf
        except:
            raise ValueError("Wrongful input for interruption length")
        finally:
            interruptions.append((start_time,length))
    
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
            blocks[i] = interruptions[i][0] - blockstart
            blockstart = interruptions[i][0] + interruptions[i][1]
        else:
            blocks[i] = np.Inf
            
    print("block capacities:")
    print(blocks)
            
# blocks = [capacity1, capacity2, capacity3]; index is the block number, length is total number of blocks
    
        
    
    
solution = solve_ilp(images, blocks)
print(solution.x)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    