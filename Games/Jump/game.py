import time
import random

from lib.Application import App
from lib.Application.events import EventType, Event

from players import Player
from obstacle import Obstacle

from settings import GRAVITY


def distance_squared(pos1, pos2):
	return (pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2


class JumpGame(App):
	def __init__(self, player: Player, scrollSpeed=15, obstacleSpawnRate=2, obstacleMinSize=40, obstacleMaxSize=50, maxObstacles=100, gravity=0.1, worldSize=(800, 600), fps=0):
		super().__init__(fps)
		self.add_listener(EventType.UPDATE, self.on_update)

		# Game State
		self.gravity = gravity
		self.worldX, self.worldY = worldSize
		self.groundLevel = self.worldY * 0.1

		self.player = player
		self.player.pos = [0, self.groundLevel + self.player.size]

		self.obstacles = []
		self.obstacleSpawnPos = self.player.pos[0] + self.player.size + obstacleMaxSize + self.worldX, self.groundLevel
		self.obstacleSpawnRate = obstacleSpawnRate
		self.obstacleMinSize, self.obstacleMaxSize = obstacleMinSize, obstacleMaxSize
		self.minObstacleSpacing = self.player.size * 1.1
		self.maxClearedObstacles = maxObstacles
		self.clearedObstacles = 0
		self.latestObstacleSpawnTime = time.time()
		self.scrollSpeed = scrollSpeed

	def is_colliding(self, obstacle):
		return distance_squared(self.player.pos, obstacle.pos) <= (self.player.size + obstacle.size)**2

	def collision_check(self):
		return any(self.is_colliding(obstacle) for obstacle in self.obstacles)

	def should_spawn_obstacle(self):
		return time.time() - self.latestObstacleSpawnTime >= self.obstacleSpawnRate

	def spawn_obstacle(self):
		newObstacleRadius = random.randint(self.obstacleMinSize, self.obstacleMaxSize)
		newObstaclePos = [self.obstacleSpawnPos[0], self.obstacleSpawnPos[1] + newObstacleRadius]

		if len(self.obstacles) != 0:
			furthestObstacle = self.obstacles[-1]
			newXPos = furthestObstacle.pos[0] + furthestObstacle.size + newObstacleRadius + self.minObstacleSpacing

			if newXPos >= newObstaclePos[0]:
				newObstaclePos[0] = newXPos

		self.obstacles.append(Obstacle(newObstaclePos, newObstacleRadius))

		self.latestObstacleSpawnTime = time.time()

	def update_obstacles(self):
		if self.should_spawn_obstacle():
			self.spawn_obstacle()

		for obstacle in self.obstacles:
			obstacle.pos[0] -= self.scrollSpeed

			if obstacle.pos[0] + obstacle.size < self.player.pos[0] - self.player.size:
				self.obstacles.remove(obstacle)


	def update_player(self):
		move = self.player.get_move()

		if move is not None and self.player.pos[1] == 0:
			self.player.jump()

		self.player.vel[1] -= GRAVITY
		self.player.update()

		if self.player.pos[1] <= 0:
			self.player.pos[1] = 0

	def on_update(self, event):
		print("update")

		self.update_obstacles()

		self.update_player()

		if self.collision_check():
			self.dispatch_event(Event(EventType.QUIT))

	"""
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
		draw_circle((self.playerLeftMargin, self.windowH - self.groundLevel - (self.player.pos[1] + self.player.size) * self.scale), self.player.size * self.scale, Colors.red)

	def draw_obstacles(self):
		for obstacle in self.obstacles:
			draw_circle((obstacle.pos[0] * self.scale + self.playerLeftMargin, self.windowH - self.groundLevel - (obstacle.pos[1] + obstacle.size) * self.scale), obstacle.size * self.scale, Colors.green)
	"""
