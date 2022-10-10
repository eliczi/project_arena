import pygame
from data.src.objects.weapons.gold_dagger import GoldDagger
from data.src.objects.weapons.big_golden_sword import BigGoldenSword


class ObjectManager:
    def __init__(self, game):
        self.objects = []
        self.game = game
        self.interaction = False

    def remove_item(self, item):
        if item in self.objects:
            self.objects.remove(item)

    def add_item(self, item):
        self.objects.append(item)

    def update(self):
        for o in self.objects:
            o.update()
            if self.interaction:
                o.interact()

    def draw(self):
        for o in self.objects:
            o.draw(self.game.display.screen)
