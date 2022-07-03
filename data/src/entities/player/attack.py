import pygame
import random
from .slash import Slash
from pygame.math import Vector2
from data.src.vfx.attack_ready import AttackReady


class Attack:

    def __init__(self, game, player, weapon):
        self.game = game
        self.player = player
        self.weapon = weapon
        self.special_attack_cooldown = 1.5
        self.mouse_timer = self.special_attack_cooldown
        self.init_timer = False
        self.attacks = []
        self.index = 0
        self.timer = 0
        self.special_attack = False
        self.normal_attack = False
        self.normal_attack_timer = 0
        self.dupa = True

    def update_special_timer(self):
        if self.init_timer:
            self.mouse_timer -= self.game.time.dtf()
        else:
            self.mouse_timer = self.special_attack_cooldown
        if self.mouse_timer < 0 and self.dupa:
            self.game.particle_manager.add_particle(AttackReady(self.player.hitbox.topleft, self.player))
            self.dupa = False

    def wait(self, time, amount):
        if pygame.time.get_ticks() - time > amount / self.game.time.game_speed:
            time = pygame.time.get_ticks()
            return True

    def input(self):
        self.update_special_timer()
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.init_timer = True
            if event.type == pygame.MOUSEBUTTONUP and not self.special_attack and self.mouse_timer < 0:
                for par in self.game.particle_manager.particles:
                    if isinstance(par, AttackReady):
                        par.alive = False
                self.init_timer = False
                self.special_attack = True
                self.mouse_timer = self.special_attack_cooldown
                self.dupa = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not self.normal_attack and self.wait(self.normal_attack_timer, 250) and not self.special_attack:
                self.normal_attack_timer = pygame.time.get_ticks()
                self.normal_attack = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.init_timer = False

    def special_attack_update(self):
        if not self.special_attack:
            return
        if self.index == 0:
            self.attacks = [[Slash(self.player, self), 0], [Slash(self.player, self), 150],
                            [Slash(self.player, self), 150],
                            [Slash(self.player, self), 300], [Slash(self.player, self), 75]]
        if self.wait(self.timer, self.attacks[self.index][1]):
            self.timer = pygame.time.get_ticks()
            self.game.particle_manager.add_particle(self.attacks[self.index][0])
            self.index += 1
        if self.index == 5:
            self.special_attack = False
            self.index = 0

    def normal_attack_update(self):
        if self.normal_attack:
            self.game.particle_manager.add_particle(Slash(self.player, self))
            self.normal_attack = False

    def update(self):
        self.update_special_timer()
        self.special_attack_update()
        self.normal_attack_update()
