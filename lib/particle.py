from pygame import Vector2
from draw import draw_circle


GRAVITY = Vector2(0, 0.001)


class Particle:
    def __init__(self, x, y, charge=1, mass=10, velX=0, velY=0, accX=0, accY=0, shouldSimulate=True):
        self.pos = Vector2(x, y)
        self.velocity = Vector2(velX, velY)
        self.acceleration = Vector2(accX, accY)
        self.charge = charge
        self.mass = mass
        self.shouldSimulate = shouldSimulate
        self.color = (0, 0, max(255, charge)) if charge <= 0 else (max(255, -charge), 0, 0)

    def draw(self):
        draw_circle(self.pos, self.mass, self.color)

    def simulate(self):
        self.velocity += self.acceleration + GRAVITY * self.shouldSimulate
        self.pos += self.velocity

