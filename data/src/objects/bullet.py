import pygame
from .object import Object
from pygame.math import Vector2


class Bullet:
    name = 'bullet'
    color = (242, 123, 54)

    def __init__(self, game, position, player, mouse):
        # super().__init__(game, 'bullet', position=position, player=player)
        self.game = game
        self.position = position
        self.player = player
        self.rect = pygame.Rect(*position, 5, 5)
        self.dir = Vector2(mouse) - Vector2(position)
        self.dir.normalize_ip()
        self.position = Vector2(self.position)

    def update(self):
        dir = pygame.mouse.get_pos()
        dir = Vector2(dir) - Vector2(self.position)
        dir.normalize_ip()
        self.position += self.dir * 3
        self.rect.update(self.position[0], self.position[1], 25, 25)

    def draw(self, surface):
        #position = self.game.camera.player_blit()
        pygame.draw.circle(surface, self.color, self.game.camera.player_blit(self), 15 * self.game.camera.zoom_factor)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)
