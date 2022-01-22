import pygame
from constants import *

class Energizer:
    def __init__(self, game, grid_pos, color, secunds_duration) -> None:
        self.game = game
        self.color = color
        self.grid_pos = grid_pos
        self.pix_pos = self.get_pix_pos(self.grid_pos)
        self.secunds_duration = secunds_duration


    def draw(self):
        x, y = self.pix_pos[0], self.pix_pos[1]
        pygame.draw.circle(
            self.game.window, self.color,
            (x + SQUARE_WIDTH//2, y + SQUARE_HEIGHT//2),
            SQUARE_WIDTH//2-4)


    def get_pix_pos(self, grid_pos):
        """
        Returns the left top corner
        in reference to
        grid position
        """
        return [
            (grid_pos[0]* SQUARE_WIDTH) + LEFT_RIGHT_PADDING,
            (grid_pos[1]* SQUARE_HEIGHT) + TOP_BOTTOM_PADDING
        ]