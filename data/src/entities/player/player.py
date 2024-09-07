import pygame
from data.src.entities.entity import Character
from pygame.math import Vector2
import math
from .roll import Roll
from data.src.objects.weapons.gold_dagger import GoldDagger
from data.src.objects.weapons.hammer import Hammer
from data.src.objects.bullet import Bullet
from .items import Items
from .attributes import Attributes
from data.src.entities.player.slash import Slash
from data.src.vfx.ground_ripple import GroundRipple
#import sand class
from data.src.vfx.sand import Sand
from .player_info import Hud

class Player(Character):
    name = 'red_beard'
    speed = 250
    path = f'data/assets/characters/players/{name}/'
    priority = 100


    def __init__(self, game):
        Character.__init__(self, game)
        self.rect = self.image.get_rect(center=(800, 832 / 2))
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
        self.game.particle_manager.add_particle(self.shadow)
        self.items.assign_item(Hammer(game, (0, 0), self), self)
        self.hud = Hud(self, game)

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
        change_factor = self.game.time.dtf() * self.speed * self.speed_multiplier
        if pressed[pygame.K_w]:
            y -= change_factor
        if pressed[pygame.K_s]:
            y += change_factor
        if pressed[pygame.K_a]:
            x -= change_factor
            self.anim_direction = 'left'
        if pressed[pygame.K_d]:
            x += change_factor
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
        
        # if self.jump.jump:
        #     self.jump.update(self.game.time.dtf())
        if self.height == 0:
            self.player_position_to_mouse()
            self.input()
            self.roll.update()
            self.wall_collision()
        self.position = [x + self.velocity[i] for i, x in enumerate(self.position)]
        self.correct_position()
        self.animation.update()
        #print("position: ", self.position, "rect: ", self.hitbox)

        self.rect.move_ip(*self.velocity)
        self.hitbox.move_ip(*self.velocity)
        #self.rect.update(self.position[0], self.position[1], 64, 64)
        #self.hitbox.midbottom = self.rect.midbottom
        self.items.update()
        if pygame.time.get_ticks() - self.hurt_timer > 300 / self.game.time.game_speed:
            self.hurt = False
            self.hurt_timer = pygame.time.get_ticks()
            


    def draw(self, surface: pygame.Surface) -> None:
        self.hud.draw(surface)
        self.resize()
        if self.hurt:
            surface.blit(self.hurting(), self.get_blit_position())
        else:
            surface.blit(self.image, self.get_blit_position())
        self.items.draw(surface)
        #self.attributes.draw()

        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)
        # pygame.draw.rect(surface, (255, 255, 255), self.hitbox, 1)
