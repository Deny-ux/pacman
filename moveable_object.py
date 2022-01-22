import copy
import pygame
from pygame.math import Vector2 as vec
from constants import *


class MoveAbleObject:
    """
    This class represent objects that can
    move, i.e. enemies, player
    """
    def __init__(self, game, start_grid_pos, current_grid_pos, speed) -> None:
        self.game = game
        self.grid_pos = current_grid_pos
        self.pix_pos = self.get_pix_pos(self.grid_pos)  # left top corner coordinates of object
        self.start_grid_pos = copy.deepcopy(start_grid_pos)
        self.start_pix_pos = self.get_pix_pos(self.start_grid_pos)
        self.direction = vec(0, 0)
        self.speed = speed

    def get_pix_pos(self, grid_pos):
        """
        Returns the left top corner
        coordinate of object
        in reference to
        grid position
        """
        return [
            (grid_pos[0]* SQUARE_WIDTH) + LEFT_RIGHT_PADDING,
            (grid_pos[1]* SQUARE_HEIGHT) + TOP_BOTTOM_PADDING
        ]

    def draw(self):
        pygame.draw.circle(self.game.window, self.color,
        (int(self.pix_pos[0] + SQUARE_WIDTH//2),
         int(self.pix_pos[1]) + SQUARE_HEIGHT//2), SQUARE_WIDTH//2-2)

    def get_grid_pos(self, pix_pos):
        """
        Returns grid position in
        reference to pixel position
        """
        return [
            (pix_pos[0] - LEFT_RIGHT_PADDING)//SQUARE_WIDTH,
            (pix_pos[1] - TOP_BOTTOM_PADDING)//SQUARE_HEIGHT
        ]

    def reset_position_and_direction(self):
        """
        This function created to
        reset object position to initial
        after player hits enemy
        """
        self.grid_pos = copy.deepcopy(self.start_grid_pos)
        self.pix_pos = copy.deepcopy(self.start_pix_pos)
        self.direction = vec(0, 0)

    def move(self):
        self.pix_pos[0] += int(self.direction.x*self.speed)
        self.pix_pos[1] += int(self.direction.y*self.speed)
        self.grid_pos = self.get_grid_pos(self.pix_pos)