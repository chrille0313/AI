from queue import Queue
from enum import Enum


class EventType(Enum):
	QUIT = 0
	UPDATE = 1


class Event:
	def __init__(self, type: EventType, **kwargs):
		self.type = type
		self.__dict__.update(kwargs)

	def __repr__(self):
		return f"Event({self.type}, {self.__dict__})"


class EventDispatcher:
	def __init__(self):
		self._listeners: dict[EventType, set] = {}

	def add_listener(self, event_type: EventType, listener: callable):
		if event_type not in self._listeners:
			self._listeners[event_type] = set()

		self._listeners[event_type].add(listener)

	def remove_listener(self, event_type: EventType, listener: callable):
		if event_type not in self._listeners or listener not in self._listeners[event_type]:
			return

		self._listeners[event_type].remove(listener)

	def dispatch_event(self, event: Event):
		if event.type not in self._listeners:
			return

		for listener in self._listeners[event.type]:
			listener(event)


class EventManager:
	def __init__(self):
		self._event_queue = Queue()
		self._event_dispatcher = EventDispatcher()

	def queue_event(self, event):
		self._event_queue.put(event)

	def dispatch_event(self, event):
		self._event_dispatcher.dispatch_event(event)

	def dispatch_events(self):
		while not self._event_queue.empty():
			event = self._event_queue.get()
			self._event_dispatcher.dispatch_event(event)

	def add_listener(self, event_type, listener):
		self._event_dispatcher.add_listener(event_type, listener)

	def remove_listener(self, event_type, listener):
		self._event_dispatcher.remove_listener(event_type, listener)