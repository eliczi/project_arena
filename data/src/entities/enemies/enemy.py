import pygame
import random
from data.src.entities.entity import Character
from data.src.entities.player.attack import Attack


class Enemy(Character):
    name = 'orc_warrior'
    speed = 96
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

    def move_towards_player(self, proximity=64):
        dt = self.game.time.dtf()
        dir_vector = pygame.math.Vector2(self.game.player.hitbox.centerx - self.hitbox.centerx,
                                         self.game.player.hitbox.centery - self.hitbox.centery)
        if dir_vector.length() > proximity:
            if dir_vector.length_squared() > 0:
                dir_vector.scale_to_length(self.speed * dt * self.speed_multiplier)
                self.set_velocity(dir_vector)
        else:
            self.set_velocity([0, 0])

    def detect_collision(self):
        if self.hitbox.colliderect(self.game.player.hitbox):
            pass

    def hurting(self):
        mask = pygame.mask.from_surface(self.image)
        mask_surf = mask.to_surface()
        mask_surf.set_colorkey((0, 0, 0))
        return mask_surf

    def update(self):
        self.animation.update()
        self.can_move = False
        if self.can_move:
            self.move_towards_player()
        self.wall_collision()
        self.rect.update(self.position[0], self.position[1], 64, 64)
        self.hitbox.midbottom = self.rect.midbottom
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
