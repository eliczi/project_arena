import pygame
import random
from data.src.vfx.line import Line
from data.src.vfx.polygon import Polygon
from data.src.vfx.smoke import Smoke


class Slash:
    def __init__(self, player, attack):
        self.player = player
        self.attack = attack
        self.game = player.game
        self.animation_frame = 0
        self.images = []
        self.image = None
        self.load_images()
        self.rect = self.image.get_rect()
        self.alive = True
        self.direction = self.player.anim_direction
        self.direct()
        self.attack_rect = None
        if self.direction == 'left':
            self.attack_rect = pygame.Rect(self.player.hitbox.topright[0] - self.image.get_width(),
                                           self.player.hitbox.topright[1],
                                           120, self.image.get_height() - 20)

        else:
            self.attack_rect = pygame.Rect(self.player.hitbox.topright[0], self.player.hitbox.topright[1],
                                           120, self.image.get_height() - 20)
        self.sound = pygame.mixer.Sound('data/assets/sound.mp3')
        self.hit = []
        self.shake = False
        self.size = (self.image.get_width(), self.image.get_height())

    def direct(self):
        pos = pygame.mouse.get_pos()
        if self.player.hitbox.center[0] - pos[0] <= 0:
            self.direction = 'right'
            self.player.direction = 'right'
        else:
            self.direction = 'left'
            self.player.anim_direction = 'left'

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
            self.player.position[0] += self.game.time.dtf() * 2000
        else:
            self.player.position[0] -= self.game.time.dtf() * 2000

    def move_entity(self, e):
        if self.direction == 'right':
            e.position[0] += self.game.time.dtf() * 2000
        else:
            e.position[0] -= self.game.time.dtf() * 2000

    def update(self, dt):
        if self.direction == 'left':
            self.attack_rect = pygame.Rect(self.player.hitbox.topright[0] - self.image.get_width(),
                                           self.player.hitbox.topright[1],
                                           120, self.image.get_height() - 20)
        else:
            self.attack_rect = pygame.Rect(self.player.hitbox.topright[0], self.player.hitbox.topright[1],
                                           120, self.image.get_height() - 20)
        self.player.animation.animation_direction = self.direction
        self.update_animation_frame()
        for e in self.game.enemy_manager.enemies:
            if self.attack_rect.colliderect(e.hitbox):
                if e not in self.hit:
                    self.add_effect(e.hitbox.center)
                    e.hurt = True
                    e.hurt_timer = pygame.time.get_ticks()
                    self.game.time.slow_down.init_slow_down(3000, 0.1)

                    e.hp -= 5
                    # pygame.mixer.Sound.play(self.sound)
                self.hit.append(e)

    def draw(self, surface):
        if self.direction == 'left':
            self.rect.topleft = (self.player.rect.topleft[0] - 104, self.player.rect.topleft[1] - 14)
        else:
            self.rect.topleft = (self.player.rect.topleft[0], self.player.rect.topleft[1] - 14)
        size = (self.size[0] * self.game.camera.zoom, self.size[1] * self.game.camera.zoom)
        self.image = pygame.transform.scale(self.image, size)
        if self.alive:
            if self.direction == 'left':
                self.game.display.screen.blit(pygame.transform.flip(self.image, 1, 0),
                                              self.game.camera.blit_position(self))
            else:
                self.game.display.screen.blit(self.image, self.game.camera.blit_position(self))
        # pygame.draw.rect(self.game.display.screen, (244, 123, 32), self.attack_rect, 1)
