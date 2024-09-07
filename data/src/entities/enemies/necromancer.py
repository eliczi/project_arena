import pygame
import random
from data.src.entities.entity import Character
from data.src.entities.player.attack import Attack
from data.src.entities.player.slash import Slash


class Necromancer(Character):
    name = 'necromancer'
    speed = 80
    path = f'data/assets/characters/{name}/'
    max_hp = 100
    hp = max_hp

    def __init__(self, game, position):
        Character.__init__(self, game)
        self.accumulated_vector = [0, 0]
        self.rect.topleft = position
        self.update_hitbox()
        self.roll = False
        self.position = [self.rect.topleft[0], self.rect.topleft[1]]
        self.hurt_timer = 0
        self.attack_timer = 0

    def move_towards_player(self, proximity=0):
        dt = self.game.time.dtf()
        x = -1 if int(self.game.player.position[0]) > int(self.position[0]) else 1
        dir_vector = pygame.math.Vector2(self.game.player.hitbox.midbottom[0] + 64 * x - self.hitbox.midbottom[0],
                                         self.game.player.hitbox.midbottom[1] + self.game.player.height - self.hitbox.midbottom[1])
        if dir_vector.length() > proximity:
            if dir_vector.length_squared() > 0:
                dir_vector.scale_to_length(self.speed * dt * self.speed_multiplier)
                self.set_velocity(dir_vector)
                self.set_direction()
                self.can_attack = False
        else:
            self.set_velocity([0, 0])
            self.can_attack = True

    def set_direction(self):
        if self.position[0] < self.game.player.position[0]:
            self.animation.animation_direction = 'right'
        else:
            self.animation.animation_direction = 'left'


    def detect_collision(self):
        if self.hitbox.colliderect(self.game.player.hitbox):
            pass

    def hurting(self):
        mask = pygame.mask.from_surface(self.image)
        mask_surf = mask.to_surface()
        mask_surf.set_colorkey((0, 0, 0))
        return mask_surf

    def attack(self):
        self.game.particle_manager.add_particle(Slash(self, self))

    def update(self):
        self.animation.update()
        if self.can_move:
            self.move_towards_player()
        self.wall_collision()
        self.rect.update(self.position[0], self.position[1], 64, 64)
        self.hitbox.midbottom = self.rect.midbottom
        if self.can_attack and pygame.time.get_ticks() - self.attack_timer > 500:
            self.attack_timer = pygame.time.get_ticks()
            self.attack()
        if self.hp <= 0:
            self.dead = True
        if pygame.time.get_ticks() - self.hurt_timer > 150 / self.game.time.game_speed:
            self.hurt = False
            self.hurt_timer = pygame.time.get_ticks()

    def draw(self, surface):
        self.resize()
        if self.hurt:
            surface.blit(self.hurting(), self.game.camera.blit_position(self))
        else:
            surface.blit(self.image, self.game.camera.blit_position(self))
        self.draw_health(surface)
        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)
        # pygame.draw.rect(surface, (255, 255, 255), self.hitbox, 1)
