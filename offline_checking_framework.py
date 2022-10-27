# this is the file where we input the situation and get the output solution

from decimal import ROUND_UP
import numpy as np
import os
import time
from offline_ILP_algorithm import solve_ilp

decimalPrecision = 0

#create output file for solution-instance comparison
output = open(os.getcwd() + '/output.txt', 'w')

# acquire data from txt file
path_test_instances_dir = os.getcwd() + "/Testinstances"
object = os.scandir(path_test_instances_dir)

# Keep track of the problem instance size by recording per instance the number of images and interruptions 
image_counts = []
interruption_counts = []
computation_times = []

instance_count = 0
for test_instance in object :
    instance_count += 1
    
    print("Test {}: {}".format(instance_count, test_instance.name))
    output.write("Test {}: {} \n".format(instance_count, test_instance.name))
    
    with open(path_test_instances_dir + "/" + test_instance.name, encoding= 'utf-8-sig') as f:
        ### Reading input from instance file
        ###
        try:
            #number_of_images_string = f.readline()
            number_of_images = int(f.readline())
        except:
            raise ValueError("Wrongful input for number of images.")
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
        
        ### Preprocessing of input 
        ###
        # computing starting times and sizes of interruptions
        interruptions = []
        infinite_interruption = False
    
        for i in range(number_of_interruptions):
            lines = f.readline().strip().split(',')
            start_time, length = lines[0].rstrip(), lines[1].rstrip()
        
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
        
        # Interruptions are sorted by their starting times
        interruptions = sorted(interruptions, key=lambda x: x[0])
        # print("interruptions:",interruptions)

        if infinite_interruption == True:
            number_of_blocks = number_of_interruptions
        else:
            number_of_blocks = number_of_interruptions + 1

        # calculate capacity of each block. 
        blocks = np.zeros(number_of_blocks) # blocks = [capacity1, capacity2, capacity3]; index is the block number, length is total number of blocks
        blockStarts = np.zeros(number_of_blocks)
        blockStarts[0] = 0
        blockstart = 0
    
        #assert len(interruptions) == number_of_interruptions
    
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
         
        ### Computing a solution
        # also measure the computation time
        t_start = time.time()
        solution = solve_ilp(images, blocks)
        t_end = time.time()
        time_duration = t_end - t_start

        ### Post-processing solution
        solutionX = np.round(solution.x, decimals=0)
        
        imageStarts = np.zeros(number_of_images)
        block_content = np.zeros(number_of_blocks)

        lastImage = 0
        lastImageStart = 0

        for i in range(number_of_images*number_of_blocks):
            if solutionX[i] == 1:
                whichImage = int(np.floor(i / number_of_blocks)) # index starts from 0
                whichBlock = int(i % number_of_blocks) # in case of 6 blocks: goes from 0 to 5       
                imageStarts[whichImage] = float(blockStarts[whichBlock])
                #print(imageStarts[whichImage])
                if imageStarts[whichImage] > lastImageStart:
                    lastImageStart = imageStarts[whichImage]
                    lastImage = whichImage

                blockStarts[whichBlock] += images[whichImage]
                #For each block, accumulate the image sizes that occur within it
                block_content[whichBlock] += images[whichImage]

        #Checking feasibility of solver solution
        is_feasible = True
        for i in range(number_of_blocks):
            if block_content[i] > blocks[i]:
                print("Block content exceeds capacity by {}.\n".format(block_content[i] - blocks[i]))
                output.write("Block content exceeds capacity by {}.\n".format(block_content[i] - blocks[i]))
                is_feasible = False

        score = lastImageStart + images[lastImage]
        score_float = score
        
        #Format solution and corresponding completion time to string
        imageStarts = np.around(imageStarts, decimals = decimalPrecision)
        imageStarts = imageStarts.astype('str')
        for i in range(len(imageStarts)):
            imageStarts[i] = imageStarts[i].rstrip('0').rstrip('.')

        score = np.around(score, decimals = decimalPrecision)
        score = str(score).rstrip('0').rstrip('.')

        #Read completion time of model solution from file
        try:
            end_time_testinstance_string = f.readline().rstrip()
        except:
            raise ValueError("Wrongful input for end time test instance")
       
        #Compare solution to model solution and write result to output
        if not is_feasible or end_time_testinstance_string != score:
            print("Incorrect solution. Feasible: {}.\n Instance time: {} --- Solver time: {}".format(is_feasible, end_time_testinstance_string, score))
            output.write("Incorrect solution. Feasible: {}.\n Instance time: {} --- Solver time: {}\n".format(is_feasible, end_time_testinstance_string, score))
            #solution_str = ""
            for i in range(number_of_images - 1):
                output.write(str(imageStarts[i]) + " -- ")
                #solution_str += str(imageStarts[i]) + " -- "
            output.write(str(imageStarts[number_of_images - 1]) + "\n")
            #print(solution_str.rstrip(' -- ') + "\n")
        else:
            print(test_instance.name + ": correct") 
            output.write(test_instance.name + ": correct\n")
            # Record input size of problem instance and computation time
            image_counts.append(number_of_images)
            interruption_counts.append(number_of_interruptions)
            computation_times.append(time_duration)
object.close()

assert(len(image_counts) == len(interruption_counts) & len(interruption_counts) == len(computation_times))

with open(os.getcwd() + '/output_statistics.txt', 'w') as f:
    f.write("Instance,number of images,number of interruptions, computation time\n")
    for i in range(len(image_counts)):
        f.write("{},{},{},{}\n".format(i, image_counts[i], interruption_counts[i], computation_times[i]))


        
