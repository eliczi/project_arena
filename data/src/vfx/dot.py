import pygame
import random
from pygame.math import Vector2


class Dot:

    def __init__(self, position):
        self.position = [p / 4 for p in position]
        self.alive = True
        self.radius = 5
        self.rate_of_growth = 19


    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), self.position, self.radius)

    def update(self, dt):
        self.radius -= self.rate_of_growth * dt
        if self.radius <= 0:
            self.alive = False