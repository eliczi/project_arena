import pygame
import random


class Particle:

    def __init__(self):
        self.position = [random.randint(400, 5000), random.randint(-800, 0)]
        self.d = random.randint(3, 6)
        self.size = (self.d, self.d)

class Sand:
    color  = (230, 150, 138)

    def __init__(self, game):
        self.game = game
        self.wind = [-5, 1]
        self.sand_particles = []
        self.alive = True
        self.add_particle(Particle())

    def add_particle(self, particle):
        if random.randint(1, 10) == 5:
            self.sand_particles.append(particle)

    def update_wind(self):
        change_vector = [random.randint(-1, 0) / 100, random.randint(0, 1) / 100]
        self.wind = [sum(x) for x in zip(change_vector, self.wind)]

    def update(self):
        #self.update_wind()
        self.add_particle(Particle())
        for particle in self.sand_particles:
            particle.position = [sum(x) for x in zip(particle.position, self.wind)]

    def draw(self):
        for particle in self.sand_particles:
            pygame.draw.rect(self.game.screen, self.color,
                             (particle.position[0], particle.position[1], particle.size[0], particle.size[1]))
