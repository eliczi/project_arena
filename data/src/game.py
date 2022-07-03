import random
import pygame

pygame.init()
pygame.mixer.init()
from data.src.entities.player.player import Player
from .objects.object_manager import ObjectManager
from .objects.object import Object
from .vfx.particle_manager import ParticleManager
from data.src.entities.enemies.enemy_manager import EnemyManager
from .camera import Camera
from .map import Arena, Market
from .setup import Time
from .display import Display
from .menu import MainMenu
from .entities.player.items import Items
world_size = (1600, 768)
BLACK = (0, 0, 0)


class Game:

    def __init__(self):
        self.display = Display(self)
        self.time = Time(self)
        self.screen_position = (0, 0)
        self.running = True
        self.particle_manager = ParticleManager(self)
        self.player = Player(self)
        self.object_manager = ObjectManager(self)
        self.enemy_manager = EnemyManager(self)
        self.camera = Camera(self)
        self.map = Arena(self)
        self.menu = MainMenu(self)
        self.rect = pygame.Rect(0, 0, 250, 250)
        self.events = []

    def update(self):
        self.time.update()
        self.display.update_screen()
        self.input()
        self.player.update()
        self.enemy_manager.update()
        self.object_manager.update()
        self.particle_manager.update()


    def draw(self):
        self.display.particle_screen.fill((0, 0, 0, 0))
        self.map.draw(self.display.screen)
        self.enemy_manager.draw(self.display.screen)
        self.player.draw(self.display.screen)
        self.object_manager.draw()
        self.particle_manager.draw(self.display.particle_screen)
        self.display.blit_particle_screen()
        self.time.draw_fps()
        self.display.blit_display()

    def input(self):
        self.events = pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.camera.input()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE]:
            self.running = False

    def run_game(self):
        while self.running:
            self.update()
            self.draw()
            pygame.display.flip()
            self.camera.zoom_change = False
        pygame.quit()
