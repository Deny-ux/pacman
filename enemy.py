from constants import *
import queue
import pygame
from pygame.math import Vector2 as vec
# from game import Game
import helper_functions
import random
i = 1
class Enemy:
    def __init__(self, game, movement_mode, grid_pos, color, speed) -> None:
        self.game = game
        self.grid_pos = grid_pos
        print(self.grid_pos)
        self.pix_pos = self.get_pix_pos(self.grid_pos)
        self.color = color
        self.speed = speed
        self.target_pos = None
        self.direction = vec(0, 0)
        self.edible = False  #  if True, than player can eat enemy
        self.movement_mode = movement_mode

    def draw(self):
        pygame.draw.circle(self.game.window, self.color,
            (self.pix_pos[0]+ SQUARE_WIDTH//2,
            self.pix_pos[1]+ SQUARE_HEIGHT//2), SQUARE_WIDTH//2-2)


    def get_grid_pos(self, pix_pos):
        """
        Returns grid position in
        reference to pixel position
        """
        return [
            (pix_pos[0] - LEFT_RIGHT_PADDING)//SQUARE_WIDTH,
            (pix_pos[1] - TOP_BOTTOM_PADDING)//SQUARE_HEIGHT
        ]

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

    def update_direction(self):
        if self.edible:
            """
            According to player position set enemy position
            to run away from him
            """
            if self.game.player.grid_pos[0] >= int(COLUMNS//2) and self.game.player.grid_pos[1] >= int(ROWS//2):
                self.target_pos = RIGHT_BOTTOM_CORNER_POS
            elif self.game.player.grid_pos[0] >= int(COLUMNS//2) and self.game.player.grid_pos[1] < int(ROWS//2):
                self.target_pos = RIGTH_UP_CORNER_POS
            elif self.game.player.grid_pos[0] < int(COLUMNS//2) and self.game.player.grid_pos[1] >= int(ROWS//2):
                self.target_pos = LEFT_BOTTOM_CORNER_POS
            else:
                self.target_pos = LEFT_UP_CORNER_POS
        else:
            # if self.movement_mode == OPTIMAL_MOTION_MODE:
                # self.target_pos = self.game.player.grid_pos
            if self.movement_mode == RANDOM_MOTION_MODE:
                self.direction = self.get_available_random_direction()
        # if self.target_pos is not None and self.:
        #     next_pos = self.next_cell_position(self.grid_pos, self.target_pos, self.game.wall_map)
        #     self.direction = self.get_next_direction(next_pos)


    def get_next_direction(self, next_pos):
        next_direction = vec(
            next_pos[0] - self.grid_pos[0],
            next_pos[1] - self.grid_pos[1]
        )
        return next_direction

    def is_on_center_of_cell(self):
        """
        If the enemy is on center of cell return True
        else False
        """
        if int(self.pix_pos[0] - LEFT_RIGHT_PADDING) % SQUARE_WIDTH == 0 and \
            int(self.pix_pos[1]- TOP_BOTTOM_PADDING) % SQUARE_HEIGHT == 0:
            return True
        return False

    def next_cell_position(self, current_grid_pos, target_grid_pos, map):
        """
        function returns the value of the next cell
        where the enemy must go to get to the target
        as quickly as possible
        """
        shortest_path = self.breadth_first_search(current_grid_pos, target_grid_pos, map)
        return shortest_path[1]

    def get_available_random_direction(self):
        """
        Returns a direction where enemy can go
        considering walls around this enemy
        """
        next_position_list = [
            [int(self.grid_pos[0]+1), int(self.grid_pos[1])],
            [int(self.grid_pos[0]-1), int(self.grid_pos[1])],
            [int(self.grid_pos[0]), int(self.grid_pos[1])-1],
            [int(self.grid_pos[0]), int(self.grid_pos[1])+1]
        ]
        # next_right_cell = [int(self.grid_pos[0]+1), int(self.grid_pos[1])]
        # next_left_cell = [int(self.grid_pos[0]-1), int(self.grid_pos[1])]
        # next_top_cell = [int(self.grid_pos[0]), int(self.grid_pos[1])-1]
        # next_bottom_cell = [int(self.grid_pos[0]), int(self.grid_pos[1])+1]
        available_pos_list = []
        for pos in next_position_list:
            if pos not in self.game.walls:
                available_pos_list.append(pos)
        # if next_right_cell not in self.game.walls:
        #     next_position_list.append(next_right_cell)

        # if  next_bottom_cell not in self.game.walls:
        #     next_position_list.append(next_bottom_cell)

        # if next_left_cell not in self.game.walls:
        #     next_position_list.append(next_left_cell)

        # if next_top_cell not in self.game.walls:
        #     next_position_list.append(next_top_cell)

        next_cell = random.choice(available_pos_list)
        direction = vec(
            next_cell[0] - self.grid_pos[0],
            next_cell[1] - self.grid_pos[1]
        )
        return direction


    def update(self):
        self.draw()
        if self.is_on_center_of_cell():
            self.update_direction()
        self.move()
        #     if self.edible or self.movement_mode == OPTIMAL_MOTION_MODE:
        #         self.update_target_pos()
        #     # elif self.movement_mode == RANDOM_MOTION_MODE:
        #         # self.set_random_direction()

        # if self.movement_mode != RANDOM_MOTION_MODE:
        #     pass
        # else:
            # self.update_target_pos()

            # self.move()

    def move(self):  # ADD SPEED
        self.pix_pos[0] += self.direction.x
        self.pix_pos[1] += self.direction.y
        self.grid_pos = self.get_grid_pos(self.pix_pos)

    # def update_direction(self):
    #     """
    #     if the next """

    #     # else:  # target is position of corner



    def breadth_first_search(self, start_grid_pos, target_grid_pos, map):
        """
        This function returns list
        of the shortest path between start_grid_pos
        and target_grid_pos considering walls positions in map
        """
        print(start_grid_pos)
        print(target_grid_pos)
        queue_path = queue.Queue()
        queue_path.put(start_grid_pos)
        path = []
        visited = []
        while queue_path:
            current = queue_path.get()
            visited.append(current)
            if current == target_grid_pos:
                break
            else:
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0]+current[0] >= 0 and \
                        neighbour[0] + current[0] < len(map[0]) and\
                        neighbour[1]+current[1] >= 0 and \
                            neighbour[1] + current[1] < len(map):
                        next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                        if next_cell not in visited and map[next_cell[1]][next_cell[0]] != "W":
                            queue_path.put(next_cell)
                            path.append({"Current": current, "Next": next_cell})
        shortest_path = [target_grid_pos]
        while target_grid_pos != start_grid_pos:
            for step in path:
                if step["Next"] == target_grid_pos:
                    target_grid_pos = step["Current"]
                    shortest_path.insert(0, step["Current"])
        return shortest_path

    def reset(self):
        pass