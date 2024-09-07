import pygame
from data.src.setup import get_mask_rect
from .animation import EntityAnimation
from typing import *
from data.src.GameElement import GameElement

def draw_health_bar(surf: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], border_c: tuple[int, int, int],
                    back_c: tuple[int, int, int], health_c: tuple[int, int, int], progress: float) -> None:
    pygame.draw.rect(surf, back_c, (*pos, *size))
    pygame.draw.rect(surf, border_c, (*pos, *size), 1)
    inner_pos = (pos[0] + 1, pos[1] + 1)
    inner_size = ((size[0] - 2) * progress, size[1] - 2)
    rect = (round(inner_pos[0]), round(inner_pos[1]), round(inner_size[0]), round(inner_size[1]))
    
    pygame.draw.rect(surf, health_c, rect)


class Shadow(GameElement):

    def __init__(self, game, player):
        super().__init__(game)
        self.player = player
        self.alive = True
        self.width = 10
        self.height = 3
        self.rect = pygame.Rect(player.hitbox.bottomleft[0] / 4, player.hitbox.bottomleft[1] / 4, self.width,
                                self.height)
        self.rect.midtop = (player.hitbox.midbottom[0] / 4, player.hitbox.midbottom[1] / 4)
        self.color = (0, 0, 0, 125)
        self.sizes = [10, 4]
        self.index = 0

    

    def update(self, dt: float) -> None:
        self.rect.midtop = ((self.player.rect.midbottom[0] / 4) , (self.player.rect.midbottom[1] + self.player.height)/ 4 )
        self.rect.size = self.sizes
        if self.player.dead:
            self.alive = False
   

    def draw(self, surface: pygame.Surface) -> None:
        rect = self.rect.copy()
        if self.game.camera.camera_target:
            result = [x - y for x, y in zip(self.game.camera.original_targets, [self.game.camera.zoom_target_x, self.game.camera.zoom_target_y])]
            rect.midtop = ((self.player.rect.midbottom[0] - result[0] / self.game.camera.zoom_factor)/ 4, 
                        (self.player.rect.midbottom[1] - result[1] / self.game.camera.zoom_factor-self.player.height * 2)/ 4)

        pygame.draw.ellipse(self.game.display.particle_screen, self.color, rect)


class Entity(GameElement):

    def __init__(self, game):
        super().__init__(game) 
        self.image = None
        self.load_image()
        self.rect = self.image.get_rect()
        self.hitbox = None
        self.update_hitbox()
        self.speed_multiplier = 2
        self.can_move = True
        self.position = []
        self.shadow = Shadow(game, self)
        self.direction = 'right'
        self.can_attack = False
        self.player = False
        self.height = 0 # height from the ground
        # self.game.particle_manager.add_particle(self.shadow)

    def load_image(self) -> None:
        pass

    def update_hitbox(self) -> None:
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom
    
    def resize(self) -> None:
        """
        Resizes the entity's image based on the game's camera zoom level.
        """
        size = (self.size[0] * self.game.camera.zoom_factor, self.size[1] * self.game.camera.zoom_factor)
        self.image = pygame.transform.scale(self.image, size)

    

class Character(Entity):
    size: tuple[int, int] = (64, 64)

    def __init__(self, game) -> None:
        super().__init__(game)
        self.velocity: list[int, int] = [0, 0] # velocity, the change in position
        self.anim_direction: str = 'right' # animation direction
        self.animation: EntityAnimation = EntityAnimation(self, game) # animation manager
        self.dead: bool = False # is the entity dead
        self.hurt: bool = False # is the entity hurt
        self.hurt_timer: int = 0 # hurt timer
        self.targetable: bool = True # can be targeted by enemies/player
        self.roll = False # is the entity rolling


    def load_image(self) -> None:
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}/idle/idle0.png'),
                                            self.size).convert_alpha()

    def set_velocity(self, velocity: list[int, int]) -> None:
        self.velocity = velocity

    def moving(self) -> bool:
        return sum(self.velocity) != 0

    def update(self) -> None:
        self.rect.move_ip(*self.velocity)
        self.hitbox.move_ip(*self.velocity)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def wall_collision(self) -> None:
        if self.hitbox.topright[0] + self.velocity[0] > 1600 or self.hitbox.x + self.velocity[0] < 0:
            self.velocity = [0, 0]
        # else:
        #     self.position[0] += self.velocity[0]
        if self.hitbox.midbottom[1] + self.velocity[1] < 256 or self.hitbox.bottomleft[1] + self.velocity[1] > 768:
            self.velocity = [0, 0]
        # else:
        #     self.position[1] += self.velocity[1]
    def correct_position(self) -> None:
        #calculate the difference between position and rect.topleft and add it to position

        x, y = self.position[0] - self.rect.topleft[0], self.position[1] - self.rect.topleft[1]
        self.position[0] -= int(x)
        self.position[1] -= int(y)


    def draw_health(self, surf: pygame.Surface) -> None:
        health_rect = pygame.Rect(0, 0, 30, 8)
        health_rect.midbottom = self.rect.centerx, self.rect.top
        draw_health_bar(surf, health_rect.topleft, health_rect.size,
                        (1, 0, 0), (255, 0, 0), (0, 255, 0), self.hp / self.max_hp)
    
    def hurting(self) -> pygame.Surface:
        """
        Returns a surface with a color key set to (0, 0, 0) representing the mask of the entity's image.

        Returns:
            pygame.Surface: A surface with a color key set to (0, 0, 0) representing the mask of the entity's image.
        """
        mask = pygame.mask.from_surface(self.image)
        mask_surf = mask.to_surface()
        mask_surf.set_colorkey((0, 0, 0))
        return mask_surf
    
    def udpate(self):
        pass
