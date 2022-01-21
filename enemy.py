from constants import *
import queue
import pygame
from pygame.math import Vector2 as vec
# from game import Game
import helper_functions
import copy
import random
i = 1
class Enemy:
    def __init__(self, game, movement_mode, grid_pos, color, speed) -> None:
        self.game = game
        self.grid_pos = grid_pos
        # print(self.grid_pos)
        self.pix_pos = self.get_pix_pos(self.grid_pos)
        self.color = color
        self.speed = speed
        self.start_grid_pos = copy.deepcopy(grid_pos)
        self.start_pix_pos = self.get_pix_pos(self.start_grid_pos)
        self.target_pos = None
        self.direction = vec(0, 0)
        self.edible = False  #  if True, than player can eat enemy
        self.movement_mode = movement_mode
        self.count_moves_in_direction = 0  # variable to choose how


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

    def reset_position_and_direction(self):
        """
        This function created to
        reset enemy position to initial
        after player hit enemy
        """
        self.grid_pos = copy.deepcopy(self.start_grid_pos)
        self.pix_pos = copy.deepcopy(self.start_pix_pos)
        self.direction = vec(0, 0)
        self.count_moves_in_direction = 0
        pass


    def update_direction(self):
        global i
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
            if self.movement_mode == OPTIMAL_MOTION_MODE:
                self.target_pos = self.game.player.grid_pos
                next_pos = self.next_cell_position(self.grid_pos, self.game.player.grid_pos, self.game.wall_map)

                self.direction = self.get_next_direction(next_pos)
            if self.movement_mode == RANDOM_MOTION_MODE:
                self.count_moves_in_direction -= 1
                if self.count_moves_in_direction <= 0:
                    self.direction = self.get_available_random_direction()


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

    # def next_cell_position(self, current_grid_pos, target_grid_pos, map):
    #     """
    #     function returns the value of the next cell
    #     where the enemy must go to get to the target
    #     as quickly as possible
    #     """
    #     shortest_path = self.breadth_first_search(current_grid_pos, target_grid_pos, map)
    #     return shortest_path[1]

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

        available_pos_list = []
        for pos in next_position_list:
            if pos not in self.game.walls:
                available_pos_list.append(pos)



        next_cell = random.choice(available_pos_list)

        direction = vec(
            next_cell[0] - self.grid_pos[0],
            next_cell[1] - self.grid_pos[1]
        )
        max_count_moves_in_direction = 0
        while next_cell not in self.game.walls:
            next_cell[0] += direction.x
            next_cell[1] += direction.y
            max_count_moves_in_direction += 1
        self.count_moves_in_direction = random.randint(1, max_count_moves_in_direction)
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
        self.pix_pos[0] += int(self.direction.x*self.speed)
        self.pix_pos[1] += int(self.direction.y*self.speed)
        self.grid_pos = self.get_grid_pos(self.pix_pos)


    def next_cell_position(self, current_grid_pos, target_grid_pos, map):
        """
        function returns the value of the next cell
        where the enemy must go to get to the target
        as quickly as possible
        """
        if target_grid_pos != current_grid_pos:
            shortest_path = self.breadth_first_search(current_grid_pos, target_grid_pos, map)
            return shortest_path[1]
        return target_grid_pos

    # def get_next_direction(next_pos):
    #     next_direction = vec(
    #         next_pos[0] - grid_pos[0],
    #         next_pos[1] - grid_pos[1]
    #     )
    #     return next_direction



    def breadth_first_search(self, start_grid_pos, target_grid_pos, map):
        """
        This function returns list
        of the shortest path between start_grid_pos
        and target_grid_pos considering walls positions in map
        """

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
                    # if neighbour[0]+current[0] >= 0 and \
                    #     neighbour[0] + current[0] < len(map[0]) and\
                    #     neighbour[1]+current[1] >= 0 and \
                    #         neighbour[1] + current[1] < len(map):
                    if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(map[0]) and \
                        neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(map):
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