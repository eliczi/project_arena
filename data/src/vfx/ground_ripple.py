import pygame
import random
from data.src.utils.utils import wait


class Ripple:

    def __init__(self, position):
        self.width = 5
        self.alive = True
        self.position = [int(x / 4) for x in position]
        self.life = random.randint(7, 25)
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
            if self.num_of_crack >=2:
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
            self.num_of_crack += dt * 200


class GroundRipple:

    def __init__(self, game, position):
        self.game = game
        self.center = position
        self.ripples = [Ripple(self.center)]
        self.number_of_ripples = 1
        self.max_ripples = random.randint(5, 8)
        self.max_radius = 10
        self.alive = True
        self.generate_ripples = True
        self.crack = Crack(position, self.game)

    def populate_ripples(self):
        for r in range(self.number_of_ripples):
            self.ripples.append(Ripple(self.center))

    def terminate(self):
        return all([not ripple.alive for ripple in self.ripples])

    def draw(self, surface):
        for ripple in self.ripples:
            ripple.draw(surface)
        self.crack.draw(surface)

    def update(self, dt):
        if self.terminate():
            self.generate_ripples = False
        if self.generate_ripples:
            for ripple in self.ripples:
                if ripple.life < 10 and self.number_of_ripples < self.max_ripples:
                    self.number_of_ripples += 1
                    self.ripples.append(Ripple(self.center))
                ripple.update(dt)
        if self.crack.chuj:
            self.crack.update(dt)
        else:
            self.alive = False
