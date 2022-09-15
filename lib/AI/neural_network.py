import numpy as np
from copy import deepcopy
from typing import List, Callable


class Layer:
	def __init__(self, inputNeurons: int, neurons: int):
		self.weights: np.ndarray = np.random.standard_normal((neurons, inputNeurons))
		self.biases: np.ndarray = np.random.standard_normal((neurons, 1))

	def process(self, inputs: np.ndarray):
		return np.dot(self.weights, inputs) + self.biases

	def activate(self, inputs: np.ndarray, activationFunction: Callable):
		return activationFunction(self.process(inputs))


class NeuralNetwork:
	def __init__(self, layerSizes, hiddenActivation: Callable, outputActivation: Callable, seed: int = None):
		self.layers: List[Layer] = [Layer(a, b) for a, b in zip(layerSizes[:-1], layerSizes[1:])]
		self.hiddenActivation: Callable = hiddenActivation
		self.outputActivation: Callable = outputActivation

		self.rng = np.random.RandomState(seed)

	def process(self, inputs):
		output = np.array(inputs).reshape((len(inputs), 1))

		for i, layer in enumerate(self.layers):
			output = layer.activate(output, self.hiddenActivation if i != len(self.layers) -1 else self.outputActivation)

		return output

	def __mutate(self, mutationSize=0.02, layers=None):
		for layer in layers:
			layer.weights *= self.rng.uniform(1 - mutationSize, 1 + mutationSize, layer.weights.shape)
			layer.biases *= self.rng.uniform(1 - mutationSize, 1 + mutationSize, layer.biases.shape)

		return layers

	def mutate(self, mutationSize=0.02):
		self.__mutate(mutationSize, self.layers)

	def mutate_copy(self, mutationSize=0.02):
		return self.__mutate(mutationSize, deepcopy(self.layers))
