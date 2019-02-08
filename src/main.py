import os
import numpy as np
from scipy.misc import imread, imsave


# Define an upscale without smoothing function
def upscale(name, ratio):
    image = imread(name + '.png', mode='RGB')
    out = np.arange(ratio * ratio * image.shape[0] * image.shape[1] * image.shape[2])\
            .reshape(ratio * image.shape[0], ratio * image.shape[1], image.shape[2])
    for i in range(ratio * image.shape[0]):
        for j in range(ratio * image.shape[1]):
            for k in range(3):
                out[i, j, k] = image[i/ratio, j/ratio, k]
    imsave(name + '_rescaled.png', out)

# Create output directory
if not os.path.isdir('../output'):
    os.makedirs('../output')

# Generate maze
os.system('python generate.py 35 35 ../output/maze.png')

# Solve maze
os.system('python solve.py ../output/maze.png ../output/solved_maze.png')

# Upscale images
upscale('../output/solved_maze', 10)
upscale('../output/maze', 10)
