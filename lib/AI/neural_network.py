import numpy as np


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
			layer.weights *= np.random.uniform(-mutationSize, mutationSize, layer.weights.shape)
			layer.biases *= np.random.uniform(-mutationSize, mutationSize, layer.biases.shape)
