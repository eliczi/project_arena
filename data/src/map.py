import pygame
from .setup import get_mask_rect
import csv, os

world_size = (1600, 768)


class Spritesheet(object):
    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert_alpha()

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, rectangle, x, y, spritesheet, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = spritesheet.image_at(rectangle)
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hitbox = get_mask_rect(self.image, self.rect.topleft[0] - 64, self.rect.topleft[1])

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    # def change_image(self, rectangle, spritesheet):
    #     self.image = spritesheet.image_at(rectangle)
    #     self.image = pygame.transform.scale(self.image, self.size)


class TileMap:
    original_tile_size = 64

    def __init__(self, game, csv_map):
        self.game = game
        self.csv_map = csv_map
        self.tile_size = self.original_tile_size
        self.spritesheet = Spritesheet('data/assets/spritesheet.png')
        self.wall_list = []
        self.tiles = []
        self.load_tiles(csv_map)
        self.size = (len(csv_map[0]) * self.original_tile_size, len(csv_map) * self.original_tile_size)
        self.original_map_surface = pygame.Surface(self.size).convert()
        self.original_map_surface.set_colorkey((0, 0, 0, 0))
        self.map_surface = None
        self.load_map()

    def resize(self):
        self.tile_size = self.game.camera.zoom * self.original_tile_size
        self.load_tiles(self.csv_map)
        self.load_map()

    def clear_map(self):
        self.map_surface = self.original_map_surface.copy()

    def load_map(self):
        self.original_map_surface.fill((0, 0, 0))
        for tile in self.tiles:
            tile.draw(self.original_map_surface)
        self.clear_map()

    @staticmethod
    def get_location(number):
        a = number // 16
        b = number % 16
        return b * 16, a * 16

    def load_tiles(self, csv_map):
        wall_list = (16, 17, 18, 240, 241, 117, 70)
        x, y = -64, 0
        tiles = []
        for row in csv_map:
            x = 0
            for tile in row:
                tiles.append(Tile((*self.get_location(int(tile)), 16, 16), x, y, self.spritesheet,
                                  (self.tile_size, self.tile_size)))
                if int(tile) in wall_list:
                    self.wall_list.append(tiles[-1])
                x += int(self.tile_size)
            y += int(self.tile_size)
        self.tiles = tiles


class Map:

    def __init__(self, game):
        self.game = game
        self.tile_maps = []
        self.wall_list = []
        self.load_tile_maps()
        self.dupa = (world_size[0] + 128, world_size[1] + 128)
        self.original_image = pygame.Surface(self.dupa, pygame.SRCALPHA).convert_alpha()
        self.load_map()
        self.rect = self.original_image.get_rect()
        self.image = self.original_image.copy()
        self.size = world_size

    def resize(self):
        size = (self.dupa[0] * self.game.camera.zoom, self.dupa[1] * self.game.camera.zoom)
        self.image = pygame.transform.scale(self.original_image, size)

    def load_tile_maps(self):
        for filename in os.listdir(self.path):
            f = os.path.join(self.path, filename)
            with open(f, newline='') as f:  # load room template
                reader = csv.reader(f)
                self.tile_maps.append(TileMap(self.game, list(reader)))
                for wall in self.tile_maps[-1].wall_list:
                    self.wall_list.append(wall)

    def load_map(self):
        self.original_image.fill((0, 0, 0))
        for tile_map in self.tile_maps:
            self.original_image.blit(tile_map.map_surface, (-64, 0))
            # for tile in tile_map.tiles:
            #     if tile.hitbox is not None:
            #         pygame.draw.rect(self.original_image, (255, 255, 255), tile.hitbox, 1)

    def draw(self, surface):
        if self.game.player.bullets:
            surface.blit(self.image, self.game.camera.center_blit(self, self.game.player.bullets[0]))
        else:
            surface.blit(self.image, self.game.camera.blit_position(self))

        # pygame.draw.rect(surface, (255, 255, 255), self.rect, 1)


class Market(Map):
    path = 'data/assets/map/market'
    name = 'market'
    wall_list = (16, 17, 18, 240, 241, 101, 117, 70)

    def __init__(self, game):
        super().__init__(game)


class Arena(Map):
    path = 'data/assets/map/arena'
    name = 'arena'

    def __init__(self, game):
        super().__init__(game)
        self.boundaries = (1600, 0, 320, 832)
