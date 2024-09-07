import pygame
import random
import math
from ..setup import get_mask_rect
from data.src.utils.utils import perfect_outline

font = pygame.font.SysFont('Bitty', 30)


class ShowName:
    # TODO drawing animation dependent on player position
    def __init__(self, object):
        self.object = object
        self.line_length = 0
        self.time = 0
        # Format weapon display name
        self.text = self.object.name.replace("_", " ").title()
        self.text_length = len(self.text)
        self.text_position = None
        self.counter = 0

    @staticmethod
    def time_passed(time, amount):
        """Wait 'amount' amount of time"""
        if pygame.time.get_ticks() - time > amount:
            return True

    def draw(self, surface, rect):
        self.draw_text_line(surface, rect)
        self.draw_text(surface)

    def draw_text(self, surface):
        font = 'data/assets/Minecraft.ttf'
        text_surface = pygame.font.Font(font, 15).render(self.text[:self.counter], True, (255, 255, 255))
        surface.blit(text_surface, self.text_position)

    def draw_text_line(self, surface, rect):
        starting_position = [rect.topleft[0], rect.topleft[1]]  # starting position of diagonal line
        for _ in range(5):  # we draw rectangles in diagonal line, so the line looks pixelated
            starting_position[0] -= 5
            starting_position[1] -= 5
            pygame.draw.rect(surface, (255, 255, 255), (starting_position[0], starting_position[1], 5, 5))

        starting_position[1] += 2  # adjustment of vertical position
        end_position = [starting_position[0] - self.line_length, starting_position[1]]
        pygame.draw.line(surface, (255, 255, 255), starting_position, end_position, 5)
        if self.line_length <= self.text_length * 8 and self.time_passed(self.time, 15):
            self.time = pygame.time.get_ticks()
            self.line_length += 8
            self.counter += 1
        self.text_position = (end_position[0], end_position[1] - 20)

    def reset_line_length(self):
        self.line_length = 0
        self.counter = 0


class Hovering:
    def __init__(self, game, obj):
        self.game = game
        self.object = obj
        self.hover_value = 0
        self.position = 1

    def set_hover_value(self):
        num = self.game.object_manager.up // 2
        if num % 2 == 0:
            self.hover_value = -5
        elif num % 2 == 1:
            self.hover_value = 5

    def hovering(self):
        if self.object.player is not None:
            return
        if self.object.game.object_manager.hover:
            self.object.rect.y += self.hover_value
            if self.hover_value > 0:
                self.object.shadow.position += 1
            else:
                self.object.shadow.position -= 1
        self.set_hover_value()


class Object:
    size = (64, 64)
    type = None

    def __init__(self, game, name, position, entity=None):
        self.game = game
        self.name = name
        self.position = position
        self.entity = entity
        self.original_image = None
        self.image = None
        self.load_image()
        self.rect = self.image.get_rect(topleft=self.position)
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.show_name = ShowName(self)
        self.bounce = None
        self.interaction = False
        self.update_hitbox()
        self.draw_merchant = False
        self.price = 15
        self.animation_frame = 0
        self.images = []
        self.load_images()

    def wait(self, time, amount):
        if pygame.time.get_ticks() - time > amount / self.game.time.game_speed:
            time = pygame.time.get_ticks()
            return True

    def load_image(self):
        self.original_image = pygame.transform.scale(pygame.image.load(
            f'{self.path}/{self.name}.png').convert_alpha(), self.size)
        self.image = self.original_image

    def detect_collision(self):
        if self.game.player.hitbox.colliderect(self.hitbox):
            self.interaction = True
        else:
            self.interaction = False
            self.show_name.reset_line_length()

    def update_hitbox(self):
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def update(self):
        self.update_hitbox()
        self.detect_collision()
        self.update_animation_frame()

    def draw_outline(self, surface):
        if self.interaction:
            perfect_outline(self.image, self.rect, surface)

    def draw(self, surface, position=None):
        if position:
            surface.blit(self.image, position)
            self.draw_outline(surface)
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
            self.draw_outline(surface)
        if self.interaction:
            self.show_name.draw(surface, self.rect)
        # self.draw_merchant_information(surface)
        #pygame.draw.rect(surface, (255, 120, 250), self.rect, 5)

    def load_images(self):
        for i in range(4):
            image = pygame.image.load(f'data/assets/coin/coin/coin{i}.png').convert_alpha()
            image = pygame.transform.scale(image, (16,16))
            self.images.append(image)

    def update_animation_frame(self):
        self.animation_frame += ((1.5 + (random.randint(1, 5) / 10)) / 15)  * self.game.time.game_speed
        if self.animation_frame > 3:
            self.animation_frame = 0

    def draw_merchant_information(self, surface):
        positions = {'coin_position': (10, 10),
                     'attack_position': (10, 26)}
        if self.draw_merchant:
            self.update_animation_frame()
            pos = pygame.mouse.get_pos()
            attack = pygame.transform.scale(
                surface=pygame.image.load(f'data/assets/attack.png').convert_alpha(),
                size=(16, 16)
            )

            pygame.draw.rect(surface, (143, 86, 59), rect=(pos[0], pos[1], 128, 64))
            pygame.draw.rect(surface, (102, 57, 49), rect=(pos[0], pos[1], 128, 64), width=5)
            surface.blit(self.images[int(self.animation_frame)], (pos[0] + 10, pos[1] + 10))
            surface.blit(attack, (pos[0] + 10, pos[1] + 36))
        # text_surface = font.render(f'{self.price}', False, (255, 255, 255))
        # self.game.display.screen.blit(text_surface, (pos[0], pos[1]))
        # surface.blit(self.image, (self.rect.x, self.rect.y))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Bounce:
    def __init__(self, x, y, limit, size):
        self.speed = random.uniform(0.5, 0.6)  # 0.5
        self.angle = random.randint(-10, 10) / 10  # random.choice([10, -10])
        self.drag = 0.999
        self.elasticity = random.uniform(0.75, 0.9)  # 0.75
        self.gravity = (math.pi, 0.002)
        self.limit = limit
        self.limits = [limit, 654]
        self.x, self.y = x, y
        self.size = size

    @staticmethod
    def add_vectors(angle1, length1, angle2, length2):
        x = math.sin(angle1) * length1 + math.sin(angle2) * length2
        y = math.cos(angle1) * length1 + math.cos(angle2) * length2
        angle = 0.5 * math.pi - math.atan2(y, x)
        length = math.hypot(x, y)
        return angle, length

    def move(self):
        self.angle, self.speed = self.add_vectors(self.angle, self.speed, *self.gravity)
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def bounce(self):
        # if self.y > any(self.limits):
        if self.y > self.limit:
            self.y = 2 * self.limit - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

        elif self.y > 654 - self.size[0]:
            self.y = 2 * (654 - self.size[0]) - self.y
            self.angle = math.pi - self.angle
            self.speed *= self.elasticity

        if self.x < 198 + 10:
            self.x = 2 * (198 + 10) - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

        elif self.x > 1136 - self.size[0]:
            self.x = 2 * (1136 - self.size[0]) - self.x
            self.angle = - self.angle
            self.speed *= self.elasticity

    def reset(self):
        self.speed = 0.5
        self.angle = random.choice([10, -10])
        self.drag = 0.999
        self.elasticity = 0.75
