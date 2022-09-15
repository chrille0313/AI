import pygame
from lib.Application.GUI.colors import Colors

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

# TODO: Decorator for run


class App:
	def __init__(self, windowSize, fps=0, render=True):
		self.windowSize = self.windowW, self.windowH = windowSize
		self.windowCenter = (self.windowW / 2, self.windowH / 2)

		self.clock = pygame.time.Clock()
		self.fps = fps
		self.running = False
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
		self.running = True
		self.__main_loop()

	def __events(self):
		if self.render:
			self.__gui_events()

		self.on_events()

	def __gui_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.quit_application()

	def __draw(self):
		if self.render:
			self.window.fill(Colors.black)

		self.on_draw()

		if self.render:
			pygame.display.update()

	def __main_loop(self):
		while self.running:
			self.__events()

			self.on_update()

			self.__draw()

			self.clock.tick(self.fps)

	def quit_application(self):
		self.running = False

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
