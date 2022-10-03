import pygame


class Camera:

    def __init__(self, game):
        self.game = game
        self.zoom = 1.0
        self.zoom_target_x = 800
        self.zoom_target_y = 768 / 2
        self.last_position = [0, 0]
        self.first = True
        self.zoom_change = False
        self.set = False
        self.adjust = False

    def set_difference(self):
        if self.zoom_target_x - self.last_position[0] > 10:
            self.zoom_target_x = self.last_position[0] + abs(self.zoom_target_x - self.last_position[0]) / 10
        elif self.zoom_target_x - self.last_position[0] <= 0:
            self.zoom_target_x = self.last_position[0] - abs(self.zoom_target_x - self.last_position[0]) / 10

        if self.zoom_target_y - self.last_position[1] > 10:
            self.zoom_target_y = self.last_position[1] + abs(self.zoom_target_x - self.last_position[1]) / 10
        elif self.zoom_target_y - self.last_position[1] < 0:
            self.zoom_target_y = self.last_position[1] - abs(self.zoom_target_x - self.last_position[1]) / 10

    def update_last_position(self):
        self.last_position = [self.zoom_target_x, self.zoom_target_y]

    def update_zoom_target(self, target=None):
        if target:
            self.zoom_target_x = target.rect.center[0]
            self.zoom_target_y = target.rect.center[1]
        if self.first:
            self.last_position = [self.zoom_target_x, self.zoom_target_y]
            self.first = False

    def zoom_in(self, target=None, zoom_factor=0.01):
        self.zoom = self.zoom * 1.05
        self.update_zoom_target(target)
        self.set_difference()
        self.update_last_position()
        self.zoom_change = True

    def zoom_out(self, target=None):
        if self.zoom > 0 + 0.01:
            self.zoom /= 1.05
        self.update_zoom_target(target)
        # self.set_difference2()
        self.update_last_position()
        self.zoom_change = True

    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_z]:
            self.zoom_in(self.game.player)
            self.game.map.resize()
        if pressed[pygame.K_x]:
            self.zoom_out(self.game.player)
            self.game.map.resize()
        if pressed[pygame.K_r]:
            self.reset()
            self.game.map.resize()
        if pressed[pygame.K_UP]:
            self.zoom_target_y -= 10
            self.update_last_position()
        if pressed[pygame.K_DOWN]:
            self.zoom_target_y += 10
            self.update_last_position()
        if pressed[pygame.K_RIGHT]:
            self.zoom_target_x += 10
            self.update_last_position()
        if pressed[pygame.K_LEFT]:
            self.zoom_target_x -= 10
            self.update_last_position()

    def blit_position(self, target):
        if self.adjust:
            if self.zoom_target_x < 800:
                self.zoom_target_x += 1
            if self.zoom_target_x > 800:
                self.zoom_target_x -=1
            if self.zoom_target_y > 768/2:
                self.zoom_target_y -= 1
            if self.zoom_target_y < 768/2:
                self.zoom_target_y += 1
        x = (target.rect.x - self.zoom_target_x) * self.zoom
        y = (target.rect.y - self.zoom_target_y) * self.zoom
        return x + 800, y + 768/2

    def center_blit(self, target, object):
        x = (target.rect.x - object.rect.center[0]) * self.zoom
        y = (target.rect.y - object.rect.center[1]) * self.zoom
        return x + self.zoom_target_x, y + self.zoom_target_y

    def follow(self, target):
        self.zoom_target_x = target.rect.center[0]
        self.zoom_target_y = target.rect.center[1]

    def player_blit(self, object):
        if not self.set:
            self.zoom_target_x = object.rect.center[0]
            self.zoom_target_y = object.rect.center[1]
            self.set = True
        if self.zoom_target_x < 800:
            self.zoom_target_x += 5
        if self.zoom_target_x > 800:
            self.zoom_target_x -= 5
        if self.zoom_target_y > 768/2:
            self.zoom_target_y -= 5
        if self.zoom_target_y < 768/2:
            self.zoom_target_y += 5

        x = self.zoom_target_x
        y = self.zoom_target_y
        return x, y

    def reset(self):
        self.adjust = True
        self.zoom_target_x = 800
        self.zoom_target_y = 768/2
        # self.zoom_target_x = object.rect.center[0]
        # self.zoom_target_y = object.rect.center[1]
        self.last_position = [0, 0]
        self.zoom = 1
        self.first = True
        self.set = False
        #self.game.map.resize()
