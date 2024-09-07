import pygame

from .weapon import Weapon
from data.src.entities.player.attack import Attack
from data.src.vfx.attack_ready import AttackReady
from data.src.entities.player.slash import Slash
from data.src.vfx.ground_ripple import GroundRipple
from pygame.math import Vector2
import random


class HammerSlash:
    def __init__(self, entity):
        self.entity = entity
        self.game = entity.game
        self.animation_frame = 0
        self.images = []
        self.image = None
        self.load_images()
        self.rect = self.image.get_rect()
        self.alive = True
        self.direction = self.entity.animation.animation_direction
        self.attack_rect = None
        self.hit = []
        self.size = (self.image.get_width(), self.image.get_height())

    def load_images(self):
        path = 'data/assets/vfx/slash'
        for i in range(5):
            image = pygame.image.load(f'{path}/slash{i}.png')
            self.images.append(image)
        self.image = self.images[int(self.animation_frame)]

    def update_animation_frame(self):
        self.image = self.images[int(self.animation_frame)]
        self.animation_frame += self.game.time.dtf() * 25
        if self.animation_frame >= 4:
            self.alive = False

    def update(self, dt):
        if self.direction == 'left':
            self.attack_rect = pygame.Rect(self.entity.hitbox.topright[0] - self.image.get_width(),
                                           self.entity.hitbox.topright[1],
                                           120, self.image.get_height() - 20)
        else:
            self.attack_rect = pygame.Rect(self.entity.hitbox.topright[0], self.entity.hitbox.topright[1],
                                           120, self.image.get_height() - 20)
        self.entity.animation.animation_direction = self.direction
        self.update_animation_frame()
        if self.player:
            for e in self.game.enemy_manager.enemies:
                if self.attack_rect.colliderect(e.hitbox):
                    if e not in self.hit:
                        self.add_effect(e.hitbox.center)
                        e.hurt = True
                        e.hurt_timer = pygame.time.get_ticks()
                        if self.direction == 'right':
                            e.position[0] += 25
                            self.entity.position[0] += 25
                        else:
                            e.position[0] -= 25
                            self.entity.position[0] -= 25
                        e.hp -= 5
                    self.hit.append(e)
        else:
            if self.attack_rect.colliderect(self.game.player.hitbox):
                if self.game.player not in self.hit and self.game.player.targetable:
                    self.add_effect(self.game.player.hitbox.center)
                self.hit.append(self.game.player)

    def draw(self, surface):
        # if self.direction == 'left':
        #     self.rect.topleft = (self.entity.rect.topleft[0] - 104, self.entity.rect.topleft[1] - 14)
        # else:
        #     self.rect.topleft = (self.entity.rect.topleft[0], self.entity.rect.topleft[1] - 14)
        # size = (self.size[0] * self.game.camera.zoom, self.size[1] * self.game.camera.zoom)
        # self.image = pygame.transform.scale(self.image, size)
        # if self.alive:
        #     if self.direction == 'left':
        #         self.game.display.screen.blit(pygame.transform.flip(self.image, 1, 0),
        #                                       self.game.camera.blit_position(self))
        #     else:
        #         self.game.display.screen.blit(self.image, self.game.camera.blit_position(self))
        pygame.draw.rect(self.game.display.screen, (244, 123, 32), self.attack_rect, 1)


class Jump:
    def __init__(self, entity):
        self.entity = entity
        self.duration = 100
        self.jump = False
        self.maximum_height = 100
        self.top = False
        self.direction = 1
        self.attack = False

    def slow_time(self):
        if not self.top and self.entity.height == 0:  # initial
            self.entity.game.time.slow_down.init_slow_down(500, 2)
        if self.entity.height + 25 >= self.maximum_height:
            self.entity.game.time.slow_down.init_slow_down(500, 0.1)
        if self.top and self.entity.height <= 50:
            self.entity.game.time.slow_down.init_slow_down(300, 0.25)
        if self.entity.height <= 0 and self.top:
            self.entity.game.time.slow_down.init_slow_down(1000, 0.25)

    def update(self):
        dt = self.entity.game.time.dtf()
        self.slow_time()
        x, y = 0, 0
        if self.entity.height >= self.maximum_height:  # check if player reached maximum jump height
            self.top = True
        if not self.top:
            y -= dt * self.entity.speed * self.entity.speed_multiplier
            x += dt * self.entity.speed * self.entity.speed_multiplier * self.direction
            self.entity.height += dt * self.entity.speed * self.entity.speed_multiplier
        else:
            y += dt * self.entity.speed * self.entity.speed_multiplier
            x += dt * self.entity.speed * self.entity.speed_multiplier * self.direction
            self.entity.height -= dt * self.entity.speed * self.entity.speed_multiplier
            if self.entity.height <= 0:
                # self.player.game.particle_manager.add_particle(Slash(self.player, self.player.game))
                self.entity.height = 0
                self.jump = False
                self.top = False
                a = GroundRipple(self.entity.game, (self.entity.hitbox.midbottom[0], self.entity.hitbox.midbottom[1]))
                self.entity.game.particle_manager.add_particle(a)
                self.entity.game.display.timer = pygame.time.get_ticks()
        self.entity.set_velocity(Vector2(x, y))


class Hammer(Weapon):
    name = 'hammer'
    size = (64, 128)

    def __init__(self, game, position, player=None):
        self.path = f'{self.base_path}{self.name}'
        super().__init__(game, self.name, position, player)
        self.damage = 25
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
        self.jump = Jump(self.entity)

    def interact(self):
        self.interaction = False
        self.show_name.reset_line_length()
        self.entity = self.game.player
        self.game.object_manager.remove_item(self)
        self.entity.items.items['weapon']['item'] = self

    def update_special_timer(self):
        if self.init_timer:
            self.mouse_timer -= self.game.time.dtf()
        else:
            self.mouse_timer = self.special_attack_cooldown
        if self.mouse_timer < 0 and self.dupa:
            self.game.particle_manager.add_particle(AttackReady(self.entity.hitbox.topleft, self.entity))
            self.dupa = False

    def input(self):
        self.update_special_timer()
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # INITIALISE SPECIAL ATTACK TIMER
                self.init_timer = True
            if event.type == pygame.MOUSEBUTTONUP and not self.special_attack and self.mouse_timer < 0:  # if enough time is waited, initialise special attack
                for par in self.game.particle_manager.particles:  # delete attack ready particle
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
        # Player jumps and attack with heavy blow, dealing AOE damage to enemies
        self.jump.jump = True
        self.jump.direction = -1 if self.entity.animation.animation_direction == 'left' else 1
        self.game.particle_manager.add_particle(
            GroundRipple(self.game, (self.entity.hitbox.midbottom[0], self.entity.hitbox.midbottom[1])))
        self.special_attack = False
        self.game.display.timer = pygame.time.get_ticks()

    def normal_attack_update(self):
        if self.normal_attack:
            self.game.particle_manager.add_particle(Slash(self.entity, self))
            self.normal_attack = False

    def update(self):
        super().update()
        if self.jump.jump:
            self.jump.update()
        # if self.entity.jump.jump: Fajnie wygląda, zachować
        #     self.weapon_swing.swing()
        if self.entity:
            self.input()
            self.update_special_timer()
            self.special_attack_update()
            self.normal_attack_update()
        self.detect_collision()

    def draw(self, surface, position=None):
        # If player is jumping

        #pygame.draw.rect(surface, (255, 255, 255), self.rect, 5)
        if self.jump.jump:
            if self.entity.animation.animation_direction == 'right':
                self.weapon_swing.swing_side = -1
            else:
                self.weapon_swing.swing_side = 1
            surface.blit(self.image, self.rect)
            #pygame.draw.rect(surface, (255, 255, 255), self.rect, 5)
            self.weapon_swing.rotate_180()
        else:
            self.weapon_swing.reset()
            if position:
                surface.blit(self.image, position)
                self.draw_outline(surface)
            if self.interaction and not self.entity:
                self.show_name.draw(surface, self.rect)
