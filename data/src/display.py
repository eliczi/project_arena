import pygame

world_size = (1600, 768 + 64)


class Display:

    def __init__(self, game):
        self.game = game
        self.display = pygame.display.set_mode(world_size, pygame.RESIZABLE)
        self.screen = pygame.Surface(world_size).convert()
        self.particle_screen = pygame.Surface((world_size[0] / 4, world_size[1] / 4),
                                              pygame.SRCALPHA).convert_alpha()
        self.dest_surf = pygame.Surface((world_size[0], world_size[1]), pygame.SRCALPHA).convert_alpha()
        self.surface = None

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
        self.screen.fill((0, 0, 0))

    def blit_display(self):
        position = ((self.display.get_width() - world_size[0]) / 2, (self.display.get_height() - world_size[1]) / 2)
        self.display.blit(self.screen, position)
