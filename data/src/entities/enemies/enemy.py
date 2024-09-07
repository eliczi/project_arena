import pygame
import random
from data.src.entities.entity import Character
from data.src.entities.player.attack import Attack
from data.src.entities.player.slash import Slash
from data.src.utils.utils import wait

class Enemy(Character):
    name = 'orc_warrior'
    speed = 160
    path = f'data/assets/characters/{name}/'
    max_hp = 100
    hp = max_hp

    def __init__(self, game, position):
        Character.__init__(self, game)
        self.rect.topleft = position
        self.update_hitbox()
        self.position = [self.rect.topleft[0], self.rect.topleft[1]]
        self.attack_timer = 0

    def move_towards_target(self, proximity=5, target=None):
        if target is None:
            target = self.game.player

        x = -1 if int(target.position[0]) > int(self.position[0]) else 1
        dir_vector = pygame.math.Vector2(target.hitbox.midbottom[0] + 64 * x - self.hitbox.midbottom[0],
                                         target.hitbox.midbottom[1] + target.height - self.hitbox.midbottom[1])
        
        # Check if the distance between the enemy and the target is greater than the proximity threshold
        # and if the direction vector is non-zero
        if dir_vector.length() > proximity and dir_vector.length_squared() > 0:
            dir_vector.scale_to_length(self.speed * self.game.time.dtf() * self.speed_multiplier)
            self.set_velocity(dir_vector)
            self.set_direction()
            self.can_attack = False
        else:
            self.set_velocity([0, 0])
            self.can_attack = True

    def set_direction(self, target=None):
        if target is None:
            target = self.game.player
        if self.position[0] < target.position[0]:
            self.animation.animation_direction = 'right'
        else:
            self.animation.animation_direction = 'left'

    def attack(self):
        if self.can_attack and wait(self.game,  self.attack_timer,500):
            self.attack_timer = pygame.time.get_ticks()
            self.game.particle_manager.add_particle(Slash(self, self))


    def update(self):
        self.animation.update()
        if self.can_move:
            self.move_towards_target()
        self.wall_collision() #if wall collistion, velocity = [0,0]
        self.rect.move_ip(*self.velocity)
        self.hitbox.move_ip(*self.velocity)
        self.position = [x + self.velocity[i] for i, x in enumerate(self.position)]
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
