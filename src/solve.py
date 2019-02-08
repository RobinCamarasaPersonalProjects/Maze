import sys

import numpy as np
from scipy.misc import imread, imsave
from scipy.ndimage.filters import convolve


# Define the path you can take
def possible_steps(position, maze):
    n, m, p = maze.shape
    dpos = [-1, 1]
    steps = []
    for i in dpos:
        if (position[0] + i in range(n)) and maze[position[0] + i, position[1], 1] == 1:
            steps.append((i, 0))
        if (position[1] + i in range(m)) and maze[position[0], position[1] + i, 1] == 1:
            steps.append((0, i))
    return steps


# Define graph
def compute_graph(out):
    x, y = np.where((out[:, :, 0] == 0) * (out[:, :, 1] == 1))
    nodes = []
    graph = {}
    for i in range(x.shape[0]):
        nodes.append((x[i], y[i]))
        graph[str((x[i], y[i]))] = []

    for node in nodes:
        steps = possible_steps(node, out)
        for step in steps:
            found = False
            counter = 1
            while not found:
                if (node[0] + counter * step[0], node[1] + counter * step[1]) in nodes:
                    graph[str(node)].append((counter, (node[0] + counter * step[0], node[1] + counter * step[1])))
                    found = True
                else:
                    counter += 1
    return nodes, graph


# Define forward djikstra algorithm
def djikstra(graph, cost, current_node):
    key_current_node = str(current_node)
    cost[key_current_node][1] = True
    for item in graph[key_current_node]:
        if not cost[str(item[1])][1]:
            cost[str(item[1])][0] = min(cost[str(item[1])][0], cost[key_current_node][0] + item[0])
            djikstra(graph, cost, item[1])


# Define backward djikstra algorithm
def back_djikstra(graph, cost, current_node, list):
    if str(current_node) == '(1, 0)':
        return list
    else:
        value = np.Inf
        node = ''
        for item in graph[str(current_node)]:
            if cost[str(item[1])][0] < value:
                value = cost[str(item[1])][0]
                node = item[1]
        list.append(node)
        return back_djikstra(graph, cost, node, list)


# Read and compute image
input = imread(sys.argv[1])
out = np.array([input[:] / 255, input[:] / 255, input[:] / 255])
out = np.transpose(out, (1, 2, 0))


# Compute maze junctions
junctions = np.uint64(1) - (convolve(input[:] / 255, [[0, 1, 0], [-1, 1, -1], [0, 1, 0]]) != 3) * (
            convolve(input[:] / 255, [[0, -1, 0], [1, 1, 1], [0, -1, 0]]) != 3)
out[:, :, 0] *= junctions
out[1, 0, 0] = 0
out[-2, -1, 0] = 0

# Compute graph
nodes, graph = compute_graph(out)

# Djikstra algorithm
cost = {}
for key in list(graph):
    cost[key] = [np.Inf, False]
current_node = (1, 0)
cost[str(current_node)] = [0, True]
djikstra(graph, cost, current_node)
path = back_djikstra(graph, cost, (input.shape[0]-2, input.shape[1]-1), [(input.shape[0]-2, input.shape[1]-1)])

# Display result
out = out.astype(float)
for i in range(1, len(path)):
    x_1, y_1 = path[i]
    x_2, y_2 = path[i-1]
    if x_1 == x_2:
        for j in range(min(y_1, y_2), max(y_1, y_2)+1):
            out[x_1, j, 0] = 1 - float(i)/len(path)
            out[x_1, j, 1] = 0
            out[x_1, j, 2] = float(i)/len(path)
    if y_1 == y_2:
        for j in range(min(x_1, x_2), max(x_1, x_2)+1):
            out[j, y_1, 0] = 1 - float(i)/len(path)
            out[j, y_1, 1] = 0
            out[j, y_1, 2] = float(i)/len(path)
out = 255 * out
imsave(sys.argv[2], out)
