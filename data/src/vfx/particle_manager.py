import pygame
from .sand import Sand


class ParticleManager:

    def __init__(self, game):
        self.game = game
        self.particles = []

    def add_particle(self, particle):
        self.particles.append(particle)

    def remove_particles(self):
        for particle in self.particles:
            if particle.alive is False:
                self.particles.remove(particle)

    def update(self):
        for particle in self.particles:
            particle.update(self.game.time.dtf())
        self.remove_particles()

    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
