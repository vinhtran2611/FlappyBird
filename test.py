import numpy as np


layer_dims = [5,4,1]
parameters = {}
L = len(layer_dims)            # number of layers in the network

for l in range(1, L):
    parameters['W' + str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) * 0.01
    parameters['b' + str(l)] = np.random.randn(layer_dims[l], 1)

print(parameters)

for l in range(1, L):
    shape = parameters['W' + str(l)].shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            parameters['W' + str(l)][i][j] = -parameters['W' + str(l)][i][j]

print(parameters)
