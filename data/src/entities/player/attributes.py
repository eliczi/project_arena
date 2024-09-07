import pygame

font = pygame.font.SysFont('Bitty', 30)


class Attributes:

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.strength = 0
        self.agility = 0
        self.attack = 0
        self.defense = 0
        self.vitality = 0
        self.charisma = 0
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.max_rolls = 1
        self.rolls = self.max_rolls
        self.magicka = 0
        self.max_hp = 100
        self.hp = self.max_hp
        self.gold = 100


    def draw(self):
        y = 0
        for attr, value in self.__dict__.items():
            if attr not in ['game', 'player']:
                text_surface = font.render(f'{attr}:{value}', False, (255, 255, 255))
                self.game.display.screen.blit(text_surface, (500, y))
                y += 20





