import numpy as np
import sys
from random import shuffle
from scipy.misc import imsave


# Determine from a position the next possible steps
def next_possible_steps(position, n, m):
    dpos = [-1, 1]
    steps = []
    for i in dpos:
        if (position[0] + 2 * i < 2*n+1) and (position[0] + 2 * i >= 0):
            steps.append((i, 0))
        if (position[1] + 2 * i < 2*m+1) and (position[1] + 2 * i >= 0):
            steps.append((0, i))
    shuffle(steps)
    return steps


# Create the maze reccursively (this approach doesn't allow large dimensions)
def rec_creation(lab, position, n, m):
    steps = next_possible_steps(position, n, m)
    for step in steps:
        if lab[position[0] + 2 * step[0], position[1] + 2 * step[1]] == 0:
            lab[position[0] + step[0], position[1] + step[1]] = 1
            lab[position[0] + 2 * step[0], position[1] + 2 * step[1]] = 1
            rec_creation(lab, (position[0] + 2*step[0], position[1] + 2*step[1]), n, m)


# Create grid
n = int(sys.argv[1])
m = int(sys.argv[2])
maze = np.zeros((2 * n + 1, 2 * m + 1))
maze[0, 0] = 1
position = (0, 0)
rec_creation(maze, position, n, m)

# Create outside walls
render = np.zeros((2*n+3, 2*m+3))
render[1,0] = 1
render[-2, -1] = 1
render[1:-1, 1:-1] = maze

# Save image
imsave(sys.argv[3], render)
