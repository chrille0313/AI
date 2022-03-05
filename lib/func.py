import pygame
import numpy as np
from numpy import random, deg2rad, rad2deg, sin, cos

from colors import Colors
from draw import draw_arrow, draw_circle, draw_line
from vector import VectorField, VectorPointer
from particle import Particle


# def bound_check(pos: Vector2, size: float = 0, top=0, left=0, down=WINDOW_H, right=WINDOW_W):
#     return pos.y - size >= top, pos.x - size >= left, pos.y + size <= down, pos.x + size <= right


def affect(particle1: Particle, particle2: Particle, k=1):
    delta = particle2.pos - particle1.pos
    F = k * particle1.charge * particle2.charge / delta.magnitude_squared()
    direction = delta.normalize()
    return -direction * F / particle1.mass
