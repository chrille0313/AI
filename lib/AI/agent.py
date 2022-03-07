from neural_network import NeuralNetwork
from func import sigmoid, linear, relu
import numpy as np
from numpy import random
from copy import deepcopy


class Game:
	def __init__(self, nr):
		self.x = nr
		self.guesses = 0

	def guess(self, x):
		self.guesses += 1

		if self.x == x:
			return 0
		elif self.x > x:
			return -1
		elif self.x < x:
			return 1


class Agent:
	def __init__(self, layerSizes, fitness=0):
		self.fitness = fitness
		self.neuralNetwork = NeuralNetwork(layerSizes)

	def think(self, inputs):
		return self.neuralNetwork.process(inputs, linear)


def new_generation(agents, nr):
	fitnesses = [agent.fitness for agent in agents]
	best, worst = max(fitnesses), min(fitnesses)

	probs = [(agent.fitness - worst) ** 2 for agent in agents]
	tot = sum(probs)
	probs = [prob / tot for prob in probs]

	newAgents = [deepcopy(agents[random.choice(range(len(agents)), p=probs)]) for _ in range(len(agents))]

	for agent in newAgents:
		agent.neuralNetwork.mutate(0.2)

	return newAgents, [Game(nr) for _ in range(len(agents))]


lower, upper = -10010, -10000
nr = random.randint(lower, upper)

agents = [Agent([1, 3, 3, 1]) for _ in range(300)]
games = [Game(nr) for _ in range(300)]

for agent in agents:
	agent.neuralNetwork.mutate()

generations = 100000000
guessAmount = 50

for generation in range(generations):
	bestDiff = 1e9
	avgDiff = 0
	avgGuess = 0
	maxGen = -1e9
	minGen = 1e9
	avgFitness = 0
	for i, agent in enumerate(agents):
		game = games[i]
		guessResult = 0

		for _ in range(guessAmount):
			agentInput = np.reshape([guessResult], (1, 1))
			guess = agent.think(agentInput)[0][0]
			guessResult = game.guess(guess)

			if guessResult == 0:
				break

		agent.fitness = -abs(game.x - guess)

		minGen = min(minGen, guess)
		maxGen = max(maxGen, guess)
		bestDiff = min(bestDiff, abs(game.x - guess))
		avgDiff += abs(game.x - guess)
		avgGuess += guess
		avgFitness += agent.fitness

	if generation % 100 == 0:
		print(
			f"avgFitness: {avgFitness / len(agents)}    bestDiff: {bestDiff}   avgDiff: {avgDiff / len(agents)}   avgGuess: {avgGuess / len(agents)}   maxGen: {maxGen}    minGen: {minGen}    generation: {generation}")

	"""if generation % 1000 == 0:
		bestAgent = max(agents, key=lambda agent: agent.fitness)
		with open("weights.txt", "a") as f:
			f.write(f"\n-------------------- GENERATION {generation} --------------------\n")
			for i, layer in enumerate(bestAgent.neuralNetwork.layers):
				f.write(f"\nlayer {i}:")
				f.write(", ".join(f"\n  neuron {j}:\n       {[w for w in neuron.weights]}" for j, neuron in enumerate(layer.neurons)))
			f.write("\n-------------------------------------------------------------------------\n")"""

	nr = random.randint(lower, upper)
	agents, games = new_generation(agents, nr)

"""
INPUTS = [1]

network = NeuralNetwork(len(INPUTS), [3, 2], 5)
print(network.process(INPUTS, sigmoid))
network.mutate()
print(network.process(INPUTS, sigmoid))
"""
