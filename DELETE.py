from tkinter.tix import ROW
from constants import *
from helper_functions import *
import queue
# grid = [
#     ["1", "1", "1", "1", "1", "1", "1", "1"],
#     ["1", "2", "2", "0", "1", "0", "0", "1"],
#     ["1", "0", "1", "1", "1", "0", "0", "1"],
#     ["1", "0", "1", "0", "0", "0", "0", "1"],
#     ["1", "0", "1", "1", "0", "1", "0", "1"],
#     ["1", "0", "1", "1", "0", "0", "0", "1"],
#     ["1", "0", "0", "0", "0", "0", "0", "1"],
#     ["1", "0", "1", "0", "0", "0", "0", "1"],
#     ["1", "1", "1", "1", "1", "1", "1", "1"]
# ]
grid = [
    ["0", "0", "1", "1"],
    ["0", "0", "0", "0"],
    ["0", "1", "1", "0"],
    ["0", "0", "0", "0"],
]
# grid = [
#     ["1", "1", "1", "1", "1", "1", "1", "1"],
#     ["1", "2", "0", "0", "1", "0", "0", "1"],
#     ["1", "2", "1", "1", "1", "2", "0", "1"],
#     ["1", "2", "1", "0", "2", "2", "0", "1"],
#     ["1", "2", "1", "1", "2", "1", "0", "1"],
#     ["1", "2", "1", "1", "2", "0", "0", "1"],
#     ["1", "2", "2", "2", "2", "0", "0", "1"],
#     ["1", "0", "1", "0", "0", "0", "0", "1"],
#     ["1", "1", "1", "1", "1", "1", "1", "1"]
# ]

# def BFS(start, target):
#     # grid = [[0 for x in range(28)] for x in range(30)]
#     # for cell in self.app.walls:
#     #     if cell.x < 28 and cell.y < 30:
#     #         grid[int(cell.y)][int(cell.x)] = 1
#     global grid
#     queue = [start]
#     path = []
#     visited = []
#     while queue:
#         current = queue[0]
#         queue.remove(queue[0])
#         visited.append(current)
#         if current == target:
#             break
#         else:
#             neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
#             for neighbour in neighbours:
#                 if neighbour[0]+current[0] >= 0 and neighbour[0] + current[0] < len(grid[0]):
#                     if neighbour[1]+current[1] >= 0 and neighbour[1] + current[1] < len(grid):
#                         next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
#                         if next_cell not in visited:
#                             if grid[next_cell[1]][next_cell[0]] != "1":
#                                 queue.append(next_cell)
#                                 path.append({"Current": current, "Next": next_cell})
#     shortest = [target]
#     while target != start:
#         for step in path:
#             if step["Next"] == target:
#                 target = step["Current"]
#                 shortest.insert(0, step["Current"])
#     return shortest

def breadth_first_search(start_grid_pos, target_grid_pos, walls_list_pos):
    """
    This function returns list
    of the shortest path between start_grid_pos
    and target_grid_pos considering walls positions
    """
    grid = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
    for wall_pos in walls_list_pos:
        x, y = wall_pos[0], wall_pos[1]
        grid[y][x] = "W"
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
                    neighbour[0] + current[0] < len(grid[0]) and\
                       neighbour[1]+current[1] >= 0 and \
                           neighbour[1] + current[1] < len(grid):
                    next_cell = [neighbour[0] + current[0], neighbour[1] + current[1]]
                    if next_cell not in visited and grid[next_cell[1]][next_cell[0]] != "W":
                        queue_path.put(next_cell)
                        path.append({"Current": current, "Next": next_cell})
    shortest_path = [target_grid_pos]
    while target_grid_pos != start_grid_pos:
        for step in path:
            if step["Next"] == target_grid_pos:
                target_grid_pos = step["Current"]
                shortest_path.insert(0, step["Current"])
    return shortest_path

dir = load_level_data_from_json("lvl1.json")
walls = dir["walls"]
# map = [["0" for x in range(COLUMNS)] for y in range(ROWS)]

d = breadth_first_search([1,2], [10, 4], walls)
print(d)
# [[1, 0], [1, 1], [2, 1], [3, 1], [3, 2], [3, 3], [2, 3]]
pass