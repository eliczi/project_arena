import pygame
from data.src.entities.entity import Character
from data.src.utils.utils import perfect_outline
from data.src.objects.object import ShowName
from data.src.objects.object import Object
from data.src.objects.weapons.gold_dagger import GoldDagger
from data.src.objects.weapons.steel_dagger import SteelDagger
from data.src.objects.weapons.mini_dagger import MiniDagger
from data.src.objects.weapons.big_golden_sword import BigGoldenSword
from data.src.objects.weapons.hammer import Hammer
from data.src.objects.weapons.sabre import Sabre
from data.src.objects.weapons.wooden_sword import WoodenSword


class Inventory:

    def __init__(self, npc, game):
        self.game = game
        self.npc = npc
        self.show_image = None
        self.load_image()
        self.rect = self.show_image.get_rect()
        self.locations = []
        self.populate_locations()
        self.items = [None for i in range(12)]
        self.populate_inventory()
        self.clicked = -1
        # self.items = {}
        self.mouse_down = False
        self.change_position = True
        self.original_position = [0, 0]
        self.position = None
        self.offset = [0, 0]

    def populate_locations(self):
        x, y = 60, 60
        for _x in range(2):
            for _y in range(4):
                self.locations.append(pygame.Rect((x + (_x * (8 + 64)), y + (_y * (8 + 64))), (64, 64)))
        self.locations.append(pygame.Rect((60 + 128 + 16, 60), (64, 128 + 8)))
        self.locations.append(pygame.Rect((60 + 192 + 24, 60), (64, 128 + 8)))
        self.locations.append(pygame.Rect((60 + 128 + 16, 196 + 8), (64, 128 + 8)))
        self.locations.append(pygame.Rect((60 + 192 + 24, 196 + 8), (64, 128 + 8)))
        # self.locations.append(pygame.Rect((60 + 192 + 24, 60), (64, 182 + 16))

    def load_image(self):
        self.show_image = pygame.transform.scale(pygame.image.load(f'data/assets/shop_items.png').convert_alpha(),
                                                 size=(400, 400))

    def populate_inventory(self):
        self.items[0] = GoldDagger(self.game, self.locations[0].topleft)
        self.items[1] = SteelDagger(self.game, self.locations[1].topleft)
        self.items[2] = MiniDagger(self.game, self.locations[2].topleft)
        self.items[8] = BigGoldenSword(self.game, self.locations[8].topleft)
        self.items[9] = Hammer(self.game, self.locations[9].topleft)
        self.items[11] = Sabre(self.game, self.locations[11].topleft)
        self.items[10] = WoodenSword(self.game, self.locations[10].topleft)

    def get_position(self, x, y) -> tuple[int, int]:
        return x + self.offset[0], y + self.offset[1]

    def draw(self, surface):
        surface.blit(self.show_image, self.rect)
        pos = pygame.mouse.get_pos()
        for rect in self.locations:
            if rect.collidepoint(pos[0] - self.offset[0], pos[1] - self.offset[1]):
                try:
                    position = (rect.x + self.offset[0], rect.y + self.offset[1])
                    pygame.draw.rect(surface, (255, 255, 255), (*position, rect.w, rect.h), 3)
                    self.items[self.locations.index(rect)].draw_merchant = True
                except:
                    pass
            elif not rect.collidepoint(pos[0] - self.offset[0], pos[1] - self.offset[1]):
                try:
                    self.items[self.locations.index(rect)].draw_merchant = False
                except:
                    pass
        if self.clicked >= 0:
            rect = self.locations[self.clicked]
            position = (rect.x + self.offset[0], rect.y + self.offset[1])
            pygame.draw.rect(surface, (255, 255, 255), (*position, rect.w, rect.h), 3)
        for item in [item for item in self.items if item is not None]:
            position = (item.rect.x + self.offset[0], item.rect.y + self.offset[1])
            item.draw(surface, position)
        for item in [item for item in self.items if item is not None]:
            item.draw_merchant_information(surface)

    def input(self):
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for rect in self.locations:
                    if rect.collidepoint(pos[0] - self.offset[0], pos[1] - self.offset[1]) and self.items[
                        self.locations.index(rect)]:
                        self.clicked = self.locations.index(rect)
                        self.buy()
        # COPIED CODE
        pos = pygame.mouse.get_pos()
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
        if self.mouse_down and self.rect.collidepoint(pos):
            if self.change_position:
                self.position = [pos[0], pos[1]]
                self.original_position = [self.rect.x, self.rect.y]
            self.change_position = False
            self.offset = [self.original_position[0] + pos[0] - self.position[0],
                           self.original_position[1] + pos[1] - self.position[1]]
            self.rect.update(*self.offset, 70 * 6, 76 * 6)
        else:
            self.change_position = True

    def update(self):
        self.input()

    def buy(self):
        item = self.items[self.clicked]
        player = self.game.player
        if item.price <= player.attributes.gold:
            #if player.items.items['weapon']['item'] is None:
            player.items.items['weapon']['item'] = item
            self.items[self.clicked] = None
            player.attributes.gold -= item.price
            self.clicked = -1
            item.player = player



class WeaponMerchant(Character):
    name = 'weapon_merchant'
    path = f'data/assets/characters/weapon_merchant/'

    def __init__(self, game):
        super().__init__(game)
        self.interaction = False
        self.rect = self.image.get_rect(center=(300, 300))
        self.items_for_sale = []
        self.show_name = ShowName(self)
        self.open_inventory = False
        self.inventory = Inventory(self, game)

    def load_image(self):
        self.image = pygame.transform.scale(pygame.image.load(f'{self.path}/idle/idle0.png'),
                                            self.size).convert_alpha()

    def detect_collision(self):
        if self.game.player.hitbox.colliderect(self.hitbox):
            self.interaction = True
        else:
            self.interaction = False
            self.open_inventory = False
            self.show_name.reset_line_length()

    def draw(self, surface):
        if self.game.player.hitbox.colliderect(self.hitbox):
            perfect_outline(self.image, self.rect, surface)
        surface.blit(self.image, self.rect)
        if self.interaction:
            self.show_name.draw(surface, self.rect)
        if self.open_inventory:
            self.inventory.draw(surface)

    def update(self):
        self.update_hitbox()
        self.detect_collision()
        self.input()
        if self.open_inventory:
            self.inventory.update()

    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_e]:
            if self.game.player.hitbox.colliderect(self.hitbox) and not self.open_inventory:
                self.open_inventory = True
                # self.game.player.items.draw_items = not self.game.player.items.draw_items
               # self.game.can_close = False
        if pressed[pygame.K_ESCAPE] and self.open_inventory:
            self.open_inventory = False
            # self.game.player.items.draw_items = not self.game.player.items.draw_items
            self.game.cooldown = pygame.time.get_ticks()
            self.game.can_close = True
