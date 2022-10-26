# This is the file where the input is read and processed
# and where the solution, the output, is written to a text file

import numpy as np
from offline_ILP_algorithm import solve_ilp

decimalPrecision = 0

# Acquire instance from txt file
filename = 'Testinstances/Instance'
with open(filename+".txt") as f:
    try:
        number_of_images = int(f.readline())
    except:
        raise ValueError("Wrongful input for number of images")
    finally:
        images = np.empty(number_of_images)
    
    # Image sizes are read and decimal precision is tracked
    for i in range(number_of_images):
        try:
            image = f.readline()
            decimals = image.split('.')
            if len(decimals) == 2:
                if len(decimals[1]) > decimalPrecision:
                    decimalPrecision = len(decimals[1])

            image = float(image)
        except:
            raise ValueError("Wrong input for image size")
        finally:
            images[i] = image
    
    number_of_interruptions = int(f.readline())
    interruptions = []
    
    # Infinite interruptions are allowed
    infinite_interruption = False
    
    # Interruptions are read
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
            raise ValueError("Wrong input for interruption start time")
        
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
            raise ValueError("Wrong input for interruption length")
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


# Calculate capacity of each block; see Preliminaries for definition of 'blocks'

    blocks = np.zeros(number_of_blocks) # Capacities of the blocks
    blockStarts = np.zeros(number_of_blocks) # Remembers starting times for next images if an image has been added to the block
    blockStarts[0] = 0
    blockstart = 0
    
    assert len(interruptions) == number_of_interruptions
    
    for i in range(number_of_blocks):           
        if i < number_of_interruptions:
            blocks[i] = interruptions[i][0] - blockstart        # Next interruption start time - previous interruption end time 
            blockstart = interruptions[i][0] + interruptions[i][1]      # Start time + length
            #print(blockstart)
            blockStarts[i+1] = blockstart
        else:
            blocks[i] = np.Inf
            
    # print("block capacities:")
    # print(blocks)

# Call solver and generate solution
solution = solve_ilp(images, blocks)
#print(solution.x, sum(solution.x))

# Transform numpy float array to integer array; necessary for if-statement
solutionX = np.round(solution.x, decimals=0)
#print(solutionX, sum(solutionX))

imageStarts = np.zeros(number_of_images)

# Needed for calculation of the score
lastImage = 0
latestTime = 0

# Calculate start times for images based on output (a binary vector)
for i in range(number_of_images*number_of_blocks):
    if solutionX[i] == 1:
        whichImage = int(np.floor(i / number_of_blocks)) # index starts from 0
        whichBlock = int(i % number_of_blocks) # in case of 6 blocks: goes from 0 to 5
        imageStarts[whichImage] = float(blockStarts[whichBlock])
        #print(imageStarts[whichImage])
        if imageStarts[whichImage] > latestTime:
            latestTime = imageStarts[whichImage]
            lastImage = whichImage

        blockStarts[whichBlock] += images[whichImage]

score = latestTime + images[lastImage]

# Format output according to decimal precision and without trailing zeros
imageStarts = np.around(imageStarts, decimals = decimalPrecision)
imageStarts = imageStarts.astype('str')
for i in range(len(imageStarts)):
    imageStarts[i] = imageStarts[i].rstrip('0').rstrip('.')

score = np.around(score, decimals = decimalPrecision)
score = str(score).rstrip('0').rstrip('.')

# Write to solution file
with open(filename+"_sol.txt", 'w') as f:
    f.write(str(score))
    for i in range(number_of_images):
        f.write('\n'+str(imageStarts[i]))