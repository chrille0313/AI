import random

from jumper import Jumper


class Player:
	def __init__(self, jumper: Jumper):
		self.jumper = jumper
		self.score = 0
		self.framesSurvived = 0
		self.possibleMoves = [None, self.jumper.jump]

	@property
	def pos(self):
		return self.jumper.pos

	@pos.setter
	def pos(self, value):
		self.jumper.pos = value

	@property
	def vel(self):
		return self.jumper.vel

	@vel.setter
	def vel(self, value):
		self.jumper.vel = value

	@property
	def size(self):
		return self.jumper.size

	def jump(self):
		self.jumper.jump()

	def update(self):
		self.framesSurvived += 1
		self.jumper.update()

	def get_move(self, *args, **kwargs):
		return None


class RandomPlayer(Player):
	def __init__(self, jumper):
		super().__init__(jumper)

	def get_move(self):
		return random.choice(self.possibleMoves)
