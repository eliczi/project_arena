import pygame
from data.src.entities.enemies.enemy import Enemy
from data.src.entities.enemies.necromancer import Necromancer
from data.src.entities.enemies.crying_skeleton import CryingSkeleton

class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.enemies = []
        self.dupa = 0

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def draw(self, surface):
        for enemy in self.enemies:
            enemy.draw(surface)

    def remove_dead_enemies(self):
        self.enemies = [enemy for enemy in self.enemies if enemy.dead is False]

    def update(self):
        self.debug()
        for enemy in self.enemies:
            enemy.update()
        self.remove_dead_enemies()

    def debug(self):
        if pygame.mouse.get_pressed()[2] and pygame.time.get_ticks() - self.dupa > 1000:
            self.dupa = pygame.time.get_ticks()
            pos = pygame.mouse.get_pos()
            self.add_enemy(CryingSkeleton(self.game, pos))
