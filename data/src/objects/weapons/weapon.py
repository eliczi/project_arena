import pygame
from ..object import Object
from pygame.math import Vector2
import math
from data.src.vfx.dot import Dot

class WeaponSwing:
    left_swing = 10
    right_swing = 190

    def __init__(self, weapon):
        self.weapon = weapon
        self.offset = Vector2(0, -126)  # how much distant from entity
        self.counter = 0
        self.swing_side = -1
        self.angle = 90 * self.swing_side
        self.center = None

    def reset(self):
        self.counter = 0
        self.angle = 90

    def rotate_180(self):
        self.angle += 1.03 * self.swing_side * self.weapon.game.time.dtf() * 400
        self.weapon.image = pygame.transform.rotozoom(self.weapon.original_image, self.angle, 1)
        offset_rotated = self.offset.rotate(-self.angle)
        position = self.weapon.entity.hitbox.center
        self.weapon.rect = self.weapon.image.get_rect(center=position + offset_rotated)
        if self.weapon.entity:
            self.center = self.weapon.entity.hitbox.center
            offset_rotated = Vector2(0, -126).rotate(-self.angle)
            center = self.center + offset_rotated
            self.weapon.game.particle_manager.add_particle(Dot(center))


class Weapon(Object):
    base_path = 'data/assets/objects/weapon/'
    damage = 0
    normal_attack_cooldown = 0
    special_attack_cooldown = 0
    type = 'weapon'
    special_attack = ""

    def __init__(self, game, name, position, entity=None):
        super().__init__(game, name, position, entity)
        self.mouse_timer = self.special_attack_cooldown
        self.init_timer = False
        self.special_attack = False
        self.normal_attack = False
        self.weapon_swing = WeaponSwing(self)

    def player_update(self):
        self.interaction = False
        if self.weapon_swing.counter == 10:
            self.original_image = pygame.transform.flip(self.original_image, 1, 0)
            self.entity.attacking = False
            self.weapon_swing.counter = 0
        else:
            self.weapon_swing.rotate()

    def update(self):
        super().update()

    def attack(self):
        pass
