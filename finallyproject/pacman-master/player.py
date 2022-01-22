
from constants import *
import pygame
from pygame.math import Vector2 as vec
from moveable_object import MoveAbleObject


class Player(MoveAbleObject):
    def __init__(self, game, start_grid_pos, current_grid_pos, saved_score, saved_lives, speed=PLAYER_SPEED) -> None:
        super().__init__(game, start_grid_pos, current_grid_pos, speed)
        self.color = YELLOW
        self.stored_direction = vec(0, 0)
        self.score = saved_score
        self.lives = saved_lives
        self.speed = PLAYER_SPEED
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

    def is_collision_with_enemy(self, enemy_pix_pos):
        distance = (((self.pix_pos[0] - enemy_pix_pos[0])**2) + ((self.pix_pos[1] - enemy_pix_pos[1])**2))**(0.5)
        if distance < SQUARE_WIDTH:
            return True
        return False

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

    def remove_live(self):
        self.lives -= 1

    def update(self):
        if self.can_change_direction():
            self.change_direction()
        if self.can_move():
            self.move()
        if self.in_energizer():
            self.drink_energizer()
        enemies_collisioned = [enemy for enemy in self.game.enemies if self.is_collision_with_enemy(enemy.pix_pos)]
        if len(enemies_collisioned) != 0:
            if enemies_collisioned[0].edible:
                for enemy in enemies_collisioned:
                    enemy.reset_position_and_direction()
            else:
                self.reset_position_and_direction()
                self.game.reset_enemies()
                self.remove_live()
                if self.lives == 0:
                    self.game.playing = False
                    self.game.current_menu = self.game.game_over_menu
        enemies_collisioned.clear()
        if self.on_coin():
            self.eat_coin()

    def reset_position_and_direction(self):
        super().reset_position_and_direction()
        self.stored_direction = vec(0, 0)

    def in_energizer(self):
        for energizer in self.game.energizers:
            if energizer.grid_pos == self.grid_pos:
                return True
        return False

    def drink_energizer(self):
        for energizer in self.game.energizers:
            if energizer.grid_pos == self.grid_pos:
                self.game.energizers.remove(energizer)
                self.game.time_to_eat_enemies = 10

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
        super().draw()
        self.draw_lives(self.game.window)

    def draw_lives(self, window):
        for x in range(self.lives):
            self.game.window.blit(self.heart_image,
            (20+x*HEART_IMAGE_WIDTH, DISPLAY_HEIGHT-40))

    def reset(self):
        self.score = 0
        self.direction = vec(0, 0)
        self.stored_direction = vec(0, 0)
        self.lives = COUNT_PLAYER_START_LIVES
        self.grid_pos = self.start_grid_pos
        self.pix_pos = self.start_grid_pos

