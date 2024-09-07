import pygame
import random
from data.src.utils.utils import wait


class Ripple:

    def __init__(self, position):
        self.width = 5
        self.max_width = 150
        self.alive = True
        self.position = [int(x / 4) for x in position]
        self.max_life = 170
        self.life = self.max_life
        self.rect = pygame.Rect(*position, self.width, self.width / 2)
        self.speed = 100
        self.new_ripple = True

    def update(self, dt):
        self.width += dt * self.speed * 1.5 * 3
        self.life -= 1
        if self.life <= 0 or self.width >= self.max_width:
            self.alive = False
        self.position[0] -= dt * self.speed * 1.5 * 3

    def draw(self, surface):
        rect = pygame.Rect(self.position[0] + self.width / 2, self.position[1] - self.width / 4, self.width,
                           self.width / 2)
        pygame.draw.ellipse(surface, (123, 66, 35), rect, random.randint(1, 2))


class Crack:

    def __init__(self, position, game):
        self.position = [x / 4 for x in position]
        self.num_of_crack = 2
        self.max_num_of_cracks = 10
        self.positions = []
        self.alive = True
        self.timer = pygame.time.get_ticks()
        self.game = game
        self.num_of_cracks = 6
        self.cracks = []
        self.generate_crack()
        self.bad_ground_timer = None
        self.dupa = True
        self.chuj = True
        self.final_timer = 0

    def generate_crack(self):
        for i in range(self.num_of_cracks):
            x, y = self.position[0], self.position[1]
            positions = [self.position]
            for i in range(self.max_num_of_cracks):
                x += random.randint(-7, 7)
                y += random.randint(-7, 7)
                positions.append([x, y])
            self.cracks.append(positions)

    def repair_floor(self):
        self.cracks = [crack[:-1] for crack in self.cracks if len(crack) > 2]

    def draw(self, surface):
        for crack in self.cracks:
            if self.num_of_crack >= 2:
                pygame.draw.lines(surface, (123, 66, 35), points=crack[:int(self.num_of_crack)], width=1, closed=False)

    def update(self, dt):
        if not self.dupa and wait(self.game, self.final_timer, 2000):
            self.chuj = False
        if not self.alive and self.num_of_crack >= 3 and wait(self.game, self.bad_ground_timer, 500):
            self.num_of_crack -= dt * random.randint(1, 10)
        if self.num_of_crack >= self.max_num_of_cracks and self.dupa:
            self.alive = False
            self.bad_ground_timer = pygame.time.get_ticks()
            self.dupa = False
            self.final_timer = pygame.time.get_ticks()
        if wait(self.game, self.timer, 50) and self.alive:
            self.num_of_crack += dt * 25


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

    def delete_dead_ripples(self):
        self.ripples = [ripple for ripple in self.ripples if ripple.alive]

    def draw(self, surface):
        for ripple in self.ripples:
            ripple.draw(surface)
        self.crack.draw(surface)

    def generate_ripples(self):
        if self.number_of_ripples < self.max_ripples:
            if len(self.ripples) == 1 and self.ripples[0].life <= self.ripples[0].max_life /  1.05:
                self.ripples.append(Ripple(self.center))
                self.number_of_ripples += 1
            elif 2 <= len(self.ripples) <= self.max_ripples:
                for ripple1, ripple2 in zip(self.ripples, self.ripples[1:]):
                    if ripple1.life <= ripple1.max_life / 1.05 and ripple1.new_ripple:
                        self.ripples.append(Ripple(self.center))
                        ripple1.new_ripple = False
                        self.number_of_ripples += 1

    def update(self, dt):
        self.delete_dead_ripples()
        self.generate_ripples()
        for ripple in self.ripples:
            ripple.update(dt)
        if self.crack.chuj:
            self.crack.update(dt)
        else:
            self.alive = False
