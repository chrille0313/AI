from enum import Enum

# TODO: Enum

BOARD_SIZE = (25, 25)
VISION = 10


class Directions:
	UP = (0, 1)
	RIGHT = (1, 0)
	DOWN = (0, -1)
	LEFT = (-1, 0)
	ALL = (UP, RIGHT, DOWN, LEFT)

	@staticmethod
	def get_next_direction(dir, right=True):
		return Directions.ALL[(Directions.ALL.index(dir) + (1 if right else -1)) % len(Directions.ALL)]


EMPTY, FOOD, SNAKE = 0, 1, -1
