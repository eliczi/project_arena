import pygame


class Items:

    def __init__(self, game):
        self.game = game
        self.image = None
        self.original_image = None
        self.load_image()
        self.rect = self.image.get_rect()
        self.items = {'ring1': {'item': None,
                                'position': (0, 0)},
                      'helmet': {'item': None,
                                 'position': (0, 1)},
                      'ring2': {'item': None,
                                'position': (0, 2)},
                      'magic': {'item': None,
                                'position': (1, 0)},
                      'armor': {'item': None,
                                'position': (1, 1)},
                      'weapon': {'item': None,
                                 'position': (1, 2)},
                      'boots': {'item': None,
                                'position': (2, 0)},
                      'pants': {'item': None,
                                'position': (2, 1)},
                      'gloves': {'item': None,
                                 'position': (2, 2)}
                      }

        self.draw_items = False
        self.cool_down = 0
        self.mouse_down = False
        self.position = None
        self.change_position = True
        self.original_position = [0, 0]
        self.empty_slot_color = (143, 86, 59)

    def can_draw(self):
        if pygame.time.get_ticks() - self.cool_down > 150:
            self.cool_down = pygame.time.get_ticks()
            return True

    def input(self):
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
            position = [self.original_position[0] + pos[0] - self.position[0],
                        self.original_position[1] + pos[1] - self.position[1]]
            self.rect.update(*position, 70 * 6, 76 * 6)
        else:
            self.change_position = True

    def update(self):
        self.input()
        for item in self.items.values():
            if item['item'] is not None:
                item['item'].update()

    def load_image(self):
        self.image = pygame.image.load('data/assets/items.png')
        self.image = pygame.transform.scale(self.image, (70 * 6, 76 * 6))
        self.original_image = self.image

    # def draw_item_mouse_outline(self, surface, ):
    #     position_x = 0 + 9 * 6 + item['position'][1] * 16 * 6 + item['position'][1] * 2 * 6
    #     position_y = 0 + 9 * 6 + item['position'][0] * 16 * 6 + item['position'][0] * 2 * 6
    #     pygame.draw.rect(surface, (255, 255, 255), (position_x, position_y, 16 * 6, 16 * 6), 5)

    def draw_item(self, surface, item, key):  # change to blit image instead of surface
        position_x = 0 + 9 * 6 + item['position'][1] * 16 * 6 + item['position'][1] * 2 * 6
        position_y = 0 + 9 * 6 + item['position'][0] * 16 * 6 + item['position'][0] * 2 * 6
        pygame.draw.rect(surface, self.empty_slot_color, (position_x, position_y, 16 * 6, 16 * 6))
        image = item['item'].image
        image = pygame.transform.scale(image, (item['item'].size[0] * 1.5, item['item'].size[1] * 1.5))
        if key == 'weapon':
            pygame.draw.rect(surface, self.empty_slot_color, (position_x, position_y + 88, 16 * 6, 16 * 6))
            surface.blit(image, (position_x, position_y + 88))

    def draw_eq_items(self):
        for key, item in self.items.items():
            if item['item'] is not None:
                self.draw_item(self.image, item, key)

    def draw(self, surface):
        if self.draw_items:
            self.draw_eq_items()
            surface.blit(self.image, self.rect)
