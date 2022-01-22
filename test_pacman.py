import pytest
import constants
import helper_functions
import enemy
import player
import game
import energizer
from pygame.math import Vector2 as vec


def test_can_open_and_write_score_to_file():
    file_name = "test_score.csv"
    scores_list = [
        ("Player1", 9000),
        ("Player2", 80)
    ]
    helper_functions.write_high_score_data_to_file(scores_list, file_name)
    list_scores = helper_functions.load_high_score_data_from_file(file_name)
    assert list_scores == [
        ("Player1", 9000),
        ("Player2", 80)
    ]


def test_update_score_file_with_new_element():
    file_name = "test_score.csv"
    scores_list = [
        ("Player1", 9000),
        ("Player2", 80)
    ]
    helper_functions.write_high_score_data_to_file(scores_list, file_name)
    new_item = ("Player3", 10)
    new_score_list = helper_functions.get_updated_high_score_list(new_item, file_name)
    assert new_score_list == [
        ("Player1", 9000),
        ("Player2", 80),
        ("Player3", 10)
    ]


def test_update_score_file_deleting_minimum_score():
    file_name = "test_score.csv"
    scores_list = [
        ("Player1", 9000),
        ("Player2", 90),
        ("Player3", 80),
        ("Player4", 80),
        ("Player5", 80),
        ("Player6", 80),
        ("Player7", 80),
        ("Player8", 80),
        ("Player9", 70),
        ("Player10", 60)
    ]
    helper_functions.write_high_score_data_to_file(scores_list, file_name)
    new_item = ("Player11", 91)
    new_score_list = \
        helper_functions.get_updated_high_score_list(new_item, file_name)
    assert new_score_list ==[
        ("Player1", 9000),
        ("Player11", 91),
        ("Player2", 90),
        ("Player3", 80),
        ("Player4", 80),
        ("Player5", 80),
        ("Player6", 80),
        ("Player7", 80),
        ("Player8", 80),
        ("Player9", 70)
    ]


def test_file_with_high_score_data_mot_found():
    file_name = "fileNotExist.csv"
    with pytest.raises(helper_functions.ScoreFileNotFoundError):
        helper_functions.load_high_score_data_from_file(file_name)


def test_file_with_high_score_data_is_directory():
    directory_name = "testdict"
    with pytest.raises(helper_functions.ScoreFileIsDirectoryError):
        helper_functions.load_high_score_data_from_file(directory_name)


def test_load_level_file_is_empty():
    empty_file_name = "empty.json"
    assert helper_functions.load_level_data_from_json(empty_file_name) is None


def test_load_level_file_has_no_necessary_key():
    invalid_data_level_file = "non_valid_level.json"
    with pytest.raises(helper_functions.MalformedNewMapData):
        helper_functions.load_level_data_from_json(invalid_data_level_file)


def test_load_level_file_not_exists():
    not_exist_file_name = "non_exist.json"
    with pytest.raises(helper_functions.NewMapFileNotFoundError):
        helper_functions.load_level_data_from_json(not_exist_file_name)


def test_load_level_file_is_directory():
    directory_name = "testdict"
    with pytest.raises(helper_functions.NewMapFileIsDirectoryError):
        helper_functions.load_level_data_from_json(directory_name)


def test_is_collision_with_enemy():
    game1 = game.Game()
    player1 = player.Player(game1, [10, 10], [20, 10], 10, 3)
    enemy1 = enemy.Enemy(game1, constants.RANDOM_MOTION_MODE,
                         [20, 10], [10, 10], constants.RED, 1)
    enemy1_pix_pos = enemy1.get_pix_pos(enemy1.grid_pos)
    assert player1.is_collision_with_enemy(enemy1_pix_pos)


def test_is_not_collision_with_enemy():
    game1 = game.Game()
    player1 = player.Player(game1, [10, 10], [20, 10], 10, 3)
    enemy1 = enemy.Enemy(game1, constants.RANDOM_MOTION_MODE,
                         [22, 10], [10, 10], constants.RED, 1)
    enemy1_pix_pos = enemy1.get_pix_pos(enemy1.grid_pos)
    assert not player1.is_collision_with_enemy(enemy1_pix_pos)


def test_player_can_not_move_in_current_direction():
    game1 = game.Game()
    game1.walls = [[0, 0]]
    player1 = player.Player(game1, [10, 10], [0, 1], 10, 3)
    player1.direction = vec(0, -1)
    player1_can_move = player1.can_move()
    assert not player1_can_move


def test_player_can_move_in_direction():
    game1 = game.Game()
    game1.walls = [[2, 0], [3, 0]]
    player1 = player.Player(game1, [10, 10], [0, 1], 10, 3)
    player1.direction = vec(0, -1)
    player1_can_move = player1.can_move()
    assert player1_can_move


def test_player_can_change_direction():
    game1 = game.Game()
    game1.walls = [[2, 0], [3, 0]]
    player1 = player.Player(game1, [10, 10], [0, 1], 10, 3)
    player1.stored_direction = vec(0, -1)
    player1_can_change_direction = player1.can_change_direction()
    assert player1_can_change_direction


def test_player_can_not_change_direction():
    game1 = game.Game()
    game1.walls = [[0, 0]]
    player1 = player.Player(game1, [10, 10], [0, 1], 10, 3)
    player1.stored_direction = vec(0, -1)
    player1_can_change_direction = player1.can_change_direction()
    assert not player1_can_change_direction


def test_remove_live_after_hitting_enemy():
    game1 = game.Game()
    player1 = player.Player(game1, [10, 10], [20, 10], 10, 3)
    enemy1 = enemy.Enemy(game1, constants.RANDOM_MOTION_MODE,
                         [20, 10], [10, 10], constants.RED, 1)
    game1.enemies.append(enemy1)
    player1.update()
    assert player1.lives == 2


def test_player_in_energizer():
    game1 = game.Game()
    energizer1 = energizer.Energizer(game1, [10, 10], constants.PINK, 10)
    player1 = player.Player(game1, [10, 10], [10, 10], 10, 3)
    game1.energizers.append(energizer1)
    assert player1.in_energizer()


def test_player_on_coin():
    game1 = game.Game()
    game1.coins.append([1, 1])
    player1 = player.Player(game1, [1, 1], [1, 1], 10, 3)
    assert player1.on_coin()


def test_player_ate_coin():
    game1 = game.Game()
    game1.coins.append([1, 1])
    player1 = player.Player(game1, [1, 1], [1, 1], 0, 3)
    player1.update()
    assert player1.score == 1