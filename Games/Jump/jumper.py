class Jumper:
	def __init__(self, pos=(0, 0), size=1, vel=(0, 0), jumpVel=2):
		self.pos = list(pos)
		self.vel = list(vel)
		self.jumpVel = jumpVel
		self.size = size

	def jump(self):
		self.vel[1] = self.jumpVel

	def update(self):
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]
