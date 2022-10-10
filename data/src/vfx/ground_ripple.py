import pygame
import random
from data.src.utils.utils import wait


class Ripple:

    def __init__(self, position):
        self.width = 5
        self.alive = True
        self.position = [int(x / 4) for x in position]
        self.life = random.randint(7, 15)
        self.rect = pygame.Rect(*position, self.width, self.width / 2)
        self.speed = 100

    def update(self, dt):
        self.width += dt * self.speed * 1.5
        self.life -= 0.25
        if self.life <= 0:
            self.alive = False
        self.position[0] -= dt * self.speed * 1.5

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] + self.width / 2, self.position[1] - self.width / 4, self.width,
                           self.width / 2)
        pygame.draw.ellipse(surface, (255, 255, 255), rect, 1)


class Crack:

    def __init__(self, position, game):
        self.position = [x / 4 for x in position]
        self.num_of_crack = 2
        self.max_num_of_cracks = 15
        self.positions = []
        self.generate_crack()
        self.alive = True
        self.timer = pygame.time.get_ticks()
        self.game = game
        self.cracks = []

    def generate_crack(self):
        x, y = self.position[0], self.position[1]
        for i in range(self.max_num_of_cracks):
            x += random.randint(-7, 7)
            y += random.randint(-7, 7)
            self.positions.append([x, y])

    def repair_floor(self):
        self.positions = self.position[:-1]

    def draw(self, surface):
        for crack in self.cracks:
            pygame.draw.lines(surface, (123, 66, 35), points=crack[:self.num_of_crack], width=1, closed=False)

        pygame.draw.lines(surface, (123, 66, 35), points=self.positions[:self.num_of_crack], width=1, closed=False)

    def update(self, dt):
        if self.num_of_crack == self.max_num_of_cracks:
            self.alive = False
        if wait(self.game, self.timer, 50):
            self.num_of_crack += 1


class GroundRipple:

    def __init__(self, game, position):
        self.game = game
        self.center = position
        self.ripples = [Ripple(self.center)]
        self.number_of_ripples = 1
        self.max_ripples = random.randint(5, 8)
        self.max_radius = 10
        self.alive = True
        self.crack = Crack(position, self.game)

    def populate_ripples(self):
        for r in range(self.number_of_ripples):
            self.ripples.append(Ripple(self.center))

    def terminate(self):
        return all([not ripple.alive for ripple in self.ripples])

    def draw(self, surface):
        # for ripple in self.ripples:
        #     ripple.draw(surface)
        self.crack.draw(surface)

    def update(self, dt):
        if self.terminate():
            self.alive = False
        for ripple in self.ripples:
            if ripple.life < 10 and self.number_of_ripples < self.max_ripples:
                self.number_of_ripples += 1
                self.ripples.append(Ripple(self.center))
            ripple.update(dt)
        self.crack.update(dt)
