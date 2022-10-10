import pygame

from .weapon import Weapon
from data.src.entities.player.attack import Attack
from data.src.vfx.attack_ready import AttackReady
from data.src.entities.player.slash import Slash


class SteelDagger(Weapon):
    name = 'steel_dagger'
    size = (64, 64)

    def __init__(self, game, position, player=None):
        self.path = f'{self.base_path}{self.name}'
        super().__init__(game, self.name, position, player)
        self.damage = 10
        # self.attack = Attack(game, player, weapon=self)
        self.image = pygame.transform.scale(self.image, self.size)
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

    def interact(self):
        self.interaction = False
        self.show_name.reset_line_length()
        self.player = self.game.player
        self.game.object_manager.remove_item(self)
        self.player.items.items['weapon']['item'] = self

    def update_special_timer(self):
        if self.init_timer:
            self.mouse_timer -= self.game.time.dtf()
        else:
            self.mouse_timer = self.special_attack_cooldown
        if self.mouse_timer < 0 and self.dupa:
            self.game.particle_manager.add_particle(AttackReady(self.player.hitbox.topleft, self.player))
            self.dupa = False

    def input(self):
        self.update_special_timer()
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # INITIALISE SPECIAL ATTACK TIMER
                self.init_timer = True
            if event.type == pygame.MOUSEBUTTONUP and not self.special_attack and self.mouse_timer < 0:  # if enough time is waited, initialise special attack
                for par in self.game.particle_manager.particles:
                    if isinstance(par, AttackReady):
                        par.alive = False
                self.init_timer = False
                self.special_attack = True
                self.mouse_timer = self.special_attack_cooldown
                self.dupa = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and not self.normal_attack and self.wait(
                    self.normal_attack_timer, 250) and not self.special_attack:
                self.normal_attack_timer = pygame.time.get_ticks()
                self.normal_attack = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.init_timer = False

    def special_attack_update(self):
        if not self.special_attack:
            return
        if self.index == 0:
            self.attacks = [0, 150, 150, 300, 75]
        if self.wait(self.timer, self.attacks[self.index]):
            self.timer = pygame.time.get_ticks()
            self.game.particle_manager.add_particle(Slash(self.player, self))
            self.index += 1
        if self.index == 5:
            self.special_attack = False
            self.index = 0

    def normal_attack_update(self):
        if self.normal_attack:
            self.game.particle_manager.add_particle(Slash(self.player, self))
            self.normal_attack = False

    def update(self):
        super().update()
        if self.player:
            self.input()
            self.update_special_timer()
            self.special_attack_update()
            self.normal_attack_update()
        self.detect_collision()
