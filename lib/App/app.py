import pygame
from lib.colors import Colors

"""
class GUI:
	def __init__(self, windowSize):
		pass

	def quit(self):
		pass

	def update(self):
		pass

	def events(self):
		pass

	def draw(self):
		pass


class PygameGUI(GUI):
	def __init__(self, windowSize):
		super().__init__(windowSize)
		pygame.init()
		self.window = pygame.display.set_mode(windowSize)
"""


class App:
	def __init__(self, windowSize, fps=60, render=True):
		self.windowSize = self.windowW, self.windowH = windowSize
		self.windowCenter = (self.windowW / 2, self.windowH / 2)

		self.clock = pygame.time.Clock()
		self.fps = fps
		self.running = True
		self.render = render

	@property
	def render(self):
		return self._render

	@render.setter
	def render(self, val):
		self._render = val

		if self.render:
			pygame.init()
			self.window = pygame.display.set_mode(self.windowSize)
		else:
			pygame.display.quit()
			pygame.quit()

		self.on_set_render(val)

	def run(self):
		self.main_loop()

	def events(self):
		if self.render:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

		self.on_events()

	def draw(self):
		if self.render:
			self.window.fill(Colors.black)

		self.on_draw()

		if self.render:
			pygame.display.update()

	def main_loop(self):
		while self.running:
			self.events()

			self.on_update()

			self.draw()

			self.clock.tick(self.fps)

	def on_update(self):
		pass

	def on_draw(self):
		pass

	def on_events(self):
		pass

	def on_set_render(self, val):
		pass


if __name__ == '__main__':
	app = App((1280, 720), 1)
	app.run()
