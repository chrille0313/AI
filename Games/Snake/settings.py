from enum import Enum

# TODO: Enum

BOARD_SIZE = (25, 25)
VISION = 10
DIRECTIONS = UP, RIGHT, DOWN, LEFT = (0, 1), (1, 0), (0, -1), (-1, 0)


class Directions:
	UP = (0, 1)
	RIGHT = (1, 0)
	DOWN = (0, -1)
	LEFT = (-1, 0)
	ALL = (UP, RIGHT, DOWN, LEFT)


EMPTY, FOOD, SNAKE = 0, 1, -1
