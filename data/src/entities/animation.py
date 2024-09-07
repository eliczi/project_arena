import pygame
import os


def load_animation_sprites(path, size=(64, 64)):
    """
    Loads animation sprites from the specified path.

    Args:
        path (str): The path to the directory containing the animation sprites.
        size (tuple, optional): The desired size of the animation sprites. Defaults to (64, 64).

    Returns:
        dict: A dictionary containing the loaded animation sprites, categorized by animation state.
              The keys of the dictionary are the animation states, and the values are lists of pygame.Surface objects.
    """
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


    def update_animation_frame(self, value=0.06 , reset_frame=4):
        """
        Updates the animation frame based on the given value and resets it when it reaches the reset frame.

        Args:
            value (float, optional): The value by which to increment the animation frame. Defaults to 1.5 / 25.
            reset_frame (int, optional): The frame at which the animation frame should be reset to 0. Defaults to 4.
        """
        self.animation_frame += value
        if self.animation_frame >= reset_frame:
            self.animation_frame = 0

    def state_animation(self, state):
        """
        Updates the animation frame and sets the image of the entity based on the animation state.

        Args:
            - state (str): The animation state.

        Returns:
            - None
        """
        self.update_animation_frame(self.game.time.dtf() * 7)
        if self.animation_direction == 'right':
            self.entity.image = self.animation_database[state][int(self.animation_frame)]
        elif self.animation_direction == 'left':
            self.entity.image = self.animation_database[state][int(self.animation_frame)]
            # Flip the image horizontally
            self.entity.image = pygame.transform.flip(self.entity.image, 1, 0)

    def rolling_animation(self):
        """
        Perform a rolling animation for the entity.

        This method updates the animation frame based on the time passed and sets the entity's image accordingly.
        If the animation direction is 'right', the image is retrieved from the 'ROLL' animation database.
        If the animation direction is 'left', the image is retrieved from the 'ROLL' animation database and flipped horizontally.

        Parameters:
        - self: The Animation object.

        Returns:
        - None
        """
        self.update_animation_frame(self.game.time.dtf() * 10.5, reset_frame=4)
        if self.animation_direction == 'right':
            self.entity.image = self.animation_database['ROLL'][int(self.animation_frame)]
        elif self.animation_direction == 'left':
            self.entity.image = self.animation_database['ROLL'][int(self.animation_frame)]
            self.entity.image = pygame.transform.flip(self.entity.image, 1, 0)

    def update(self):
        """
        Update the animation based on the entity's current state.

        If the entity is rolling, play the rolling animation.
        If the entity is moving, play the walking animation.
        Otherwise, play the idle animation.
        """
        if self.entity.roll and self.entity.roll.roll:
            self.rolling_animation()
        elif self.entity.moving():
            self.state_animation('WALK')
        else:
            self.state_animation('IDLE')
