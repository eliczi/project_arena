import pygame
import random
from data.src.entities.entity import Character
from data.src.entities.player.attack import Attack
from data.src.entities.player.slash import Slash
from data.src.entities.enemies.enemy import Enemy   

class CryingSkeleton(Enemy):
    name = 'crying_skeleton'
    speed = 200
    path = f'data/assets/characters/{name}/'
    max_hp = 100
    hp = max_hp

    def __init__(self, game, position):
        Character.__init__(self, game)
        self.image = pygame.transform.flip(self.image,
                                            1, 0).convert_alpha()
        self.rect.topleft = position
        self.update_hitbox()
        self.roll = False
        self.position = [self.rect.topleft[0], self.rect.topleft[1]]
        self.hurt_timer = 0
        self.attack_timer = 0
        self.game.particle_manager.add_particle(self.shadow)


    # def attack(self):
    #     if self.can_attack and wait(self.game,  self.attack_timer,500):
    #     self.game.particle_manager.add_particle(Slash(self, self))
    #     #Maybe add different effects for different enemies

    
