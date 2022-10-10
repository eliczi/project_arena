import pygame
from ..object import Object
from pygame.math import Vector2
import math

class WeaponSwing:
    left_swing = 10
    right_swing = -190

    def __init__(self, weapon):
        self.weapon = weapon
        self.angle = 0
        self.offset = Vector2(0, -50)
        self.offset_rotated = Vector2(0, -25)
        self.counter = 0
        self.swing_side = 1

    def reset(self):
        self.counter = 0

    def rotate(self, weapon=None):
        mx, my = pygame.mouse.get_pos()
        dx = mx - self.weapon.player.hitbox.centerx  # - 64
        dy = my - self.weapon.player.hitbox.centery  # - 32
        if self.swing_side == 1:
            self.angle = (180 / math.pi) * math.atan2(-self.swing_side * dy, dx) + self.left_swing
        else:
            self.angle = (180 / math.pi) * math.atan2(self.swing_side * dy, dx) + self.right_swing

        position = self.weapon.player.hitbox.center
        if weapon:
            self.weapon.image = pygame.transform.rotozoom(self.weapon.image, self.angle, 1)
        else:
            self.weapon.image = pygame.transform.rotozoom(self.weapon.original_image, self.angle, 1)

        offset_rotated = self.offset.rotate(-self.angle)
        self.weapon.rect = self.weapon.image.get_rect(center=position + offset_rotated)
        #self.weapon.hitbox = pygame.mask.from_surface(self.weapon.image)
        self.offset_rotated = Vector2(0, -35).rotate(-self.angle)

    def swing(self):
        self.angle += 20 * self.swing_side
        position = self.weapon.player.hitbox.center
        self.weapon.image = pygame.transform.rotozoom(self.weapon.original_image, self.angle, 1)
        offset_rotated = self.offset.rotate(-self.angle)
        self.weapon.rect = self.weapon.image.get_rect(center=position + offset_rotated)
        #self.rect_mask = get_mask_rect(self.image, *self.rect.topleft)
        self.weapon.hitbox = pygame.mask.from_surface(self.weapon.image)
        self.counter += 1


class Weapon(Object):
    base_path = 'data/assets/objects/weapon/'
    damage = 0
    normal_attack_cooldown = 0
    special_attack_cooldown = 0
    type = 'weapon'
    special_attack = ""

    def __init__(self, game, name, position, player=None):
        super().__init__(game, name, position, player)
        self.mouse_timer = self.special_attack_cooldown
        self.init_timer = False
        self.special_attack = False
        self.normal_attack = False
        self.weapon_swing = WeaponSwing(self)

    def player_update(self):
        self.interaction = False
        if self.weapon_swing.counter == 10:
            self.original_image = pygame.transform.flip(self.original_image, 1, 0)
            self.player.attacking = False
            self.weapon_swing.counter = 0
        else:
            self.weapon_swing.rotate()

    def update(self):
        super().update()


    def attack(self):
        pass
