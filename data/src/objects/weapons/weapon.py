import pygame
from ..object import Object


class Weapon(Object):
    base_path = 'data/assets/objects/weapon/'
    damage = 0
    normal_attack_cooldown = 0
    special_attack_cooldown = 0

    def __init__(self, game, name, position, player=None):
        super().__init__(game, name, position, player)
        self.mouse_timer = self.special_attack_cooldown
        self.init_timer = False
        self.special_attack = False
        self.normal_attack = False

    def update(self):
        super().update()

    def attack(self):
        pass
