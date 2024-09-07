import pygame
from typing import List, Optional, Tuple
from .entities.player.player import Player
from .entities.entity import Entity
from .utils.utils import wait



class SmoothZoom:

    def __init__(self) -> None:
        self.number_of_zooms = 50
        self.smooth_zoom = False

    def update(self):
        pass
    
class Camera:

    def __init__(self, game) -> None:
        self.game  = game
        self.zoom_factor: float = 1.0
        self.original_targets: List[int] = [800,  384]
        self.zoom_target_x: float = 800
        self.zoom_target_y: float = 384
        self.last_position: List[float] = [0, 0]
        self.zoom_change: bool = False
        self.camera_target: Optional[Entity] = None  # The entity the camera is following
        self.zooming = False


    def update(self):
        pass


    def zoom(self, target=None, zoom_factor=1.05, zoom_type='in'):
        if zoom_type == 'in':
            self.zoom_factor = self.zoom_factor * zoom_factor
        elif zoom_type == 'out':
            if self.zoom_factor > 0.01:
                self.zoom_factor /= zoom_factor
        self.zoom_change = True
        self.game.map.resize()

    def input(self):
        step_size: int = 5
        
        key_to_function = {
            pygame.K_z: lambda: self.zoom(zoom_type='in'),
            pygame.K_x: lambda: self.zoom(zoom_type='out'),
            pygame.K_r: lambda: [self.reset(), self.game.map.resize()],
            pygame.K_UP: lambda: setattr(self, 'zoom_target_y', self.zoom_target_y - step_size),
            pygame.K_DOWN: lambda: setattr(self, 'zoom_target_y', self.zoom_target_y + step_size),
            pygame.K_RIGHT: lambda: setattr(self, 'zoom_target_x', self.zoom_target_x + step_size),
            pygame.K_LEFT: lambda: setattr(self, 'zoom_target_x', self.zoom_target_x - step_size),
        }

        pressed = pygame.key.get_pressed()
        for key, function in key_to_function.items():
            if pressed[key]:
                function()

    def blit_position(self, target) -> Tuple[float, float]:
        x = (target.rect.x - self.zoom_target_x) * self.zoom_factor
        y = (target.rect.y - self.zoom_target_y) * self.zoom_factor

        return x + 800, y + 768/2
    
    def center_blit(self, target) -> Tuple[float, float]:
        """
        Centers the target object on the camera and calculates the blit coordinates of the object calling this function.
        """
        x: float = (target.rect.x - self.camera_target.rect.topleft[0]) * self.zoom_factor
        y: float = (target.rect.y - self.camera_target.rect.topleft[1]) * self.zoom_factor

        return x + self.zoom_target_x, y + self.zoom_target_y


    def reset(self):
        self.zoom_target_x = 800
        self.zoom_target_y = 768/2
        self.last_position = [0, 0]
        self.zoom_factor = 1
