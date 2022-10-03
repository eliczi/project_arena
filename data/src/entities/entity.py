import pygame
from data.src.setup import get_mask_rect
from .animation import EntityAnimation


def draw_health_bar(surf, pos, size, border_c, back_c, health_c, progress):
    pygame.draw.rect(surf, back_c, (*pos, *size))
    pygame.draw.rect(surf, border_c, (*pos, *size), 1)
    inner_pos = (pos[0] + 1, pos[1] + 1)
    inner_size = ((size[0] - 2) * progress, size[1] - 2)
    rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    pygame.draw.rect(surf, health_c, rect)


class Shadow:

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.alive = True
        self.width = 10
        self.height = 3
        self.rect = pygame.Rect(player.hitbox.bottomleft[0] / 4, player.hitbox.bottomleft[1] / 4, self.width,
                                self.height)
        self.rect.midtop = (player.hitbox.midbottom[0] / 4, player.hitbox.midbottom[1] / 4)
        self.color = (0, 0, 0, 125)
        self.sizes = [[10, 4]]
        self.index = 0

    def update(self, dt):
        self.rect.midtop = (self.player.rect.midbottom[0] / 4, self.player.rect.midbottom[1] / 4)
        self.rect.size = self.sizes[int(self.index)]

    def draw(self, surface):
        pygame.draw.ellipse(self.game.display.particle_screen, self.color, self.rect)


class Entity:

    def __init__(self, game):
        self.game = game
        self.image = None
        self.load_image()
        self.rect = self.image.get_rect()
        self.hitbox = None
        self.update_hitbox()
        self.speed_multiplier = 2
        self.can_move = True
        self.position = []
        self.shadow = Shadow(game, self)
        #self.game.particle_manager.add_particle(self.shadow)

    def load_image(self):
        pass

    def update_hitbox(self):
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def resize(self):
        size = (self.size[0] * self.game.camera.zoom, self.size[1] * self.game.camera.zoom)
        self.image = pygame.transform.scale(self.image, size)


class Character(Entity):
    size = (64, 64)

    def __init__(self, game):
        super().__init__(game)
        self.velocity = [0, 0]
        self.anim_direction = 'right'
        self.animation = EntityAnimation(self, game)
        self.dead = False
        self.hurt = False
        self.facing_direction = 'right'

    def load_image(self):
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}/idle/idle0.png'),
                                            self.size).convert_alpha()

    def set_velocity(self, velocity):
        self.velocity = velocity

    def moving(self):
        if sum(self.velocity) != 0:
            return True

    def update(self):
        self.rect.move_ip(*self.velocity)
        self.hitbox.move_ip(*self.velocity)

    def zoom_in(self):
        if self.game.camera.zoom != 1:
            self.size = (size * self.game.camera.zoom for size in self.size)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def wall_collision(self):
        if self.hitbox.topright[0] + self.velocity[0] > 1600 or self.hitbox.x + self.velocity[0] < 0:
            self.velocity = [0, 0]
        else:
            self.position[0] += self.velocity[0]
        if self.hitbox.midbottom[1] + self.velocity[1] < 256 or self.hitbox.bottomleft[1] + self.velocity[1] > 768:
            self.velocity = [0, 0]
        else:
            self.position[1] += self.velocity[1]

    def draw_health(self, surf):
        health_rect = pygame.Rect(0, 0, 30, 8)
        health_rect.midbottom = self.rect.centerx, self.rect.top
        draw_health_bar(surf, health_rect.topleft, health_rect.size,
                        (1, 0, 0), (255, 0, 0), (0, 255, 0), self.hp / self.max_hp)
