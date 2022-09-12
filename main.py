import random

import numpy as np

from lib.App.app import App
from lib.draw import draw_rect
from lib.colors import Colors
from lib.AI.neural_network import NeuralNetwork
from lib.AI.func import sigmoid


MOVES = UP, RIGHT, DOWN, LEFT = (0, 1), (1, 0), (0, -1), (-1, 0)
EMPTY, FOOD = 0, 1


class Snake:
	def __init__(self, pos, dir, length, size=(10, 10)):
		self.pos = pos
		self.dir = dir
		self.length = length
		self.size = size
		self.body = [(pos[0] - dir[0] * i, pos[1] - dir[1] * i) for i in range(length)]

	def turn_right(self):
		self.dir = MOVES[(MOVES.index(self.dir) + 1) % len(MOVES)]

	def turn_left(self):
		self.dir = MOVES[(MOVES.index(self.dir) - 1) % len(MOVES)]

	def move(self):
		self.pos = self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]
		prevPos = self.pos

		for i, body in enumerate(self.body):
			self.body[i], prevPos = prevPos, self.body[i]

	def extend_body(self, count=1):
		if len(self.body) > 1:
			dirX, dirY = self.body[-1][0] - self.body[-2][0], self.body[-1][1] - self.body[-2][1]
		else:
			dirX, dirY = -self.dir[0], -self.dir[1]

		for i in range(count):
			self.body.append((self.body[-1][0] + dirX * i, self.body[-1][1] + dirY * i))

	def has_collided(self, worldSize=None):
		return len(set(self.body)) != len(self.body) or (worldSize is not None and not (0 <= self.pos[0] < worldSize[0] and 0 <= self.pos[1] < worldSize[1]))

	def draw(self):
		for i, cell in enumerate(self.body):
			draw_rect((cell[0] * self.size[0], cell[1] * self.size[1]), self.size, Colors.yellow if i == 0 else Colors.white)


class Player:
	def __init__(self, snake):
		self.snake = snake
		self.points = 0

		self.possibleMoves = [None, self.snake.turn_left, self.snake.turn_right]

	def get_move(self, *args, **kwargs):
		pass


class RandomPlayer(Player):
	def __init__(self, snake):
		super().__init__(snake)

	def get_move(self):
		return random.choice(self.possibleMoves)


class GeneticPlayer(Player):
	def __init__(self, snake):
		super().__init__(snake)

		self.brain = NeuralNetwork([1, 1, 3])

	def process_board(self, board):
		return []

	def get_move(self, board):
		inputVector = self.process_board(board)
		output = self.brain.process(inputVector, sigmoid)
		return self.possibleMoves[np.argmax(output)]


class SnakeGame(App):
	def __init__(self, gridSize, playerCount, foodCount=4, display=False, maxTurns=100):
		super().__init__((800, 800), fps=10, render=display)

		self.gridSize = gridSize
		self.playerCount = playerCount
		self.display = display
		self.maxTurns = maxTurns

		self.foodCount = foodCount
		self.turn = 0
		self.snakeSize = 3

		self.players = [RandomPlayer(Snake((self.gridSize[0] // 2, self.gridSize[1] // 2), RIGHT, 3, (self.windowW / self.gridSize[0], self.windowH / self.gridSize[1]))) for _ in range(self.playerCount)]
		self.food = {self.get_random_food() for _ in range(self.foodCount)}

	def get_random_food(self):
		return random.randint(0, self.gridSize[0] - 1), random.randint(0, self.gridSize[1] - 1)

	def on_update(self):
		for player in self.players:
			move = player.get_move()

			if move is not None:
				move()

			player.snake.move()

			if player.snake.has_collided(self.gridSize):
				self.players.remove(player)
			elif player.snake.body[0] in self.food:
				self.food.remove(player.snake.body[0])
				player.snake.extend_body()
				player.points += 1
				self.food.add(self.get_random_food())

	def on_draw(self):
		self.draw_board()

		for player in self.players:
			player.snake.draw()

	def draw_board(self):
		for f in self.food:
			scaleX, scaleY = self.windowW / self.gridSize[0], self.windowH / self.gridSize[1]
			draw_rect((f[0] * scaleX, f[1] * scaleY), (scaleX, scaleY), Colors.red)


if __name__ == '__main__':
	s = SnakeGame((25, 25), 1, display=True)
	s.run()
