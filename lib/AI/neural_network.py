import numpy as np


class Neuron:
	def __init__(self, value=0, weights=None, bias=0):
		self.value = value
		self.weights = weights if weights is not None else []
		self.bias = bias

	def process(self, inputs):
		return np.dot(inputs, self.weights) + self.bias

	def activate(self, inputs, activationFunction):
		return activationFunction(self.process(inputs))


class Layer:
	def __init__(self, neurons):
		self.neurons = [Neuron() for _ in range(neurons)]

	def process(self, inputs):
		for neuron in self.neurons:
			yield neuron.process(inputs)

	def activate(self, inputs, activationFunction):
		for neuron in self.neurons:
			yield neuron.activate(inputs, activationFunction)


class NeuralNetwork:
	def __init__(self, hiddenLayers):
		self.hiddenLayers = [Layer(layer) for layer in hiddenLayers]

	def process(self, inputs, f, layer=0):
		if layer == len(self.hiddenLayers):
			return [val for val in self.hiddenLayers[layer].activate(inputs, f)]

		return self.process([val for val in self.hiddenLayers[layer].activate(inputs, f)], layer + 1)

