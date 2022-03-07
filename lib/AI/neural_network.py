import numpy as np
from func import sigmoid

"""
class Neuron:
	def __init__(self, weights=None, bias=0, value=0):
		self.value = value
		self.weights = weights if weights is not None else []
		self.bias = bias

	def process(self, inputs):
		return np.dot(inputs, self.weights) + self.bias

	def activate(self, inputs, activationFunction):
		return activationFunction(self.process(inputs))
"""


class Layer:
	def __init__(self, inputNeurons, neurons):
		self.weights = np.random.standard_normal([neurons, inputNeurons])
		self.biases = np.zeros((neurons, 1))

	def process(self, inputs):
		return np.dot(self.weights, inputs) + self.biases

	def activate(self, inputs, activationFunction):
		return activationFunction(self.process(inputs))


class NeuralNetwork:
	def __init__(self, layerSizes):
		self.layers = [Layer(a, b) for a, b in zip(layerSizes[:-1], layerSizes[1:])]

	def process(self, inputs, f):
		output = inputs[:]

		for layer in self.layers:
			output = layer.activate(output, f)

		return output

	def mutate(self, mutationSize=0.02):
		for layer in self.layers:
			layer.weights += np.random.uniform(-mutationSize, mutationSize, layer.weights.shape)
			layer.biases += np.random.uniform(-mutationSize, mutationSize, layer.biases.shape)


# network = NeuralNetwork([3, 3, 5, 3, 1])
# X = np.ones((3, 1))
# print(X)
# print(network.process(X, sigmoid))
