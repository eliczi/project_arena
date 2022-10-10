import random
import pygame

pygame.init()
pygame.mixer.init()
from data.src.entities.player.player import Player
from .objects.object_manager import ObjectManager
from .objects.object import Object
from .vfx.particle_manager import ParticleManager
from data.src.entities.enemies.enemy_manager import EnemyManager
from data.src.entities.npc.npc_manager import NpcManager
from .camera import Camera
from .map import Arena, Market
from .setup import Time
from .display import Display
from .menu import MainMenu
from data.src.vfx.ground_ripple import GroundRipple
from .entities.player.items import Items
world_size = (1600, 768)
BLACK = (0, 0, 0)
from data.src.utils.utils import wait
from data.src.vfx.ground_ripple import Crack
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
        self.npc_manager = NpcManager(self)
        self.camera = Camera(self)
        self.map = Market(self)
        self.menu = MainMenu(self)
        self.rect = pygame.Rect(0, 0, 250, 250)
        self.events = []
        self.can_close = True
        self.cooldown = 0
        self.init()

    def init(self):
        self.npc_manager.populate()

    def update(self):
        self.time.update()
        self.display.update_screen()
        self.npc_manager.update()
        self.input()
        self.player.update()
        self.enemy_manager.update()
        self.object_manager.update()
        self.particle_manager.update()


    def draw(self):
        self.display.particle_screen.fill((0, 0, 0, 0))
        self.map.draw(self.display.screen)
        self.enemy_manager.draw(self.display.screen)
        self.npc_manager.draw(self.display.screen)
        self.particle_manager.draw(self.display.particle_screen)
        self.display.blit_particle_screen()
        self.player.draw(self.display.screen)

        self.object_manager.draw()

        self.time.draw_fps()
        self.display.blit_display()

    def input(self):
        self.events = pygame.event.get()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        mx, my = pygame.mouse.get_pos()
        # for event in self.events:
        #     if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.player.jump.jump:
        #         self.particle_manager.add_particle(Crack((mx, my)))
        #self.camera.input()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_ESCAPE] and wait(self, self.cooldown, 250) and self.can_close:
            self.running = False

    def run_game(self):
        while self.running:
            self.update()
            self.draw()
            pygame.display.flip()
            self.camera.zoom_change = False
        pygame.quit()
