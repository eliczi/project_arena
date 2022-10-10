import random
import pygame
import math
from pygame.math import Vector2


class AttackReady:
    alpha = 255
    color = (255, 255, 255, alpha)

    # do two lines
    def __init__(self, center, player):
        self.center = [p / 4 for p in center]
        self.player = player
        self.angle = 45  # random.randint(-180, 180)
        self.perpendicular_straight = 1
        self.points = []
        self.lines = []
        self.length = 1
        self.max_length = 20
        self.create_polygon(self.length, self.angle)
        self.create_polygon(self.length, self.angle + 90)
        self.alive = True
        self.dir = None
        self.speed = 20
        self.radius = 1
        self.draw_lines = True
        self.calculate_direction()
        self.dir2 = None
        self.calculate_direction2()
        self.reverse = False

    def calculate_direction(self):
        self.dir = pygame.math.Vector2(self.lines[0][2] - self.lines[0][0])
        self.dir.normalize_ip()
        self.dir.scale_to_length(self.speed)

    def calculate_direction2(self):
        self.dir2 = pygame.math.Vector2(self.lines[1][2] - self.lines[1][0])
        self.dir2.normalize_ip()
        self.dir2.scale_to_length(self.speed)

    def create_polygon(self, length, angle):
        # 1
        x = self.center[0] + length * math.cos(math.radians(angle))
        y = self.center[1] + length * math.sin(math.radians(angle))
        self.points.append(Vector2([x, y]))
        # 2
        x = self.center[0] - length * math.cos(math.radians(angle))
        y = self.center[1] - length * math.sin(math.radians(angle))
        self.points.append(Vector2([x, y]))

        x1, x2 = self.points[0][0], self.points[1][0]
        y1, y2 = self.points[0][1], self.points[1][1]
        x3, y3 = self.center
        b = Vector2(y1 - y2, x2 - x1)
        b.normalize_ip()
        # 3
        x, y = Vector2(x3, y3) + self.perpendicular_straight * b
        self.points.append(Vector2([x, y]))
        # 4
        x, y = Vector2(x3, y3) - self.perpendicular_straight * b
        self.points.append(Vector2([x, y]))

        self.points[1], self.points[2] = self.points[2], self.points[1]
        self.lines.append(self.points)
        self.points = []

    def correct_position(self):
        position = None
        if self.player.direction == 'right':
            position = self.player.hitbox.topleft
        else:
            position = self.player.hitbox.topright
        if self.center[0] != position[0] / 4:
            for line in self.lines:
                for vector in line:
                    vector.x += position[0] / 4 - self.center[0]
            self.center[0] = position[0] / 4

        if self.center[1] != position[1] / 4:
            for line in self.lines:
                for vector in line:
                    vector.y += position[1] / 4 - self.center[1]
            self.center[1] = position[1] / 4

    def update(self, dt):
        self.correct_position()
        if self.reverse:
            self.lines[0][0] -= self.dir * dt * self.speed / 6
            self.lines[0][2] += self.dir * dt * self.speed / 6

            self.lines[1][0] -= self.dir2 * dt * self.speed / 6
            self.lines[1][2] += self.dir2 * dt * self.speed / 6

            self.radius -= dt * self.speed * 2
        else:
            self.lines[0][0] += self.dir * dt * self.speed / 6
            self.lines[0][2] -= self.dir * dt * self.speed / 6

            self.lines[1][0] += self.dir2 * dt * self.speed / 6
            self.lines[1][2] -= self.dir2 * dt * self.speed / 6

            self.radius += dt * self.speed * 2

        if Vector2(self.lines[0][0] - self.lines[1][0]).length() > 20:
            self.reverse = True
        if Vector2(self.lines[0][0] - self.lines[1][0]).length() < 2:
            self.reverse = False
        if self.radius > 11:
            self.reverse = True
        if self.radius < 1:
            self.reverse = False

    def draw(self, surface):
        if self.alive:
            if self.draw_lines:
                pygame.draw.polygon(surface, self.color, self.lines[0], width=0)
                pygame.draw.polygon(surface, self.color, self.lines[1], width=0)
            if self.player.direction == 'right':
                pygame.draw.circle(surface, self.color, [x / 4 for x in self.player.hitbox.topleft], self.radius, 1)
                pygame.draw.circle(surface, self.color, [x / 4 for x in self.player.hitbox.topleft], self.radius / 2.5,
                                   1)
            else:
                pygame.draw.circle(surface, self.color, [x / 4 for x in self.player.hitbox.topright], self.radius, 1)
                pygame.draw.circle(surface, self.color, [x / 4 for x in self.player.hitbox.topright], self.radius / 2.5,
                                   1)
