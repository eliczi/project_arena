import pygame
import random
from data.src.vfx.line import Line
from data.src.vfx.polygon import Polygon
from data.src.vfx.smoke import Smoke


class Slash:
    def __init__(self, entity, attack):
        self.entity = entity
        self.player = True if entity.player == True else False
        self.attack = attack
        self.game = entity.game
        self.animation_frame = 0
        self.images = []
        self.image = None
        self.load_images()
        self.rect = self.image.get_rect()
        self.alive = True
        self.direction = self.entity.animation.animation_direction
        if self.player:
            self.direct()
        self.attack_rect = None
        if self.direction == 'left':
            self.attack_rect = pygame.Rect(self.entity.hitbox.topright[0] - self.image.get_width(),
                                           self.entity.hitbox.topright[1],
                                           120, self.image.get_height() - 20)

        else:
            self.attack_rect = pygame.Rect(self.entity.hitbox.topright[0], self.entity.hitbox.topright[1],
                                           120, self.image.get_height() - 20)
        self.sound = pygame.mixer.Sound('data/assets/sound.mp3')
        self.hit = []
        self.shake = False
        self.size = (self.image.get_width(), self.image.get_height())

    def direct(self):
        pos = pygame.mouse.get_pos()
        if self.entity.hitbox.center[0] - pos[0] <= 0:
            self.direction = 'right'
            self.entity.direction = 'right'
        else:
            self.direction = 'left'
            self.entity.anim_direction = 'left'

    def load_images(self):
        path = 'data/assets/vfx/slash'
        for i in range(5):
            image = pygame.image.load(f'{path}/slash{i}.png')
            self.images.append(image)
        self.flip_images()
        self.image = self.images[int(self.animation_frame)]

    def flip_images(self):
        if random.randint(1, 2) == 1:
            self.images = [pygame.transform.flip(img, 0, 1) for img in self.images]

    def add_effect(self, pos):
        self.game.particle_manager.add_particle(Line(self.game, pos))
        for _ in range(20):
            self.game.particle_manager.add_particle(Polygon(self.game, pos))

    def update_animation_frame(self):
        self.image = self.images[int(self.animation_frame)]
        self.animation_frame += self.game.time.dtf() * 25
        if self.animation_frame >= 4:
            self.alive = False

    def move_player(self):
        if self.direction == 'right':
            self.entity.position[0] += self.game.time.dtf() * 2000
        else:
            self.entity.position[0] -= self.game.time.dtf() * 2000

    def move_entity(self, e):
        if self.direction == 'right':
            e.position[0] += self.game.time.dtf() * 2000
        else:
            e.position[0] -= self.game.time.dtf() * 2000

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
        if self.direction == 'left':
            self.rect.topleft = (self.entity.rect.topleft[0] - 104, self.entity.rect.topleft[1] - 14)
        else:
            self.rect.topleft = (self.entity.rect.topleft[0], self.entity.rect.topleft[1] - 14)
        size = (self.size[0] * self.game.camera.zoom, self.size[1] * self.game.camera.zoom)
        self.image = pygame.transform.scale(self.image, size)
        if self.alive:
            if self.direction == 'left':
                self.game.display.screen.blit(pygame.transform.flip(self.image, 1, 0),
                                              self.game.camera.blit_position(self))
            else:
                self.game.display.screen.blit(self.image, self.game.camera.blit_position(self))
        #pygame.draw.rect(self.game.display.screen, (244, 123, 32), self.attack_rect, 1)
