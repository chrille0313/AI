import pygame
from pygame import Vector2
import numpy as np
from numpy import degrees, radians, sin, cos, arctan2
import random
from lib.colors import Colors


def draw_circle(pos, radius, color=Colors.white):
    pygame.draw.circle(pygame.display.get_surface(), color, pos, radius)


def draw_line(start, end, color=Colors.white):
    pygame.draw.line(pygame.display.get_surface(), color, start, end)


def draw_arrow(start, end, trirad=1, lcolor=Colors.white, tricolor=Colors.white):
    pygame.draw.line(pygame.display.get_surface(), lcolor, start, end)
    rotation = degrees(arctan2(start[1] - end[1], end[0] - start[0])) + 90
    pygame.draw.polygon(pygame.display.get_surface(),
                        tricolor,
                        ((end[0] + trirad * sin(radians(rotation)), end[1] + trirad * cos(radians(rotation))),
                         (end[0] + trirad * sin(radians(rotation-120)), end[1] + trirad * cos(radians(rotation - 120))),
                         (end[0] + trirad * sin(radians(rotation+120)), end[1] + trirad * cos(radians(rotation + 120)))))


# def bound_check(pos: Vector2, size: float = 0, top=0, left=0, down=WINDOW_H, right=WINDOW_W):
#     return pos.y - size >= top, pos.x - size >= left, pos.y + size <= down, pos.x + size <= right


class Particle:
    def __init__(self, x, y, charge=1, mass=10, velX=0, velY=0, accX=0, accY=0):
        self.pos = Vector2(x, y)
        self.velocity = Vector2(velX, velY)
        self.acceleration = Vector2(accX, accY)
        self.charge = charge
        self.mass = mass
        self.color = (0, 0, max(255, charge)) if charge <= 0 else (max(255, -charge), 0, 0)

    def draw(self):
        draw_circle(self.pos, self.mass, self.color)

    def simulate(self):
        self.velocity += self.acceleration
        self.pos += self.velocity


def affect(particle1: Particle, particle2: Particle, k=1):
    delta = particle2.pos - particle1.pos
    F = k * particle1.charge * particle2.charge / delta.magnitude_squared()
    dir = delta.normalize()
    return -dir * F / particle1.mass


class VectorPointer:
    def __init__(self, x, y, color=Colors.white, sprite=None):
        self.pos = Vector2(x, y)
        self.vector = Vector2(x, y)
        self.sprite = sprite
        self.color = color

    def update(self, affectors, affectorClass, affectFunction):
        self.vector = pygame.Vector2(0, 0)
        p = affectorClass(self.pos.x, self.pos.y)

        for affector in affectors:
            self.vector += affectFunction(p, affector)

    def draw(self):
        draw_arrow(self.pos, self.pos + self.vector.normalize() * 10, 3)
        # draw_line(self.pos, self.pos + self.vector.normalize() * 10)


class VectorField:
    def __init__(self, sizeX, sizeY, density):
        self.size = Vector2(sizeX, sizeY)
        self.density = density

        self.vectors = [VectorPointer(x * density, y * density, Particle) for y in range(int(sizeY/density)) for x in range(int(sizeX/density))]

    def draw(self):
        for vector in self.vectors:
            vector.draw()


class App:
    def __init__(self, windowW, windowH):
        pygame.init()

        self.windowSize = self.windowW, self.windowH = windowW, windowH
        self.window = pygame.display.set_mode(self.windowSize)

        self.vectorField = VectorField(windowW, windowH, 20)

        self.particles = []

        for i in range(4):
            self.particles.append(
                Particle(random.randint(0, windowW), random.randint(0, windowH), 10 if i % 2 != 0 else -10))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def draw(self):
        self.window.fill(Colors.black)

        self.vectorField.draw()

        for particle in self.particles:
            particle.draw()

        pygame.display.update()

    def main_loop(self):
        while True:
            self.events()

            for particle1 in self.particles:
                for particle2 in self.particles:
                    if particle1 != particle2:
                        particle1.velocity += affect(particle1, particle2)
                        particle2.velocity += affect(particle2, particle1)

            for particle in self.particles:
                particle.simulate()

            for vector in self.vectorField.vectors:
                vector.update(self.particles, Particle, affect)

            self.draw()


if __name__ == '__main__':
    app = App(1280, 720)
    app.main_loop()
