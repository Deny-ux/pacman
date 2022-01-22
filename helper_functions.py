from enum import Enum
import queue
from constants import *
# from constants import(
#     COLUMNS,
#     NEW_MAP_FILE_NAME,
#     ROWS,
#     SCORE_FILE_NAME,
#     MAX_LEN_NAME
# )
import json
import csv


class MalformedScoreDataError(Exception):
    pass


class ScoreFileNotFoundError(FileNotFoundError):
    pass


class ScoreFilePermissionError(PermissionError):
    pass


class MalformedNewMapData(Exception):
    pass


class ScoreFileIsDirectoryError(IsADirectoryError):
    pass

class NewMapFileNotFoundError(FileNotFoundError):
    pass


class NewMapFilePermissionError(PermissionError):
    pass


class NewMapFileIsDirectoryError(IsADirectoryError):
    pass


def take_second(elem):
        return elem[1]



# def update_score_list(score_list, name, score):
#     """
#     Change list only if
#     score > min(score_list[1])
#     """



def get_dict_elements_from_map(file_name):
    try:
        with open(file_name, 'r') as handle:
            walls_list = []
            coins_list = []
            enemies_list = []
            player_grid_pos = None
            energizers = []
            for yidx, line in enumerate(handle):
                for xidx, char in enumerate(line):
                    if char == "W":
                        walls_list.append([xidx, yidx])
                    elif char == "C":
                        coins_list.append([xidx, yidx])
                    elif char == "P":
                        player_grid_pos = [xidx, yidx]
                    elif char in ["1", "2", "3", "4"]:
                        enemies_list.append([xidx, yidx])
                    elif char == "S":
                        energizers.append([xidx, yidx])
            dict_el = dict()
            dict_el["walls"] = walls_list
            dict_el["coins"] = coins_list
            dict_el["enemies"] = enemies_list
            dict_el["player_grid_pos"] = player_grid_pos
            dict_el["energizers"] = energizers
            return dict_el
                    # elif char == "B":
                    #     pygame.draw.rect(self.background, BLACK, (xidx*self.cell_width, yidx*self.cell_height,
                    #                                               self.cell_width, self.cell_height))

    except FileNotFoundError:
        raise NewMapFileNotFoundError("Can not find file with new map!")
    except IsADirectoryError:
        raise NewMapFileIsDirectoryError("Can only work with files")
    except PermissionError:
        raise NewMapFilePermissionError(
            "You don't have permission to open file with new map!")


def load_level_data_from_json(filename):
    """
    This function returns dictionary
    with elements in json file
    """
    try:

        with open(filename, 'r') as handle:
            data_dict = json.load(handle)
            """
            Check if all elements
            are present in file
            """
            if all(key in data_dict for key in (
                "walls_pos_list",
                "coins_pos_list",
                "enemies",
                "player",
                "energizers",
                "remaining_time_energizer")):
                player = data_dict["player"]
                energizers = data_dict["energizers"]
                for enemy in data_dict["enemies"]:
                    if all(key in enemy for key in(
                        "current_grid_pos",
                        "start_grid_pos",
                        "color",
                        "movement_mode",
                        "speed"
                    )) and \
                        all(key in player for key in(
                            "current_grid_pos",
                            "start_grid_pos",
                            "lives",
                            "score",
                            "score"
                        )) and \
                            all(key in energizers for key in (
                                "grid_pos",
                                "color",
                                "secunds_duration"
                            )):
                        return data_dict
            raise MalformedNewMapData("Missing some keys in file!")

    except FileNotFoundError:
        raise NewMapFileNotFoundError("Can not find file with new map!")
    except IsADirectoryError:
        raise NewMapFileIsDirectoryError("Can only work with files")
    except PermissionError:
        raise NewMapFilePermissionError(
            "You don't have permission to open file with new map!")

d = load_level_data_from_json("lvl1.json")
pass
# def sort_high_scores_list(score_list):
a= 1

def load_high_score_data_from_file(file_name):
    try:
        with open(file_name) as handle:
            people = []
            reader = csv.DictReader(handle)
            try:
                for row in reader:
                    name = row["name"]
                    score = int(row["score"])
                    people.append((name, score))
                    # print(name, str(score))
            except csv.Error:
                raise MalformedScoreDataError(
                    "Score data file has invalid data")
    except FileNotFoundError:
        raise ScoreFileNotFoundError("Can not find file with high scores!")
    except IsADirectoryError:
        raise ScoreFileIsDirectoryError("Can only work with files")
    except PermissionError:
        raise ScoreFilePermissionError(
            "You don't have permission to open high score file!")
    people.sort(key=take_second, reverse=True)
    return people


def write_high_score_data_to_file(score_list, file_name):
    try:
        with open(file_name, "w") as handle:
            handle.write("name,score\n")
            for score_item in score_list:
                handle.write(f"{score_item[0]},{str(score_item[1])}\n")

    except FileNotFoundError:
        raise ScoreFileNotFoundError("Can not find file with high scores!")
    except IsADirectoryError:
        raise ScoreFileIsDirectoryError("Can only work with files")
    except PermissionError:
        raise ScoreFilePermissionError(
            "You don't have permission to open high score file!")


def get_updated_high_score_list(new_score_item, file_name):
    """
    If new_score is greater than
    minimum value of high score or length of
    list of hish score is less than 10
    than it will be placed in the file
    with high scores
    """
    new_name, new_score = new_score_item[0], new_score_item[1]
    people = load_high_score_data_from_file(SCORE_FILE_NAME)
    people.sort(key=take_second, reverse=True)
    if len(people) < 10:
        people.append(new_score_item)
    elif people[len(people)-1][1] < new_score:
        people.pop(len(people)-1)
        people.append(new_score_item)
        people.sort(key=take_second, reverse=True)
            # if to_update:
                # with open(file_name, "w") as handle:

    return people

def get_walls_list_pos(list_walls_pos):
        """
        Create a list which represent a map
        of walls
        """
        map = [["0" for x in range(COLUMNS)] for y in range(ROWS)]
        for wall_pos in list_walls_pos:
            x, y = wall_pos[0], wall_pos[1]
            map[y][x] = "W"
        return map

# ############################################

# dir = load_level_data_from_json("lvl1.json")
# walls = dir["walls"]
# map = [["0" for x in range(COLUMNS)] for y in range(ROWS)]
# for wall_pos in walls:
#     x, y = wall_pos[0], wall_pos[1]
#     map[y][x] = "1"


# for line in map:
#     print(line)
# print(f"{map[1][2]} ,{map[2][1]}")




# q = queue.Queue("0")
# for i in range(1):
#     print(i)
#     x = q.get()
#     if x is not None:
#         y = x + "0"
#         z = x + "1"
#     else:
#         y = "0"
#         z = "1"
#     print(y)
#     q.put(y)
#     q.put(z)

#     print(y)
#  print map
# for line in map:
#     print(line)



# print(load_high_score_data_from_file(SCORE_FILE_NAME))
# p =[('player', 9000), ('player2', 10000), ('player6', 1000), ('playeds', 92), ('player2', 12), ('player2', 10), ('player2', 10), ('player2', 10), ('player2', 10), ('player2', 10)]
# p = load_high_score_data_from_file(SCORE_FILE_NAME)
# new_score_item = ("john", 100)
# p1 = get_updated_high_score_list(new_score_item, SCORE_FILE_NAME)

# write_high_score_data_to_file(p1, SCORE_FILE_NAME)

# p2 = load_high_score_data_from_file(SCORE_FILE_NAME)
# print(p)
# """
# player,9000
# player2,9000
# player6,1000
# PLAYER8,100
# john,100
# p,1
# p,1
# p,2
# playeds,92
# player2,12
# """
# print(p1)
# print(p2)




# # d = get_dict_elements_from_map("lvl1.txt")
# # print(d["coins"])
# # print(d["energizers"])
# pass
# """
# [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [12, 0], [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0], [21, 0], [22, 0], [23, 0], [24, 0], [25, 0], [26, 0], [27, 0], [28, 0], [29, 0], [30, 0], [31, 0], [32, 0], [33, 0], [34, 0], [0, 1], [1, 1], [2, 1], [3, 1], [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [10, 1], [11, 1], [12, 1], [13, 1], [14, 1], [20, 1], [21, 1], [22, 1], [23, 1], [24, 1], [25, 1], [26, 1], [27, 1], [28, 1], [29, 1], [30, 1], [31, 1], [32, 1], [33, 1], [34, 1], [0, 2], [13, 2], [14, 2], [20, 2], [21, 2], [34, 2], [0, 3], [1, 3], [2, 3], [4, 3], [5, 3], [7, 3], [8, 3], [9, 3], [25, 3], [26, 3], [27, 3], [29, 3], [30, 3], [32, 3], [33, 3], [34, 3], [0, 4], [9, 4], [11, 4], [12, 4], [13, 4], [14, 4], [15, 4], [16, 4], [17, 4], [18, 4], [19, 4], [20, 4], [21, 4], [22, 4], [23, 4], [25, 4], [34, 4], [0, 5], [9, 5], [11, 5], [23, 5], [25, 5], [34, 5], [0, 6], [1, 6], [3, 6], [4, 6], [6, 6], [7, 6], [9, 6], [11, 6], [13, 6], [14, 6], [15, 6], [16, 6], [17, 6], [18, 6], [19, 6], [20, 6], [21, 6], [23, 6], [25, 6], [27, 6], [28, 6], [30, 6], [31, 6], [33, 6], [34, 6], [0, 7], [1, 7], [3, 7], [7, 7], [9, 7], [11, 7], [13, 7], [21, 7], [23, 7], [25, 7], [27, 7], [31, 7], [33, 7], [34, 7], [0, 8], [1, 8], [3, 8], [4, 8], [6, 8], [7, 8], [9, 8], [11, 8], [12, 8], [13, 8], [14, 8], [15, 8], [16, 8], [17, 8], [18, 8], [19, 8], [20, 8], [21, 8], [22, 8], [23, 8], [25, 8], [27, 8], [28, 8], [30, 8], [31, 8], [33, 8], [34, 8], [0, 9], [34, 9], [0, 10], [1, 10], [2, 10], [4, 10], [5, 10], [6, 10], [7, 10], [9, 10], [10, 10], [11, 10], [13, 10], [14, 10], [15, 10], [19, 10], [20, 10], [21, 10], [23, 10], [24, 10], [25, 10], [27, 10], [28, 10], [29, 10], [30, 10], [32, 10], [33, 10], [34, 10], [0, 11], [1, 11], [2, 11], [4, 11], [7, 11], [9, 11], [11, 11], [13, 11], [21, 11], [23, 11], [25, 11], [27, 11], [30, 11], [32, 11], [33, 11], [34, 11], [0, 12], [1, 12], [2, 12], [4, 12], [7, 12], [9, 12], [11, 12], [13, 12], [21, 12], [23, 12], [25, 12], [27, 12], [30, 12], [32, 12], [33, 12], [34, 12], [0, 13], [1, 13], [2, 13], [4, 13], [7, 13], [9, 13], [11, 13], [13, 13], [21, 13], [23, 13], [25, 13], [27, 13], [30, 13], [32, 13], [33, 13], [34, 13], [0, 14], [1, 14], [2, 14], [4, 14], [7, 14], [9, 14], [11, 14], [13, 14], [14, 14], [15, 14], [16, 14], [17, 14], [18, 14], [19, 14], [20, 14], [21, 14], [23, 14], [25, 14], [27, 14], [30, 14], [32, 14], [33, 14], [34, 14], [0, 15], [1, 15], [2, 15], [4, 15], [7, 15], [9, 15], [11, 15], [23, 15], [25, 15], [27, 15], [30, 15], [32, 15], [33, 15], [34, 15], [0, 16], [1, 16], [2, 16], [4, 16], [7, 16], [9, 16], [11, 16], [12, 16], [13, 16], [14, 16], [15, 16], [16, 16], [17, 16], [18, 16], [19, 16], [20, 16], [21, 16], [22, 16], [23, 16], [25, 16], [27, 16], [30, 16], [32, 16], [33, 16], [34, 16], [0, 17], [1, 17], [2, 17], [4, 17], [5, 17], [6, 17], [7, 17], [9, 17], [10, 17], [11, 17], [23, 17], [24, 17], [25, 17], [27, 17], [28, 17], [29, 17], [30, 17], [32, 17], [33, 17], [34, 17], [0, 18], [13, 18], [14, 18], [15, 18], [16, 18], [17, 18], [18, 18], [19, 18], [20, 18], [21, 18], [34, 18], [0, 19], [2, 19], [3, 19], [4, 19], [5, 19], [6, 19], [7, 19], [8, 19], [10, 19], [11, 19], [12, 19], [13, 19], [14, 19], [15, 19], [16, 19], [17, 19], [18, 19], [19, 19], [20, 19], [21, 19], [22, 19], [23, 19], [24, 19], [26, 19], [27, 19], [28, 19], [29, 19], [30, 19], [31, 19], [32, 19], [34, 19], [0, 20], [2, 20], [8, 20], [10, 20], [11, 20], [12, 20], [22, 20], [23, 20], [24, 20], [26, 20], [32, 20], [34, 20], [0, 21], [2, 21], [3, 21], [4, 21], [5, 21], [6, 21], [7, 21], [8, 21], [10, 21], [11, 21], [12, 21], [14, 21], [15, 21], [16, 21], [17, 21], [18, 21], [19, 21], [20, 21], [22, 21], [23, 21], [24, 21], [26, 21], [27, 21], [28, 21], [29, 21], [30, 21], [31, 21], [32, 21], [34, 21], [0, 22], [2, 22], [3, 22], [4, 22], [5, 22], [6, 22], [7, 22], [8, 22], [10, 22], [11, 22], [12, 22], [14, 22], [15, 22], [16, 22], [17, 22], [18, 22], [19, 22], [20, 22], [22, 22], [23, 22], [24, 22], [26, 22], [27, 22], [28, 22], [29, 22], [30, 22], [31, 22], [32, 22], [34, 22], [0, 23], [34, 23], [0, 24], [1, 24], [2, 24], [3, 24], [4, 24], [5, 24], [6, 24], [7, 24], [8, 24], [9, 24], [10, 24], [11, 24], [12, 24], [13, 24], [14, 24], [15, 24], [16, 24], [17, 24], [18, 24], [19, 24], [20, 24], [21, 24], [22, 24], [23, 24], [24, 24], [25, 24], [26, 24], [27, 24], [28, 24], [29, 24], [30, 24], [31, 24], [32, 24], [33, 24], [34, 24]]
# """
# # print(d.get("coins"))
# """
# [[15, 1], [16, 1], [17, 1], [18, 1], [19, 1], [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2], [9, 2], [10, 2], [11, 2], [12, 2], [15, 2], [16, 2], [17, 2], [18, 2], [19, 2], [22, 2], [23, 2], [24, 2], [25, 2], [26, 2], [27, 2], [28, 2], [29, 2], [30, 2], [31, 2], [32, 2], [33, 2], [3, 3], [6, 3], [10, 3], [11, 3], [12, 3], [13, 3], [14, 3], [15, 3], [16, 3], [17, 3], [18, 3], [19, 3], [20, 3], [21, 3], [22, 3], [23, 3], [24, 3], [28, 3], [31, 3], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [10, 4], [24, 4], [26, 4], [27, 4], [28, 4], [29, 4], [30, 4], [31, 4], [32, 4], [33, 4], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [10, 5], [24, 5], [26, 5], [27, 5], [28, 5], [29, 5], [30, 5], [31, 5], [32, 5], [33, 5], [2, 6], [5, 6], [8, 6], [10, 6], [24, 6], [26, 6], [29, 6], [32, 6], [2, 7], [4, 7], [5, 7], [6, 7], [8, 7], [10, 7], [24, 7], [26, 7], [28, 7], [29, 7], [30, 7], [32, 7], [2, 8], [5, 8], [8, 8], [10, 8], [24, 8], [26, 8], [29, 8], [32, 8], [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9], [14, 9], [15, 9], [16, 9], [17, 9], [18, 9], [19, 9], [20, 9], [21, 9], [22, 9], [23, 9], [24, 9], [25, 9], [26, 9], [27, 9], [28, 9], [29, 9], [30, 9], [31, 9], [32, 9], [33, 9], [2, 10], [8, 10], [12, 10], [16, 10], [17, 10], [18, 10], [22, 10], [26, 10], [32, 10], [2, 11], [8, 11], [12, 11], [22, 11], [26, 11], [32, 11], [2, 12], [8, 12], [12, 12], [22, 12], [26, 12], [32, 12], [2, 13], [8, 13], [12, 13], [22, 13], [26, 13], [32, 13], [2, 14], [8, 14], [12, 14], [22, 14], [26, 14], [32, 14], [2, 15], [8, 15], [12, 15], [13, 15], [14, 15], [15, 15], [16, 15], [17, 15], [18, 15], [19, 15], [20, 15], [21, 15], [22, 15], [26, 15], [32, 15], [2, 16], [8, 16], [26, 16], [32, 16], [2, 17], [8, 17], [12, 17], [13, 17], [14, 17], [15, 17], [16, 17], [17, 17], [18, 17], [19, 17], [20, 17], [21, 17], [22, 17], [26, 17], [32, 17], [1, 18], [2, 18], [3, 18], [4, 18], [5, 18], [6, 18], [7, 18], [8, 18], [9, 18], [10, 18], [11, 18], [12, 18], [22, 18], [23, 18], [24, 18], [25, 18], [26, 18], [27, 18], [28, 18], [29, 18], [30, 18], [31, 18], [32, 18], [33, 18], [1, 19], [9, 19], [25, 19], [33, 19], [1, 20], [9, 20], [13, 20], [14, 20], [15, 20], [16, 20], [17, 20], [18, 20], [19, 20], [20, 20], [21, 20], [25, 20], [33, 20], [1, 21], [9, 21], [13, 21], [21, 21], [25, 21], [33, 21], [1, 22], [9, 22], [13, 22], [21, 22], [25, 22], [33, 22], [1, 23], [2, 23], [3, 23], [4, 23], [5, 23], [6, 23], [7, 23], [8, 23], [9, 23], [10, 23], [11, 23], [12, 23], [13, 23], [14, 23], [15, 23], [16, 23], [18, 23], [19, 23], [20, 23], [21, 23], [22, 23], [23, 23], [24, 23], [25, 23], [26, 23], [27, 23], [28, 23], [29, 23], [30, 23], [31, 23], [32, 23], [33, 23]]
# """
# # print(d.get("enemies"))
# """
# [[14, 11], [20, 11], [14, 13], [20, 13]]
# """


# # pass
# # name = "lvl1.json"
# ar = [1,2]

# # print(ar.empty())
# dir = load_level_data_from_json("lvl1.json")
# walls = dir["walls"]
# map = [["0" for x in range(COLUMNS)] for y in range(ROWS)]
# for wall_pos in walls:
#     x, y = wall_pos[0], wall_pos[1]
#     map[y][x] = "1"
# # for line in map:
#     # print(line)

# maze = [
#     ["1", "1", "1", "1", "1", "1", "1", "1"]
#     ["1", "0", "0", "0", "1", "0", "0", "1"]
#     ["1", "2", "1", "1", "1", "0", "0", "1"]
#     ["1", "0", "1", "0", "3", "0", "0", "1"]
#     ["1", "0", "1", "1", "0", "1", "0", "1"]
#     ["1", "0", "1", "1", "0", "0", "0", "1"]
#     ["1", "0", "0", "0", "0", "0", "0", "1"]
#     ["1", "0", "1", "0", "0", "0", "0", "1"]
#     ["1", "1", "1", "1", "1", "1", "1", "1"]
# ]
# start_pos = [1, 2]
# target_pos = [4, 3]

# "LEFT", "RIGHT", "UP", "DOWN"
# def get_last_pos(start_pos, path_list):
#     """
#     Return the coordinates of
#     end of route
#     """

# # def can_move()
# def BFS(start_pos, walls, end_pos):
#     pass

map_list = [['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'], ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', '0', '0', '0', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'], ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W', 'W', '0', '0', '0', '0', '0', 'W', 'W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'], ['W', 'W', 'W', '0', 'W', 'W', '0', 'W', 'W', 'W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W', 'W', 'W', '0', 'W', 'W', '0', 'W', 'W', 'W'], ['W', '0', '0', '0', '0', '0', '0', '0', '0', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', '0', '0', '0', '0', '0', '0', '0', '0', 'W'], ['W', '0', '0', '0', '0', '0', '0', '0', '0', 'W', '0', 'W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W', '0', 'W', '0', '0', '0', '0', '0', '0', '0', '0', 'W'], ['W', 'W', '0', 'W', 'W', '0', 'W', 'W', '0', 'W', '0', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', '0', 'W', '0', 'W', 'W', '0', 'W', 'W', '0', 'W', 'W'], ['W', 'W', '0', 'W', '0', '0', '0', 'W', '0', 'W', '0', 'W', '0', 'W', '0', '0', '0', '0', '0', '0', '0', 'W', '0', 'W', '0', 'W', '0', 'W', '0', '0', '0', 'W', '0', 'W', 'W'], ['W', 'W', '0', 'W', 'W', '0', 'W', 'W', '0', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', '0', 'W', 'W', '0', 'W', 'W', '0', 'W', 'W'], ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'], ['W', 'W', 'W', '0', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W', '0', 'W', 'W', 'W', '0', '0', '0', 'W', 'W', 'W', '0', 'W', 'W', 'W', '0', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W'], ['W', 'W', 'W', '0', 'W', '0', '0', 'W', '0', 'W', '0', 'W', '0', 'W', '0', '0', '0', '0', '0', '0', '0', 'W', '0', 'W', '0', 'W', '0', 'W', '0', '0', 'W', '0', 'W', 'W', 'W'], ['W', 'W', 'W', '0', 'W', '0', '0', 'W', '0', 'W', '0', 'W', '0', 'W', '0', '0', '0', '0', '0', '0', '0', 'W', '0', 'W', '0', 'W', '0', 'W', '0', '0', 'W', '0', 'W', 'W', 'W'], ['W', 'W', 'W', '0', 'W', '0', '0', 'W', '0', 'W', '0', 'W', '0', 'W', '0', '0', '0', '0', '0', '0', '0', 'W', '0', 'W', '0', 'W', '0', 'W', '0', '0', 'W', '0', 'W', 'W', 'W'], ['W', 'W', 'W', '0', 'W', '0', '0', 'W', '0', 'W', '0', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', '0', 'W', '0', 'W', '0', '0', 'W', '0', 'W', 'W', 'W'], ['W', 'W', 'W', '0', 'W', '0', '0', 'W', '0', 'W', '0', 'W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W', '0', 'W', '0', 'W', '0', '0', 'W', '0', 'W', 'W', 'W'], ['W', 'W', 'W', '0', 'W', '0', '0', 'W', '0', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', '0', 'W', '0', '0', 'W', '0', 'W', 'W', 'W'], ['W', 'W', 'W', '0', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W', 'W', 'W', '0', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W'], ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'], ['W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W'], ['W', '0', 'W', '0', '0', '0', '0', '0', 'W', '0', 'W', 'W', 'W', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W', 'W', 'W', '0', 'W', '0', '0', '0', '0', '0', 'W', '0', 'W'], ['W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W'], ['W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W', 'W', 'W', '0', 'W', 'W', 'W', 'W', 'W', 'W', 'W', '0', 'W'], ['W', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'W'], ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]
from pygame.math import Vector2 as vec
import queue

grid_pos = [20, 11]
# [14, 11]
# [14, 12] +-
#[14, 15]
target_pos = [17, 23]
# if self.movement_mode == OPTIMAL_MOTION_MODE:
#     self.target_pos = self.game.player.grid_pos
#     next_pos = self.next_cell_position(self.grid_pos, self.target_pos, self.game.walls)
#     self.direction = self.get_next_direction(next_pos)

def next_cell_position(current_grid_pos, target_grid_pos, map):
    """
    function returns the value of the next cell
    where the enemy must go to get to the target
    as quickly as possible
    """
    shortest_path = breadth_first_search(current_grid_pos, target_grid_pos, map)
    return shortest_path[1]

def get_next_direction(next_pos):
    next_direction = vec(
        next_pos[0] - grid_pos[0],
        next_pos[1] - grid_pos[1]
    )
    return next_direction



def breadth_first_search(start_grid_pos, target_grid_pos, map):
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

next_pos = next_cell_position(grid_pos, target_pos, map_list)

direction = get_next_direction(next_pos)

# print(grid_pos)  # [14, 11]
# print(target_pos) # [17, 23]
# print(map_list)
print(9)
print(direction)