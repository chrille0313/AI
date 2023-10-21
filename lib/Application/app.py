import time
from time import perf_counter

from lib.Application.events import EventManager, Event, EventType


class App:
	def __init__(self, fps: float = 0):
		self.fps = fps
		self.running = False

		self._event_manager = EventManager()
		self._event_manager.add_listener(EventType.QUIT, self._quit)

	def run(self):
		self.running = True
		self.__main_loop()

	def _quit(self):
		self.running = False

	def __main_loop(self):
		while self.running:
			startTime = perf_counter()
			self._event_manager.queue_event(Event(EventType.UPDATE))
			self._event_manager.dispatch_events()

			if self.fps != 0:
				sleepTime = max(0.0, (1 / self.fps - (perf_counter() - startTime)))
				# print(sleepTime)
				# print(1 / self.fps - (perf_counter() - startTime))
				time.sleep(sleepTime)

			# endTime = perf_counter()

			# print(startTime, endTime, endTime - startTime, sleepTime)

	def add_listener(self, event_type: EventType, listener: callable):
		self._event_manager.add_listener(event_type, listener)

	def remove_listener(self, event_type: EventType, listener: callable):
		self._event_manager.remove_listener(event_type, listener)

	def queue_event(self, event: Event):
		self._event_manager.queue_event(event)


if __name__ == '__main__':
	app = App(60)
	app.run()

