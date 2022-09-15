import random

from jumper import Jumper


class Player:
	def __init__(self, jumper: Jumper):
		self.jumper = jumper
		self.score = 0
		self.framesSurvived = 0
		self.possibleMoves = [None, self.jumper.jump]

	def get_move(self, *args, **kwargs):
		return None


class RandomPlayer(Player):
	def __init__(self, jumper):
		super().__init__(jumper)

	def get_move(self):
		return random.choice(self.possibleMoves)
