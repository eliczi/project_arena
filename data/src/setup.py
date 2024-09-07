import pygame
import time

world_size = (1600, 768)


def get_mask_rect(surf, top=0, left=0):
    """Returns minimal bounding rectangle of an image"""
    surf_mask = pygame.mask.from_surface(surf)
    rect_list = surf_mask.get_bounding_rects()
    if rect_list:
        surf_mask_rect = rect_list[0].unionall(rect_list)
        surf_mask_rect.move_ip(top, left)
        return surf_mask_rect


class Time:

    def __init__(self, game):
        self.game = game
        self.clock = pygame.time.Clock()
        self.fps = 30
        self.prev_time = 0
        self.dt = 0
        self.game_speed = 1.0
        self.slow_down = SlowDown(self)
        self.font = pygame.font.SysFont('Bitty', 30)

    def dtf(self):
        return self.dt * self.game_speed

    def update(self):
        now = time.time()
        self.dt = now - self.prev_time
        self.prev_time = now
        self.slow_down.update()
        self.clock.tick()

    def draw_fps(self):
        #return
        text_surface = self.font.render(f'{self.clock.get_fps()}', False, (255, 255, 255))
        self.game.display.screen.blit(text_surface, (0, 0))


class SlowDown:
    def __init__(self, time: Time):
        self.time = time
        self.slow_time = False
        self.slow_down_amount = 0.25
        self.slow_down_cooldown = 0
        self.slow_down_duration = 1000
        self.slow_down_init_time = 0
        self.slow_down_current_time = 0

    def set_slow_down_amount(self):
        speed = self.slow_down_amount + (1 - self.slow_down_amount) * (
                self.slow_down_current_time / self.slow_down_duration)
        return speed

    def init_slow_down(self, duration, slow_down_amount):
        self.slow_time = True
        self.slow_down_duration = duration
        self.slow_down_amount = slow_down_amount
        self.slow_down_cooldown = pygame.time.get_ticks()

    def stop_slow_down(self):
        if pygame.time.get_ticks() - self.slow_down_cooldown > self.slow_down_duration:
            self.slow_down_cooldown = pygame.time.get_ticks()
            self.slow_time = False
            self.time.game_speed = 1.0

    def slow_down(self):
        if self.slow_time:
            self.time.game_speed = self.set_slow_down_amount()
            self.slow_down_current_time = pygame.time.get_ticks() - self.slow_down_cooldown
            self.stop_slow_down()

    def update(self):
        self.slow_down()
