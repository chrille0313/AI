import pygame
from lib.colors import Colors
from numpy import degrees, radians, arctan2, sin, cos


def draw_circle(pos, radius, color=Colors.white):
    pygame.draw.circle(pygame.display.get_surface(), color, pos, radius)


def draw_line(start, end, color=Colors.white):
    pygame.draw.line(pygame.display.get_surface(), color, start, end)


def draw_rect(pos, size, color=Colors.white, hollow=False):
    pygame.draw.rect(pygame.display.get_surface(), color, (*pos, *size), hollow)


def draw_arrow(start, end, trirad=1, lcolor=Colors.white, tricolor=Colors.white):
    pygame.draw.line(pygame.display.get_surface(), lcolor, start, end)
    rotation = degrees(arctan2(start[1] - end[1], end[0] - start[0])) + 90
    pygame.draw.polygon(pygame.display.get_surface(),
                        tricolor,
                        ((end[0] + trirad * sin(radians(rotation)), end[1] + trirad * cos(radians(rotation))),
                         (end[0] + trirad * sin(radians(rotation-120)), end[1] + trirad * cos(radians(rotation - 120))),
                         (end[0] + trirad * sin(radians(rotation+120)), end[1] + trirad * cos(radians(rotation + 120)))))