import time
import random

from players import Player
from obstacle import Obstacle

from settings import GRAVITY

from lib.Application import App
from lib.Application.GUI import Colors
from lib.Application.GUI.draw import draw_line, draw_circle


class JumpGame(App):
	def __init__(self, player: Player, scrollSpeed=0.1, obstacleSpawnRate=2, obstacleMinSize=3, obstacleMaxSize=10, maxObstacles=100, gravity=0.1, display=False, displayFPS=60, windowSize=(800, 800)):
		# GUI
		self.display = display
		self.displayFps = displayFPS
		super().__init__(windowSize, fps=displayFPS, render=display)
		self.groundLevel = self.windowH * 0.1
		self.playerLeftMargin = self.groundLevel
		self.scale = self.windowH / 25

		# Game State
		self.player = player
		self.player.pos = [0, 0]

		self.obstacles = []
		self.scrollSpeed = scrollSpeed
		self.obstacleSpawnPos = self.player.jumper.pos[0] + player.jumper.size + obstacleMaxSize * 2 * 10, 0
		self.obstacleSpawnRate = obstacleSpawnRate
		self.obstacleMinSize, self.obstacleMaxSize = obstacleMinSize, obstacleMaxSize
		self.minObstacleSpacing = self.player.jumper.size
		self.maxClearedObstacles = maxObstacles
		self.clearedObstacles = 0
		self.latestObstacleSpawnTime = time.time()

		self.gravity = gravity

	def is_colliding(self, obstacle):
		return abs(self.player.jumper.pos[0] - obstacle.pos[0])**2 + abs(self.player.jumper.pos[1] - obstacle.pos[1])**2 <= (self.player.jumper.size + obstacle.size)**2

	def collision_check(self):
		return any(self.is_colliding(obstacle) for obstacle in self.obstacles)

	def should_spawn_obstacle(self):
		return time.time() - self.latestObstacleSpawnTime >= self.obstacleSpawnRate

	def spawn_obstacle(self):
		newObstacleRadius = random.randint(self.obstacleMinSize, self.obstacleMaxSize)

		if len(self.obstacles) != 0:
			furthestObstacle = self.obstacles[-1]
			distToFurthestObstacle = max((furthestObstacle.pos[0] + furthestObstacle.size) - (self.obstacleSpawnPos[0] - newObstacleRadius), -self.minObstacleSpacing)
			newObstacleSpawnPos = [distToFurthestObstacle + self.minObstacleSpacing, 0]
		else:
			newObstacleSpawnPos = list(self.obstacleSpawnPos)

		self.obstacles.append(Obstacle(newObstacleSpawnPos, newObstacleRadius))

		self.latestObstacleSpawnTime = time.time()

	def update_obstacles(self):
		for obstacle in self.obstacles:
			obstacle.pos[0] -= self.scrollSpeed

			if obstacle.pos[0] + obstacle.size < self.player.jumper.size:
				self.obstacles.remove(obstacle)

		if self.should_spawn_obstacle():
			self.spawn_obstacle()

	def update_player(self):
		move = self.player.get_move()

		if self.player.jumper.pos[1] == 0 and move is not None:
			self.player.jumper.jump()

		self.player.jumper.vel[1] -= GRAVITY
		self.player.jumper.update()

		if self.player.jumper.pos[1] <= 0:
			self.player.jumper.pos[1] = 0

	def on_update(self):
		self.update_obstacles()

		self.update_player()

		if self.collision_check():
			self.quit_application()

	def on_draw(self):
		if self.display:
			self.draw_ground()
			self.draw_player()
			self.draw_obstacles()

	def on_set_render(self, val):
		self.fps = self.displayFps if self.display else 0

	def draw_ground(self):
		draw_line((0, self.windowH - self.groundLevel), (self.windowW, self.windowH - self.groundLevel))

	def draw_player(self):
		draw_circle((self.playerLeftMargin, self.windowH - self.groundLevel - (self.player.jumper.pos[1] + self.player.jumper.size) * self.scale), self.player.jumper.size * self.scale, Colors.red)

	def draw_obstacles(self):
		for obstacle in self.obstacles:
			draw_circle((obstacle.pos[0] * self.scale + self.playerLeftMargin, self.windowH - self.groundLevel - (obstacle.pos[1] + obstacle.size) * self.scale), obstacle.size * self.scale, Colors.green)

