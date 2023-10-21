from game import JumpGame
from jumper import Jumper
from players import RandomPlayer, Player

from settings import JUMP_VELOCITY

if __name__ == "__main__":
	JumpGame(RandomPlayer(Jumper(jumpVel=JUMP_VELOCITY, size=40))).run()
