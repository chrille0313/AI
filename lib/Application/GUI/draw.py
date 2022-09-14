import pygame
from .colors import Colors


def draw_circle(pos, radius, color=Colors.white):
    pygame.draw.circle(pygame.display.get_surface(), color, pos, radius)


def draw_line(start, end, color=Colors.white):
    pygame.draw.line(pygame.display.get_surface(), color, start, end)


def draw_rect(pos, size, color=Colors.white, hollow=False):
    pygame.draw.rect(pygame.display.get_surface(), color, (*pos, *size), hollow)

