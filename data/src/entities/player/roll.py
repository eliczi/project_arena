import pygame
import random
from pygame.math import Vector2
import math


class Roll:

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.roll = False
        self.roll_destination = [0, 0]
        self.rolling_distance = 250
        self.rolling_speed = 2.5
        self.roll_cooldown = 250
        self.roll_time = 0

    def assign_roll_destination(self): # describe it!!!
        x = [i for i, e in enumerate(self.player.velocity) if e != 0]
        for i in range(2):
            if all(self.player.velocity):
                sign = self.player.velocity[i] / abs(self.player.velocity[i])  # negative or positive
                self.roll_destination[i] = self.player.position[i] + (math.sqrt(2) / 2 * self.rolling_distance * sign)
            elif i in x:
                sign = self.player.velocity[i] / abs(self.player.velocity[i])  # negative or positive
                self.roll_destination[i] = self.player.position[i] + self.rolling_distance * sign
            else:
                self.roll_destination[i] = self.player.position[i]
        if sum(self.player.velocity) == 0:#self.player.velocity[0] == 0 and self.player.velocity[1] == 0:#
            if self.player.anim_direction == 'right':
                self.roll_destination[0] = self.player.position[0] + self.rolling_distance
            else:
                self.roll_destination[0] = self.player.position[0] - self.rolling_distance
            self.roll_destination[1] = self.player.position[1]

    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and not self.roll and pygame.time.get_ticks() - self.roll_time > self.roll_cooldown:
            self.roll = True
            self.player.can_move = False
            self.roll_destination = [0, 0]
            self.assign_roll_destination()

    def rolling(self):
        if not self.roll:
            return
        vector = Vector2(self.roll_destination[0] - self.player.position[0],
                         self.roll_destination[1] - self.player.position[1])
        if vector.length() < 5:
            self.roll = False
            self.player.velocity = [0, 0]
            self.player.can_move = True

        if self.roll and vector.length() > 0:
            dt = self.game.time.dt * self.game.time.game_speed
            vector.scale_to_length(dt * self.player.speed * self.player.speed_multiplier * self.rolling_speed)
            if all([vector.x, vector.y]):
                vector.x = vector.x * math.sqrt(2) / 2
                vector.y = vector.y * math.sqrt(2) / 2
            self.player.velocity = [vector.x, vector.y]
        # else:
        #     self.roll = False
        #     self.player.can_move = True
        #     self.roll_time = pygame.time.get_ticks()
