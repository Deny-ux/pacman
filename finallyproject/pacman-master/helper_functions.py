from constants import(
    COLUMNS,
    ROWS,
)
import json
import csv
import os


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
    """
    helper function for
    sorting array by second element
    """
    return elem[1]


def load_level_data_from_json(file_name):
    """
    This function returns dictionary
    with elements from json file
    If file is empty returns None
    """
    try:
        if os.path.getsize(file_name) == 0:
            return None

        with open(file_name, 'r') as handle:
            data_dict = json.load(handle)
            """
            Check if all necessary elements
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


def load_high_score_data_from_file(file_name):
    """
    This function returns a list with scores
    from file with csv extension
    """
    try:
        with open(file_name) as handle:
            people = []
            reader = csv.DictReader(handle)
            try:
                for row in reader:
                    name = row["name"]
                    score = int(row["score"])
                    people.append((name, score))
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
    """
    This function writes scores
    to score file with csv extension"""
    try:
        score_list.sort(key=take_second, reverse=True)
        with open(file_name, "w") as handle:
            handle.write("name,score\n")
            for score_item in score_list:
                handle.write(f"{score_item[0]},{str(score_item[1])}\n")


    except IsADirectoryError:
        raise ScoreFileIsDirectoryError("Can only work with files")
    except PermissionError:
        raise ScoreFilePermissionError(
            "You don't have permission to open high score file!")


def get_updated_high_score_list(new_score_item, file_name):
    """
    If new_score is greater than
    minimum value of high score list from file
    or length of list of high score is less than 10
    than new_score will be added to list of scores
    """
    new_score =  new_score_item[1]
    people = load_high_score_data_from_file(file_name)
    people.sort(key=take_second, reverse=True)
    if len(people) < 10:
        people.append(new_score_item)
    elif people[len(people)-1][1] < new_score:
        people.pop(len(people)-1)
        people.append(new_score_item)
        people.sort(key=take_second, reverse=True)
    return people


def get_walls_list_pos(list_walls_pos):
        """
        Create a list which
        represent a map of walls
        """
        map = [["0" for x in range(COLUMNS)] for y in range(ROWS)]
        for wall_pos in list_walls_pos:
            x, y = wall_pos[0], wall_pos[1]
            map[y][x] = "W"
        return map
