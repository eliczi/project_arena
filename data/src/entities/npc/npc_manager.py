import pygame
from data.src.entities.npc.weapon_merchant import WeaponMerchant


class NpcManager:
    def __init__(self, game):
        self.game = game
        self.npcs = []
        self.interaction = False

    def populate(self):
        self.npcs.append(WeaponMerchant(self.game))

    def draw(self, surface):
        for npc in self.npcs:
            npc.draw(surface)

    def update(self):
        for npc in self.npcs:
            npc.update()

