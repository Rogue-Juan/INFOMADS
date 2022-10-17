# this is the file where we input the situation and get the output solution

from decimal import ROUND_UP
import numpy as np
import os
from offline_ILP_algorithm import solve_ilp

decimalPrecision = 0

# acquire data from txt file
path_of_the_directory = os.getcwd() + "/Testinstances"
object = os.scandir(path_of_the_directory)
for test_instance in object :
    with open(path_of_the_directory + "/" + test_instance.name) as f:
        try:
            number_of_images = int(f.readline())
        except:
            raise ValueError("Wrongful input for number of images")
        finally:
            images = np.empty(number_of_images)
    
        for i in range(number_of_images):
            try:
                image = f.readline()
                decimals = image.split('.')
                if len(decimals) == 2:
                    if len(decimals[1]) > decimalPrecision:
                        decimalPrecision = len(decimals[1])

                image = float(image)
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
                decimals = start_time.split('.')
                if len(decimals) == 2:
                    if len(decimals[1]) > decimalPrecision:
                        decimalPrecision = len(decimals[1])
                start_time = float(start_time)
            except:
                raise ValueError("Wrongful input for interruption start time")
        
            try:
                decimals = length.split('.')
                if len(decimals) == 2:
                    if len(decimals[1]) > decimalPrecision:
                        decimalPrecision = len(decimals[1])
                length = float(length)
                if length == float('inf'):
                    infinite_interruption = True
                    # print('infinite interruption present')
                    length = np.Inf
            except:
                raise ValueError("Wrongful input for interruption length")
            finally:
                interruptions.append((start_time,length))
    
        # print("images:",images)
        # print("interruptions:",interruptions)
    
        interruptions = sorted(interruptions, key=lambda x: x[0])
        # print("interruptions:",interruptions)


        if infinite_interruption == True:
            number_of_blocks = number_of_interruptions
        else:
            number_of_blocks = number_of_interruptions + 1


        # calculate capacity of each block

        blocks = np.zeros(number_of_blocks)
        blockStarts = np.zeros(number_of_blocks)
        blockStarts[0] = 0
        blockstart = 0
    
        assert len(interruptions) == number_of_interruptions
    
        for i in range(number_of_blocks):           
            if i < number_of_interruptions:
                blocks[i] = interruptions[i][0] - blockstart
                blockstart = interruptions[i][0] + interruptions[i][1]
                #print(blockstart)
                blockStarts[i+1] = blockstart
            else:
                blocks[i] = np.Inf
            
         # print("block capacities:")
         # print(blocks)
            
         # blocks = [capacity1, capacity2, capacity3]; index is the block number, length is total number of blocks
    
        solution = solve_ilp(images, blocks)

        imageStarts = np.zeros(number_of_images)

        for i in range(number_of_images*number_of_blocks):
            if solution.x[i] == 1:
                whichImage = int(np.floor(i / number_of_blocks)) # index starts from 0
                whichBlock = int(i % number_of_blocks) # in case of 6 blocks: goes from 0 to 5
                imageStarts[whichImage] = float(blockStarts[whichBlock])
                #print(imageStarts[whichImage])
                blockStarts[whichBlock] += images[whichImage]

        score = imageStarts[-1] + images[-1] # [-1] accesses last elements in arrays.

        #string formatting

        imageStarts = np.around(imageStarts, decimals = decimalPrecision)
        imageStarts = imageStarts.astype('str')
        for i in range(len(imageStarts)):
            imageStarts[i] = imageStarts[i].rstrip('0').rstrip('.')

        score = np.around(score, decimals = decimalPrecision)
        score = str(score).rstrip('0').rstrip('.')

        #checking output with solution. Format = endtime, then n lines with start times of images (in input order)
        try:
            end_time_testinstance = float(f.readline())
        except:
            raise ValueError("Wrongful input for end time test instance")
       
        if end_time_testinstance == float(score):
            print(test_instance.name + ": correct") 
        else:
            print(test_instance.name + ": incorrect solution. \n \t Either the solution found or the test instance is incorrect.")
object.close()