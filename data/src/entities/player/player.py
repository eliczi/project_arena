import pygame
from data.src.entities.entity import Character
from pygame.math import Vector2
import math
from .roll import Roll
from data.src.objects.weapons.gold_dagger import GoldDagger
from data.src.objects.bullet import Bullet
from .items import Items
from .attributes import Attributes
from data.src.entities.player.slash import Slash
from data.src.vfx.ground_ripple import GroundRipple


class Jump:
    def __init__(self, player):
        self.player = player
        self.duration = 100
        self.jump = False
        self.maximum_height = 100
        self.top = False
        self.direction = 1

    def update(self, dt):
        x, y = 0, 0
        if self.player.height >= self.maximum_height:  # check if player reached maximum jump height
            self.top = True
        if not self.top:
            y -= dt * self.player.speed * self.player.speed_multiplier
            x += dt * self.player.speed * self.player.speed_multiplier * self.direction
            self.player.height += dt * self.player.speed * self.player.speed_multiplier
        else:
            y += dt * self.player.speed * self.player.speed_multiplier
            x += dt * self.player.speed * self.player.speed_multiplier * self.direction
            self.player.height -= dt * self.player.speed * self.player.speed_multiplier
            if self.player.height <= 0:
                # self.player.game.particle_manager.add_particle(Slash(self.player, self.player.game))
                self.jump = False
                self.top = False
                a = GroundRipple(self.player.game, (self.player.hitbox.midbottom[0], self.player.hitbox.midbottom[1]))
                self.player.game.particle_manager.add_particle(a)
                #self.player.game.time.slow_down.init_slow_down(500, 0.25)
        self.player.set_velocity(Vector2(x, y))


class Player(Character):
    name = 'red_beard'
    speed = 250
    path = f'data/assets/characters/players/{name}/'
    priority = 100

    def __init__(self, game):
        Character.__init__(self, game)
        self.rect = self.image.get_rect(center=(800, 768 / 2))
        self.update_hitbox()
        self.time = 0
        self.velocity = Vector2(0, 0)
        self.position = [self.rect.topleft[0], self.rect.topleft[1]]
        self.roll = Roll(game, self)
        self.weapon = None
        self.bul = 0
        self.bullets = []
        self.can_attack = True
        self.items = Items(game)
        self.player = True
        self.attributes = Attributes(game, self)
        self.jump = Jump(self)
        self.game.particle_manager.add_particle(self.shadow)

    def wait(self, time, amount):
        if pygame.time.get_ticks() - time > amount / self.game.time.game_speed:
            time = pygame.time.get_ticks()
            return True

    def wall_collision(self):
        test_rect = self.hitbox.move(*self.velocity)
        collide_points = (test_rect.midbottom, test_rect.bottomleft, test_rect.bottomright)
        for wall in self.game.map.wall_list:
            if any(wall.hitbox.collidepoint(point) for point in collide_points):
                self.velocity = [0, 0]
                self.roll.roll = False
                self.can_move = True

    def move_player(self):
        x, y = 0, 0
        pressed = pygame.key.get_pressed()
        dt = self.game.time.dtf()
        if pressed[pygame.K_w]:
            y -= dt * self.speed * self.speed_multiplier
        if pressed[pygame.K_s]:
            y += dt * self.speed * self.speed_multiplier
        if pressed[pygame.K_a]:
            x -= dt * self.speed * self.speed_multiplier
            self.anim_direction = 'left'
        if pressed[pygame.K_d]:
            x += dt * self.speed * self.speed_multiplier
            self.anim_direction = 'right'
        if pressed[pygame.K_i] and self.items.can_draw():
            self.items.draw_items = not self.items.draw_items
        if pressed[pygame.K_e]:
            self.game.object_manager.interaction = True
            self.game.npc_manager.interaction = True
        else:
            self.game.object_manager.interaction = False
            self.game.npc_manager.interaction = False
        if all((x, y)):
            x = x * math.sqrt(2) / 2
            y = y * math.sqrt(2) / 2
        self.set_velocity(Vector2(x, y))

    def input(self):
        # player movement
        if self.can_move:
            self.move_player()
        # rolling
        self.roll.input()

    def player_position_to_mouse(self):
        pos = pygame.mouse.get_pos()
        if self.hitbox.center[0] - pos[0] <= 0:
            self.animation.animation_direction = 'right'
            self.direction = 'right'
        else:
            self.direction = 'left'
            self.animation.animation_direction = 'left'

    def update(self):
        if self.jump.jump:
            self.jump.update(self.game.time.dtf())
        else:
            self.player_position_to_mouse()
            self.input()
            self.roll.rolling()
            self.wall_collision()
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.animation.update()
        self.rect.update(self.position[0], self.position[1], 64, 64)
        self.hitbox.midbottom = self.rect.midbottom
        self.items.update()

    def draw(self, surface):
        if self.game.camera.zoom != 1:
            self.resize()
        if self.bullets:
            surface.blit(self.image, self.game.camera.center_blit(self, self.bullets[0]))
        else:
            surface.blit(self.image, self.game.camera.blit_position(self))
        self.items.draw(surface)
        self.attributes.draw()
        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)
        # pygame.draw.rect(surface, (255, 255, 255), self.hitbox, 1)
