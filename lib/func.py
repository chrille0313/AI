import pygame
from pygame import Vector2

import numpy as np
from numpy import degrees, radians, sin, cos, arctan2, random

from colors import Colors
from particle import Particle
from vector import VectorField


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



def affect(particle1: Particle, particle2: Particle, k=1):
    delta = particle2.pos - particle1.pos
    F = k * particle1.charge * particle2.charge / delta.magnitude_squared()
    direction = delta.normalize()
    return -direction * F / particle1.mass
