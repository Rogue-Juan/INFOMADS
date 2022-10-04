# this is the file where we input the situation and get the output solution

import numpy as np
#from offline_ILP_algorithm import solve_ilp



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
    
    
   # solve_ilp(images, blocks)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    