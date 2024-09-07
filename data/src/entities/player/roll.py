import pygame
from pygame.math import Vector2
import math


class Roll:

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.roll = False
        self.roll_destination = [0, 0]  # where player roll ends
        self.rolling_distance = 250  # how much distance player covers while rolling
        self.rolling_speed = 2.5  # how fast rolls
        self.roll_cooldown = 250
        self.roll_time = 0  # used to measure cooldown

    def assign_roll_destination(self):
        player_direction = [1 if x > 0 else -1 if x < 0 else 0 for x in self.player.velocity]
        if all(player_direction):
            self.roll_destination = [x + (math.sqrt(2) / 2 * self.rolling_distance * y)
                                     for x, y in zip(self.player.position, player_direction)]
        elif any(player_direction):
            self.roll_destination = [x + self.rolling_distance * y
                                     for x, y in zip(self.player.position, player_direction)]
        else:  # player_direction = [0,0]
            if self.player.direction == 'right':
                self.roll_destination[0] = self.player.position[0] + self.rolling_distance
            else:
                self.roll_destination[0] = self.player.position[0] - self.rolling_distance
            self.roll_destination[1] = self.player.position[1]  # y coordinate stays the same

    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and not self.roll and pygame.time.get_ticks() - self.roll_time > self.roll_cooldown:
            self.roll_time = pygame.time.get_ticks()
            self.roll = True
            self.player.can_move = False
            self.roll_destination = [0, 0]  # reseting roll destination
            self.assign_roll_destination()  # assigning new role destination

    def update(self):
        if not self.roll:
            self.player.targetable = True
            return
        self.player.targetable = False
        vector = Vector2(self.roll_destination[0] - self.player.position[0],
                         self.roll_destination[1] - self.player.position[1])
        if vector.length() < 5:
            self.roll = False
            self.player.velocity = [0, 0]
            self.player.can_move = True
        if self.roll and vector.length() > 0:
            dt = self.game.time.dt * self.game.time.game_speed
            # add additional speed if player rolls diogonally
            vector.scale_to_length(dt * self.player.speed * self.player.speed_multiplier * self.rolling_speed)
            if all([vector.x, vector.y]):
                vector.x = vector.x * math.sqrt(2) / 2
                vector.y = vector.y * math.sqrt(2) / 2
            self.player.velocity = [vector.x, vector.y]
