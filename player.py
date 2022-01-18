from constants import *
import pygame
from pygame.math import Vector2 as vec

j = 1

class Player:
    def __init__(self, game, start_grid_pos) -> None:
        self.game = game
        self.grid_pos = start_grid_pos  # list of two elements
        self.pix_pos = self.get_pix_pos(self.grid_pos)  # left top corner coordinates
        self.direction = vec(0, 0)
        self.stored_direction = vec(0, 0)
        self.score = 0
        self.lives = COUNT_PLAYER_START_LIVES
        heart_image = pygame.image.load(HEART_IMAGE_PATH)
        self.heart_image = pygame.transform.scale(heart_image ,(HEART_IMAGE_WIDTH, HEART_IMAGE_HEIGHT))


    def change_direction(self):
        self.direction = self.stored_direction

    def can_move(self):
        if (self.pix_pos[0] - LEFT_RIGHT_PADDING) % SQUARE_WIDTH == 0 and \
            (self.pix_pos[1] - TOP_BOTTOM_PADDING) % SQUARE_HEIGHT == 0:
            next_grid_pos = [
                self.grid_pos[0] + self.direction.x,
                self.grid_pos[1] + self.direction.y
            ]
            for wall in self.game.walls:
                if next_grid_pos == wall:
                    return False
        return True


    def can_change_direction(self):
        if self.stored_direction != vec(0, 0) and self.direction != self.stored_direction:
            if int(self.pix_pos[0] - LEFT_RIGHT_PADDING) % SQUARE_WIDTH == 0 and \
                int(self.pix_pos[1] - TOP_BOTTOM_PADDING) % SQUARE_HEIGHT == 0:
                next_grid_pos = [
                    self.grid_pos[0] + self.stored_direction.x,
                    self.grid_pos[1] + self.stored_direction.y]
                for wall in self.game.walls:
                    if next_grid_pos == wall:
                        return False
                return True
            return False
        return False

    def move(self):
        self.pix_pos[0] += int(self.direction.x*PLAYER_SPEED)
        self.pix_pos[1] += int(self.direction.y*PLAYER_SPEED)
        self.grid_pos = self.get_grid_pos(self.pix_pos)

    def update(self):
        # if self.stored_direction is not None:
        #     if self.can_move():
        #         self.change_direction()

        # self.move()
        if self.can_change_direction():
            self.change_direction()
        if self.can_move():
            self.move()
        if self.on_coin():
            self.eat_coin()

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

    def get_grid_pos(self, pix_pos):
        """
        Returns grid position in
        reference to pixel position
        """
        return [
            (pix_pos[0] - LEFT_RIGHT_PADDING)//SQUARE_WIDTH,
            (pix_pos[1] - TOP_BOTTOM_PADDING)//SQUARE_HEIGHT
        ]

    def on_coin(self):
        """
        Returns True if player is
        on coin
        else returns false
        """
        if self.grid_pos in self.game.coins:
            if self.pix_pos == self.get_pix_pos(self.grid_pos):
                return True
        return False

    def eat_coin(self):
        self.game.coins.remove(self.grid_pos)
        self.score += 1

    def draw(self):
        self.draw_lives(self.game.window)
        pygame.draw.circle(self.game.window, YELLOW,
        (int(self.pix_pos[0] + SQUARE_WIDTH//2), int(self.pix_pos[1]) + SQUARE_HEIGHT//2), SQUARE_WIDTH//2-2)

    def draw_lives(self, window):
        for x in range(self.lives):
            self.game.window.blit(self.heart_image,
            (20+x*HEART_IMAGE_WIDTH, DISPLAY_HEIGHT-40))


    def reset(self):
        self.score = 0
        self.direction = vec(0, 0)
        self.stored_direction = vec(0, 0)
        self.lives = COUNT_PLAYER_START_LIVES


# print( int(pl.pix_pos[0] - LEFT_RIGHT_PADDING ) % SQUARE_WIDTH)
# if int(pl.pix_pos[0] - LEFT_RIGHT_PADDING - SQUARE_WIDTH//2) % SQUARE_WIDTH == 0:
#     print(1)

# print(pl.grid_pos)
# print(pl.pix_pos)
# print(pl.get_grid_pos([60, 60]))
# print(pl.get_grid_pos([70, 50]))
