import random
import numpy as np

from abc import abstractmethod

from snake import Snake
from settings import Directions, SNAKE

from lib.AI import NeuralNetwork
from lib.AI.agents import GeneticAgent
from lib.AI.activation_functions import relu, sigmoid


class Player:
	def __init__(self, snake: Snake):
		self.snake = snake
		self.score = 0
		self.turnsSurvived = 0
		self.possibleMoves = [None, self.snake.turn_left, self.snake.turn_right]

	@abstractmethod
	def get_move(self, *args, **kwargs):
		raise Exception("get_move method must be defined!")


class RandomPlayer(Player):
	def __init__(self, snake):
		super().__init__(snake)

	def get_move(self, board):
		return random.choice(self.possibleMoves)


class GeneticPlayer(GeneticAgent, Player):
	def __init__(self, snake, vision=10):
		super().__init__(snake)

		self.vision = vision
		self.brain = NeuralNetwork([(2 * self.vision + 1)**2 + len(Directions.ALL), 20, 12, len(self.possibleMoves)], relu, sigmoid)

	@property
	def fitness(self):
		return self.turnsSurvived + 2**self.score + self.score**2.1 * 500 - 0.25 * self.turnsSurvived**1.3 * self.score**1.2
		# return self.score*self.score

	def process_board(self, board):
		processedBoard = []

		for row in range(self.snake.pos[1] - self.vision, self.snake.pos[1] + self.vision + 1):
			if 0 <= row < len(board):
				processedRow = []
				for col in range(self.snake.pos[0] - self.vision, self.snake.pos[0] + self.vision + 1):
					if not (0 <= col < len(board[0])) or (col, row) in self.snake.body:
						processedRow.append(SNAKE)
					else:
						processedRow.append(board[row][col])
			else:
				processedRow = [SNAKE] * (self.vision * 2 + 1)

			processedBoard.append(processedRow)

		return processedBoard

	def get_move(self, board):
		processedWorld = self.process_board(board)
		inputVector = [item for row in processedWorld for item in row]
		inputVector.extend([1 if direction == self.snake.dir else 0 for direction in Directions.ALL])
		output = self.brain.process(inputVector)
		return self.possibleMoves[np.argmax(output)]
