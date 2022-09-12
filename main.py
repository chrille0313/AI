import random

import numpy as np

from lib.App.app import App
from lib.draw import draw_rect
from lib.colors import Colors
from lib.AI.neural_network import NeuralNetwork
from lib.AI.func import sigmoid

MOVES = UP, RIGHT, DOWN, LEFT = (0, 1), (1, 0), (0, -1), (-1, 0)
EMPTY, FOOD = 0, 1


class Snake:
    def __init__(self, pos, dir, length, size=(10, 10)):
        self.pos = pos
        self.dir = dir
        self.length = length
        self.size = size
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

    def draw(self):
        for i, cell in enumerate(self.body):
            draw_rect((cell[0] * self.size[0], cell[1] * self.size[1]), self.size,
                      Colors.yellow if i == 0 else Colors.white)


class Player:
    def __init__(self, snake):
        self.snake = snake
        self.points = 0

        self.possibleMoves = [None, self.snake.turn_left, self.snake.turn_right]

    def get_move(self, *args, **kwargs):
        pass


class RandomPlayer(Player):
    def __init__(self, snake):
        super().__init__(snake)

    def get_move(self):
        return random.choice(self.possibleMoves)


class GeneticPlayer(Player):
    def __init__(self, snake, vision=10):
        super().__init__(snake)

        self.brain = NeuralNetwork([1, 1, 3])
        self.vision = vision

    def process_board(self, board):
        processedBoard = []

        for row in range(self.snake.pos[1] - self.vision, self.snake.pos[1] + self.vision):
            if 0 <= row < len(board):
                processedBoard.append([board[col] if 0 <= col < len(board[0]) else -1 for col in
                                       range(self.snake.pos[0] - self.vision, self.snake.pos[0] + self.vision)])
            else:
                processedBoard.append([-1] * self.vision)

        return processedBoard

    def get_move(self, board):
        inputVector = self.process_board(board)
        output = self.brain.process(inputVector, sigmoid)
        return self.possibleMoves[np.argmax(output)]


class SnakeGame(App):
    def __init__(self, gridSize, player=None, foodCount=4, maxTurns=100, display=False, displayFPS=10):
        # GUI
        self.display = display
        self.displayFps = displayFPS
        super().__init__((400, 400), fps=displayFPS, render=display)

        # Game State
        self.gridSize = gridSize
        self.maxTurns = maxTurns
        self.turn = 0

        self.player = player if player is not None else RandomPlayer(
            Snake(
                (self.gridSize[0] // 2, self.gridSize[1] // 2),
                RIGHT,
                3,
                (self.windowW / self.gridSize[0], self.windowH / self.gridSize[1])
            ))

        self.food = set()
        self.food = {self.get_random_food() for _ in range(foodCount)}

    def get_random_food(self):
        pos = None

        while pos is None or pos in self.food:
            pos = random.randint(0, self.gridSize[0] - 1), random.randint(0, self.gridSize[1] - 1)

        return pos

    def on_update(self):
        move = self.player.get_move()

        if move is not None:
            move()

        self.player.snake.move()

        if self.player.snake.has_collided(self.gridSize):
            self.running = False
        elif self.player.snake.body[0] in self.food:
            self.food.remove(self.player.snake.body[0])
            self.player.snake.extend_body()
            self.player.points += 1
            self.food.add(self.get_random_food())

    def on_draw(self):
        if self.display:
            self.draw_board()
            self.player.snake.draw()

    def on_set_render(self, val):
        self.fps = self.displayFps if self.display else 0

    def draw_board(self):
        for f in self.food:
            scaleX, scaleY = self.windowW / self.gridSize[0], self.windowH / self.gridSize[1]
            draw_rect((f[0] * scaleX, f[1] * scaleY), (scaleX, scaleY), Colors.red)


if __name__ == '__main__':
    SnakeGame((25, 25), display=False).run()
    SnakeGame((25, 25), display=True).run()
