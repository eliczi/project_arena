import pygame


class Bar:

    def __init__(self, player, game):
        self.game = game
        self.image = None
        self.load_image()
        self.player = player
        self.attributes = player.attributes

    def load_image(self):
        self.image = pygame.image.load(self.path).convert_alpha()
        w, h = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (w * 4, h * 4))

    def draw(self, surface):
        pass


class HealthBar(Bar):
    path = 'data/assets/player_info/basic_health_bar.png'
    max_hp_color = (98, 35, 47)
    hp_color = (217, 78, 56)
    frame_position = (0, 0)

    def __init__(self, player, game):
        self.image = None
        super().__init__(player, game)

    def draw(self, surface):
        length = 116
        hp = self.attributes.hp / self.attributes.max_hp * length
        pygame.draw.rect(surface, self.max_hp_color, (20, 10, length, 20))
        pygame.draw.rect(surface, self.hp_color, (20, 10, hp, 20))
        self.draw_frame(surface)
        self.draw_hp_info(surface)

    def draw_hp_info(self, surface):
        font = 'data/assets/Minecraft.ttf'
        text = f'{self.attributes.hp}/{self.attributes.max_hp}'
        text_surface = pygame.font.Font(font, 15).render(text, True, (255, 255, 255))
        surface.blit(text_surface, (116 / 2, 10))

    def draw_frame(self, surface):
        surface.blit(self.image, self.frame_position)


class StaminaBar(Bar):
    path = 'data/assets/player_info/basic_stamina_bar.png'
    max_stamina_color = (30, 60, 130)
    stamina_color = (56, 111, 199)

    def __init__(self, player, game):
        self.stamina_bar = None
        super().__init__(player, game)

    def draw(self, surface):
        length = 116
        stamina = self.attributes.stamina / self.attributes.max_stamina * length
        pygame.draw.rect(surface, self.max_stamina_color, (20, 50, length, 20))
        pygame.draw.rect(surface, self.stamina_color, (20, 50, stamina, 20))
        self.draw_frame(surface)
        self.draw_stamina_info(surface)

    def draw_stamina_info(self, surface):
        font = 'data/assets/Minecraft.ttf'
        text_surface = pygame.font.Font(font, 15).render(f'{self.attributes.stamina}/{self.attributes.max_stamina}',
                                                         True,
                                                         (255, 255, 255))
        surface.blit(text_surface, (116 / 2, 50))

    def draw_frame(self, surface):
        surface.blit(self.image, (0, 40))


class Roll(Bar):
    path = 'data/assets/player_info/roll.png'

    def __init__(self, player, game):
        super().__init__(player, game)

    def draw_roll_info(self, surface):
        font = 'data/assets/Minecraft.ttf'
        test = f'{self.attributes.rolls}/{self.attributes.max_rolls}'
        text_surface = pygame.font.Font(font, 15).render(test, True, (255, 255, 255))
        surface.blit(text_surface, (116 / 2, 100))

    def draw(self, surface):
        surface.blit(self.image, (20, 100))
        self.draw_roll_info(surface)


class Hud:

    def __init__(self, player, game):
        self.health = HealthBar(player, game)
        self.stamina = StaminaBar(player, game)
        #self.roll = Roll(player, game)

    def draw(self, surface):
        for p, value in vars(self).items():
            value.draw(surface)
