import pygame

world_size = (1600, 768 + 64)
import random
from data.src.utils.utils import wait


class ScreenShake:

    def __init__(self, display):
        self.display = display
        self.timer = 0
        self.screen_position = [0, 0]
        self.shake = False

    def update(self):
        if self.shake:
            return self.screen_position

    def shake_screen(self):
        if self.shake:
            self.screen_shake()

    def screen_shake(self, amount, intensity):
        """Intensity should be relatively low, 3 is good enough"""
        if not wait(self.display.game, self.timer, amount):
            self.screen_position = [random.randint(-intensity, intensity), random.randint(-intensity, intensity)]


class Display:

    def __init__(self, game):
        self.game = game
        self.display = pygame.display.set_mode(world_size, pygame.RESIZABLE)
        self.screen = pygame.Surface(world_size).convert()
        self.screen_position = [0, 0]
        self.particle_screen = pygame.Surface((world_size[0] / 4, world_size[1] / 4),
                                              pygame.SRCALPHA).convert_alpha()
        self.dest_surf = pygame.Surface((world_size[0], world_size[1]), pygame.SRCALPHA).convert_alpha()
        self.surface = None
        self.timer = 0

    def blit_default_particle_screen(self):
        # if self.game.particle_manager.particles:
        self.screen.blit(
            pygame.transform.scale(self.particle_screen, (world_size[0], world_size[1]), self.dest_surf),
            (0, 0))

    def blit_resized_particle_screen(self):
        x = (0 - self.game.camera.zoom_target_x) * self.game.camera.zoom
        y = (0 - self.game.camera.zoom_target_y) * self.game.camera.zoom
        position = (x + self.game.camera.zoom_target_x, y + self.game.camera.zoom_target_y)

        self.surface = pygame.transform.scale(self.particle_screen.copy(),
                                              (world_size[0] * self.game.camera.zoom,
                                               world_size[1] * self.game.camera.zoom))
        self.screen.blit(self.surface, position)

    def blit_particle_screen(self):
        if self.game.camera.zoom == 1:
            self.blit_default_particle_screen()
        else:
            self.blit_resized_particle_screen()

    def update_screen(self):
        self.screen_shake()

    # self.screen.fill((0, 0, 0))

    def blit_display(self):
        position = ((self.display.get_width() - world_size[0]) / 2, (self.display.get_height() - world_size[1]) / 2)
        self.display.blit(self.screen, self.screen_position)

    def screen_shake(self):
        if not wait(self.game, self.timer, 150):
            self.screen_position = [random.randint(-3, 3), random.randint(-3, 3)]
