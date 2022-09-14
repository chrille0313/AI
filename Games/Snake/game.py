import random
from settings import RIGHT, FOOD, SNAKE, EMPTY

from players import RandomPlayer
from snake import Snake

from lib.Application import App
from lib.Application.GUI import Colors
from lib.Application.GUI.draw import draw_rect


class SnakeGame(App):
	def __init__(self, gridSize, player=None, foodCount=4, maxTurns=100, display=False, displayFPS=10, windowSize=(800, 800)):
		# GUI
		self.display = display
		self.displayFps = displayFPS
		super().__init__(windowSize, fps=displayFPS, render=display)
		self.cellSize = (self.windowW / gridSize[0], self.windowH / gridSize[1])

		# Game State
		self.gridSize = gridSize
		self.maxTurns = maxTurns
		self.turn = 0

		self.player = player if player is not None else RandomPlayer(Snake())
		self.player.snake.pos = (self.gridSize[0] // 2, self.gridSize[1] // 2)
		self.player.snake.dir = RIGHT
		self.player.snake.length = 3

		self.food = set()
		self.food = {self.get_random_food() for _ in range(foodCount)}

		self.board = [[EMPTY for _ in range(self.gridSize[0])] for _ in range(self.gridSize[1])]

		for x, y in self.food:
			self.board[y][x] = FOOD

	def get_random_food(self):
		pos = None

		while pos is None or pos in self.food or pos in self.player.snake.body:
			pos = random.randint(0, self.gridSize[0] - 1), random.randint(0, self.gridSize[1] - 1)

		return pos

	def on_update(self):
		move = self.player.get_move(self.board)

		if move is not None:
			move()

		self.player.snake.move()

		if self.player.snake.has_collided(self.gridSize):
			self.running = False
		elif self.player.snake.body[0] in self.food:
			x, y = self.player.snake.body[0]
			self.food.remove(self.player.snake.body[0])
			self.board[y][x] = EMPTY
			self.player.snake.extend_body()
			self.player.score += 1

			foodPos = self.get_random_food()
			self.food.add(foodPos)
			self.board[foodPos[1]][foodPos[0]] = FOOD

		self.turn += 1
		self.player.turnsSurvived += 1

		if self.turn >= self.maxTurns:
			self.running = False

	def on_draw(self):
		if self.display:
			self.draw_board()
			self.draw_snake()

	def on_set_render(self, val):
		self.fps = self.displayFps if self.display else 0

	def draw_board(self):
		for food in self.food:
			draw_rect((food[0] * self.cellSize[0], food[1] * self.cellSize[1]), self.cellSize, Colors.red)

	def draw_snake(self):
		for i, cell in enumerate(self.player.snake.body):
			draw_rect((cell[0] * self.cellSize[0], cell[1] * self.cellSize[1]), self.cellSize, Colors.yellow if i == 0 else Colors.white)
