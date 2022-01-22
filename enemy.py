from constants import *
import queue
from pygame.math import Vector2 as vec
import copy
import random
from moveable_object import MoveAbleObject


class E:
    def __init__(self) -> None:
        pass

    def t(self, a):
        return 1

class Enemy(MoveAbleObject):
    def __init__(self, game, movement_mode, current_grid_pos, start_grid_pos, color, speed) -> None:
        super().__init__(game, start_grid_pos, current_grid_pos, speed)
        self.initial_color = color
        self.color = copy.deepcopy(color)
        self.direction = vec(0, 0)
        self.target_pos = None
        self.edible = False  # if True, than player can eat enemy
        self.initial_movement_mode = movement_mode
        self.movement_mode = copy.deepcopy(self.initial_movement_mode)
        self.count_moves_in_direction = 0  # variable for random movement logic


    def reset_position_and_direction(self):
        super().reset_position_and_direction()
        self.count_moves_in_direction = 0

    def update_direction(self):
        """
        if player used energizer, than enemy
        moves randomly. Else enemy moves
        according to its initial movement mode
        """
        if self.edible:
            self.movement_mode = RANDOM_MOTION_MODE
            self.color = WHITE
        else:
            self.movement_mode = self.initial_movement_mode
            self.color = self.initial_color
        if self.movement_mode == RANDOM_MOTION_MODE:
            self.count_moves_in_direction -= 1
            if self.count_moves_in_direction <= 0:
                self.direction = self.get_available_random_direction()
        elif self.movement_mode == OPTIMAL_MOTION_MODE:
            self.count_moves_in_direction = 0
            self.target_pos = self.game.player.grid_pos
            next_pos = self.next_cell_position(self.grid_pos, self.target_pos, self.game.wall_map)
            self.direction = self.get_next_direction(next_pos)

    def get_next_direction(self, next_pos):
        """
        Returns direction of enemy movement
        according to its current position
        and next position
        """
        next_direction = vec(
            next_pos[0] - self.grid_pos[0],
            next_pos[1] - self.grid_pos[1]
        )
        return next_direction

    def is_on_center_of_cell(self):
        """
        If the enemy is on center of cell in grid return True
        else False
        """
        if int(self.pix_pos[0] - LEFT_RIGHT_PADDING) % SQUARE_WIDTH == 0 and \
           int(self.pix_pos[1] - TOP_BOTTOM_PADDING) % SQUARE_HEIGHT == 0:
            return True
        return False

    def get_available_random_direction(self):
        """
        Returns a random direction where enemy can go
        considering walls around it and how many steps
        in this direction enemy can go
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
        if self.game.time_to_eat_enemies > 0:
            self.edible = True
            self.color = WHITE
        elif self.game.time_to_eat_enemies <= 0:
            self.edible = False
            self.color = self.initial_color
        self.move()

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

    def breadth_first_search(self, start_grid_pos, target_grid_pos, map):
        """
        This function returns list
        of the shortest path between start_grid_pos
        and target_grid_pos considering walls positions in map
        using breadth first search algorithm
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
