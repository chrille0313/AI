import numpy as np
from copy import deepcopy
from typing import List

from snake import Snake
from game import SnakeGame
from players import RandomPlayer, GeneticPlayer
from settings import BOARD_SIZE, VISION


def create_population(populationSize: int) -> List[GeneticPlayer]:
	return [GeneticPlayer(Snake(), VISION) for _ in range(populationSize)]


def reproduce(population: List[GeneticPlayer], probabilities: List[float]) -> List[GeneticPlayer]:
	newPopulation = np.random.choice(population, len(population), p=probabilities)

	for i, agent in enumerate(newPopulation):
		mutatedAgent = deepcopy(agent)
		mutatedAgent.score = 0
		mutatedAgent.brain.mutate(0.05)
		newPopulation[i] = mutatedAgent

	return newPopulation


def new_generation(population: List[GeneticPlayer]) -> List[GeneticPlayer]:
	worstFitness = min(population, key=lambda a: a.fitness).fitness
	probs = np.array([(agent.fitness - worstFitness)**2 for agent in population])
	probSum = probs.sum()
	probs = probs / probSum if probSum != 0 else np.full(len(probs), 1 / len(probs))
	return reproduce(population, probs)


def display_agent(agent: GeneticPlayer, fps: int):
	agentRepresentation = GeneticPlayer(Snake(), agent.vision)
	agentRepresentation.brain.layers = agent.brain.layers
	SnakeGame(BOARD_SIZE, agentRepresentation, display=True, displayFPS=fps, windowSize=(400, 400)).run()


if __name__ == '__main__':
	generations = 1_000_000
	populationSize = 100
	population = create_population(populationSize)

	for generation in range(generations):
		print(f"Training Generation {generation}...")
		bestAgent = None

		for agent in population:
			game = SnakeGame(BOARD_SIZE, agent)
			game.run()

			if bestAgent is None or agent.fitness > bestAgent.fitness:
				bestAgent = agent

			"""if agent.fitness >= 4:
				print(f"Found agent with high fitness ({agent.fitness})! Displaying...")
				display_agent(agent, 60)"""

		if generation % 10 == 0:
			print(f"---------- Generation {generation} ----------")
			print(f"Best agent score: {bestAgent.score}")

			display_agent(bestAgent, 15)

		population = new_generation(population)

