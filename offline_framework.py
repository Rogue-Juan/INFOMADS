# this is the file where we input the situation and get the output solution

import numpy as np
import offline_ILP_algorithm

with open('testInstance.txt') as f:
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
            else:
                raise ValueError("Wrongful input for interruption length")
        finally:
            interruptions.append((start_time,length))
    
    images = np.sort(images)        # sorts from smallest to largest
    print("images:",images)
    print("interruptions:",interruptions)
    
    if infinite_interruption == True:
        number_of_blocks = number_of_interruptions
    else:
        number_of_blocks = number_of_interruptions + 1
    
    # [TODO]: sort interruptions by starting time
    
    # [TODO]: calculate capacity of each block
    # blocks = [capacity1, capacity2, capacity3]; index is the block number, length is total number of blocks
    
    block_price = np.zeros([number_of_images,number_of_blocks])
    
    
    
    for image in range(len(block_price)):
        for block in range(len(block_price[0])):
            block_price[image,block] = images[image] * (block+1)
            
    print(block_price)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    