import pygame
import os


def load_animation_sprites(path, size=(64, 64)):
    animation_data = {"IDLE": [], "WALK": [], "RUN": [], 'HURT': [], 'DEAD': [], 'ATTACK': [], 'ROLL': []}
    animation_states = os.listdir(path)  # Lists all the subdirectories in specified path
    for state in animation_states:
        sub_states = os.listdir(path + state)
        for sub_state in sub_states:
            key = state.upper()  # key to dictionary
            animation_image = pygame.image.load(path + state + '/' + sub_state).convert_alpha()
            animation_image = pygame.transform.scale(animation_image, size)
            animation_data[key].append(animation_image)
    return animation_data


class EntityAnimation:
    def __init__(self, entity, game, death_anim=4, speed=25):
        self.entity = entity
        self.game = game
        self.animation_direction = 'right'
        self.animation_frame = 0
        self.hurt_timer = 0
        self.death_animation_frames = death_anim
        self.speed = speed
        self.animation_database = load_animation_sprites(self.entity.path)

    def get_direction(self):
        if self.entity.velocity[0] > 0:
            self.animation_direction = 'right'
        elif self.entity.velocity[0] < 0:
            self.animation_direction = 'left'

    def update_animation_frame(self, value=1.5 / 25, reset_frame=4):
        self.animation_frame += value
        if self.animation_frame >= reset_frame:
            self.animation_frame = 0

    def idle_animation(self, state):
        self.update_animation_frame(self.game.time.dtf() * 7)
        self.get_direction()
        if self.animation_direction == 'right':
            self.entity.image = self.animation_database[state][int(self.animation_frame)]
        elif self.animation_direction == 'left':
            self.entity.image = self.animation_database[state][int(self.animation_frame)]
            self.entity.image = pygame.transform.flip(self.entity.image, 1, 0)

    def rolling_animation(self):
        self.update_animation_frame(self.game.time.dtf() * 10.5, reset_frame=4)
        if self.animation_direction == 'right':
            self.entity.image = self.animation_database['ROLL'][int(self.animation_frame)]
        elif self.animation_direction == 'left':
            self.entity.image = self.animation_database['ROLL'][int(self.animation_frame)]
            self.entity.image = pygame.transform.flip(self.entity.image, 1, 0)

    def update(self):
        if self.entity.roll and self.entity.roll.roll:
            self.rolling_animation()
        elif self.entity.moving():
            self.idle_animation('WALK')
        else:
            self.idle_animation('IDLE')
