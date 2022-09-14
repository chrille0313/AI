from settings import MOVES, RIGHT


class Snake:
	def __init__(self, pos=(0, 0), dir=RIGHT, length=3):
		self.pos = pos
		self.dir = dir
		self.length = length
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
		return len(set(self.body)) != len(self.body) or (
				worldSize is not None and not (0 <= self.pos[0] < worldSize[0] and 0 <= self.pos[1] < worldSize[1]))