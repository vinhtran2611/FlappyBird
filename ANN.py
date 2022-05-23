import numpy as np
import Bird as Bird_Class
from settings import *
import sys
import random


class ANN:
    def __init__(self, layer_dims = LAYER_DIMS, genome = None):
        self.fitness = 0
        self.layer_dims = layer_dims
        self.parameters = {}

        if genome is not None:  # if constructor have genome then use that genome for weight
            self.parameters = genome
        else:
            self.parameters = self.initialize_parameters_deep()

    def sigmoid(self, Z):
        A = 1/(1+np.exp(-Z))
        return A

    def relu(self, Z):        
        A = np.maximum(0,Z)
        return A

    def initialize_parameters_deep(self):
        parameters = {}
        L = len(self.layer_dims)            # number of layers in the network

        for l in range(1, L):
            parameters['W' + str(l)] = np.random.randn(self.layer_dims[l], self.layer_dims[l-1]) * 0.01
            parameters['b' + str(l)] = np.zeros((self.layer_dims[l], 1))
        
        return parameters

    def linear_forward(self, A, W, b):
        Z = np.dot(W, A) + b
        return Z

    def linear_activation_forward(self, A_prev, W, b, activation):    
        if activation == "sigmoid":
            Z = self.linear_forward(A_prev, W, b)
            A = self.sigmoid(Z)
        elif activation == "relu":
            Z = self.linear_forward(A_prev, W, b)
            A = self.relu(Z)

        return A

    def L_model_forward(self, X):
        A = X
        L = len(self.parameters) // 2                  # number of layers in the neural network
        
        # Implement [LINEAR -> RELU]*(L-1). Add "cache" to the "caches" list.
        for l in range(1, L):
            A_prev = A 
            A = self.linear_activation_forward(A_prev, self.parameters['W'+str(l)], self.parameters['b'+str(l)], activation="relu")
        
        AL = self.linear_activation_forward(A, self.parameters['W'+str(L)], self.parameters['b'+str(L)], activation="sigmoid")
        return AL

    @classmethod
    def selection(clf, bird_list):
        elite_birds_copy = []  # create a copy of list to put all elite bird in to avoid inconsistency problem
        elite_birds = bird_list[0:round(ELITE_PRECENTAGE * POPULATION)]

        for bird in elite_birds:
            gen = bird.ANN.parameters  # encode to gen
            elite_birds_copy.append(Bird_Class.Bird(genome = gen))  # decode gen to read weight

        return elite_birds_copy

    @classmethod
    def mutation(clf, bird):  # change some weights randomly
        gen = bird.ANN.parameters

        L = len(bird.ANN.layer_dims)            # number of layers in the network
        for l in range(1, L):
            shape = gen['W' + str(l)].shape
            for i in range(shape[0]):
                for j in range(shape[1]):
                    if np.random.rand(0, 100) < MUTATION_RATE * 100:
                        gen['W' + str(l)][i][j] = - gen['W' + str(l)][i][j]


        new_bird = Bird_Class.Bird(genome= gen)
        return new_bird

    @classmethod
    def crossover(clf, bird1, bird2):  # swap weight
        gen_bird1 = bird1.ANN.parameters  # mutation on a gene so that the actual bird.ANN will not be change
        gen_bird2 = bird2.ANN.parameters
        new_gen = gen_bird2

        L = len(bird1.ANN.layer_dims)            # number of layers in the network
        for l in range(1, L):
            shape = gen_bird1['W' + str(l)].shape
            for i in range(shape[0]):
                for j in range(shape[1]):
                    if np.random.rand(0, 100) < CROSSOVER_RATE * 100:
                        # aprox 1
                        # new_gen['W' + str(l)][i][j] = 0.5 * (gen_bird1['W' + str(l)][i][j] +  gen_bird2['W' + str(l)][i][j])
                        # aprox 2
                        new_gen['W' + str(l)][i][j] = gen_bird1['W' + str(l)][i][j]
                    
        return Bird_Class.Bird(genome = new_gen)

    @classmethod
    def save_weight(cls):
        pass

    @classmethod
    def create_new_generation(clf, bird_list):
        new_generation = []

        # selection
        elite_birds = ANN.selection(bird_list)
        new_generation.extend(elite_birds)

        # crossover best bird and elite birds
        for i in range(1, round(len(elite_birds) / 2)):
            new_generation.append(ANN.crossover(elite_birds[0], elite_birds[i]))

        # crossover best bird with the old birds
        for i in range(round((CROSSOVER_PERCENTAGE * POPULATION))):
            idx_bird2 = random.randint(0, len(bird_list) - 2)
            new_generation.append(ANN.mutation(ANN.crossover(elite_birds[0], bird_list[idx_bird2])))

        # crossover with the elite birds
        for i in range(round((3 * CROSSOVER_PERCENTAGE * POPULATION))):
            idx_bird1, idx_bird2 = random.sample(range(0, len(elite_birds)), 2)	
            new_generation.append(ANN.crossover(elite_birds[idx_bird1], elite_birds[idx_bird2]))
            
        # crossover + mutation with the elite birds
        for i in range(round((CROSSOVER_PERCENTAGE * POPULATION))):
            idx_bird1 = random.randint(0, len(elite_birds) - 2)
            idx_bird2 = random.randint(0, len(bird_list) - 2)
            new_generation.append(ANN.mutation(ANN.crossover(elite_birds[idx_bird1], bird_list[idx_bird2])))

        # random bird to increase diversity
        for i in range(POPULATION - len(new_generation)):
            new_generation.append(Bird_Class.Bird())

        return new_generation
