import pygame
import json
from pygame.math import Vector2 as vec
from energizer import Energizer
from menu import *
from player import *
from constants import *
import helper_functions
import sys
from enemy import Enemy


class Game():
    def __init__(self) -> None:
        pygame.init()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        self.run_menu, self.playing = True, False
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.main_menu = MainMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.high_score_menu = HighScoreMenu(self)
        self.set_name_menu = SetNameMenu(self)
        self.choose_game_menu = ChooseGameMenu(self)
        self.finished_game_menu = FinishedGameMenu(self)
        self.pause_menu = PauseMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.save_file_is_empty_menu = SaveFileIsEmptyMenu(self)
        self.UP_KEY, self.DOWN_KEY = False, False
        self.ENTER_KEY, self.ESC_KEY = False, False
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.player_name = "Player"
        self.player = None
        self.wall_map = []
        self.walls = []
        self.coins = []
        self.enemies = []
        self.energizers = []
        self.time_to_eat_enemies = 0  # to display how much time player can eat enemies
        self.energizer_time_action_remaining = 0
        self.current_menu = self.set_name_menu
        self.font = pygame.font.Font(FONT_NAME, 20)

    def draw_walls(self):
        for wall_pos in self.walls:
            pix_pos = self.get_pix_pos(wall_pos)
            x, y = pix_pos[0], pix_pos[1]
            pygame.draw.rect(self.window, BLUE, (x, y, 20, 20), 3)

    def draw_coins(self):
        for coin_pos in self.coins:
            pix_pos = self.get_pix_pos(coin_pos)
            x, y = pix_pos[0], pix_pos[1]
            pygame.draw.circle(
                self.window, YELLOW,
                (x + SQUARE_WIDTH//2, y + SQUARE_HEIGHT//2),
                SQUARE_WIDTH//2-7)

    def run(self):
        while True:
            while self.playing:
                self.play()
                pygame.display.update()
            if self.current_menu is not None:
                self.current_menu.display_menu()
            if self.playing == self.run_menu == False:  # Quit the game
                self.close_game()

    def save_current_game_to_file(self, file_name):
        """
        This function writes the level data
        to json file so that program can
        load that level with saved parametrs
        (player position, enemies position, etc.)
        """
        with open(file_name, "w") as handle:
            data = dict()
            data["walls_pos_list"] = self.walls
            data["remaining_time_energizer"] = self.time_to_eat_enemies
            data["coins_pos_list"] = self.coins
            data["enemies"] = []
            for enemy in self.enemies:
                enemy_el = dict()
                enemy_el["current_grid_pos"] = enemy.grid_pos
                enemy_el["start_grid_pos"] = enemy.start_grid_pos
                enemy_el["color"] = enemy.initial_color
                enemy_el["movement_mode"] = enemy.initial_movement_mode
                enemy_el["speed"] = enemy.speed
                data["enemies"].append(enemy_el)

            player_dict = dict()
            player_dict["current_grid_pos"] = self.player.grid_pos
            player_dict["start_grid_pos"] = self.player.start_grid_pos
            player_dict["lives"] = self.player.lives
            player_dict["score"] = self.player.score
            data["energizers"] = dict()
            data["player"] = player_dict
            energizers_pos = []
            for energizer in self.energizers:
                energizers_pos.append(energizer.grid_pos)
                energizer_color = energizer.color
                energizer_secunds_duration = energizer.secunds_duration
            if len(energizers_pos) > 0:
                energizers = dict()
                energizers["grid_pos"] = energizers_pos
                energizers["color"] = energizer_color
                energizers["secunds_duration"] = energizer_secunds_duration
                data["energizers"] = energizers
            json.dump(data, handle, indent=2)

    def play(self):
        while self.playing:
            self.window.fill(BLACK)
            self.draw_current_score()
            self.draw_walls()
            self.draw_coins()
            self.check_events()
            for enemy in self.enemies:
                enemy.update()

            for energizer in self.energizers:
                energizer.draw()

            self.player.update()
            self.player.draw()
            if self.game_is_finished():
                self.playing, self.run_menu = False, True
                self.current_menu = self.finished_game_menu
            if self.ESC_KEY:  # MAKE MENU
                self.run_menu, self.playing = True, False

            self.clock.tick(MAX_FPS)  # to control FPS
            pygame.display.update()

    def set_data_from_file(self, file_name):
        """
        This function read json file with level
        setings and based on file content
        create level
        """
        self.enemies.clear()
        self.energizers.clear()

        dict_elements = helper_functions.load_level_data_from_json(file_name)
        if dict_elements is not None:
            self.time_to_eat_enemies = dict_elements["remaining_time_energizer"]
            player = dict_elements["player"]
            player_current_grid_pos = player["current_grid_pos"]
            player_start_grid_pos = player["start_grid_pos"]
            player_score = player["score"]
            player_lives = player["lives"]
            self.player = Player(self, player_start_grid_pos, player_current_grid_pos,
                                 player_score, player_lives)

            enemies = dict_elements.get("enemies")

            for enemy in enemies:
                movement_mode = enemy["movement_mode"]
                enemy_current_grid_pos = enemy["current_grid_pos"]
                enemy_start_grid_pos = enemy["start_grid_pos"]
                color = enemy["color"]
                speed = enemy["speed"]
                self.enemies.append(
                    Enemy(self, movement_mode, enemy_current_grid_pos,
                          enemy_start_grid_pos, color, speed)
                )

            self.walls = dict_elements["walls_pos_list"]
            self.coins = dict_elements["coins_pos_list"]

            energizers = dict_elements["energizers"]
            if len(energizers) > 0:
                energizer_color = energizers["color"]
                energizer_secunds_duration = energizers["secunds_duration"]
                for energizer_pos in energizers["grid_pos"]:
                    energizer = Energizer(self, energizer_pos, energizer_color, energizer_secunds_duration)
                    self.energizers.append(energizer)

            self.wall_map = helper_functions.get_walls_list_pos(self.walls)

    def load_saved_game(self):
        """
        Read data from file for
        saving level
        """
        self.set_data_from_file(SAVED_GAME_FILE_NAME)

    def start_new_game(self, saved_score=0, saved_lives=COUNT_PLAYER_START_LIVES):
        """
        Read data from file where initial
        content of level is located.
        If starts the game after passing level
        than score and count of lives is saved.
        Otherwise this data are setted by default
        """
        self.set_data_from_file(NEW_MAP_FILE_NAME)
        self.player.score = saved_score
        self.player.lives = saved_lives

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_game()
            elif event.type == pygame.USEREVENT and self.playing:
                self.time_to_eat_enemies -= 1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True
                elif event.key == pygame.K_ESCAPE:
                    if self.playing == True:
                        self.playing = False
                        self.current_menu = self.pause_menu

                    self.ESC_KEY = True
                elif event.key == pygame.K_DOWN:
                    if self.playing:
                        self.player.stored_direction = vec(0, 1)
                    self.DOWN_KEY = True
                elif event.key == pygame.K_UP:
                    if self.playing:
                        self.player.stored_direction = vec(0, -1)
                    self.UP_KEY = True
                elif event.key == pygame.K_RIGHT:
                    if self.playing:
                        self.player.stored_direction = vec(1, 0)
                    self.RIGHT_KEY == True
                elif event.key == pygame.K_LEFT:
                    if self.playing:
                        self.player.stored_direction = vec(-1, 0)
                    self.LEFT_KEY == True

    def reset_enemies(self):
        for enemy in self.enemies:
            enemy.reset_position_and_direction()

    def draw_grid(self):
        """
        Helper function to see grid
        where all elements will be located
        """
        for x in range(LEFT_RIGHT_PADDING,
                       DISPLAY_WIDTH - LEFT_RIGHT_PADDING - SQUARE_WIDTH + 1,
                       SQUARE_WIDTH):
            for y in range(TOP_BOTTOM_PADDING,
                           DISPLAY_HEIGHT - TOP_BOTTOM_PADDING - SQUARE_HEIGHT + 1,
                           SQUARE_HEIGHT):
                pygame.draw.rect(self.window, WHITE,
                (x, y, SQUARE_WIDTH, SQUARE_HEIGHT), 1)

    def game_is_finished(self):
        """
        According to the task
        game is finished after player ate all coins
        """
        if len(self.coins) == 0:
            return True
        return False

    def close_game(self):
        pygame.quit()
        sys.exit()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESC_KEY = False, False,  False, False
        self.RIGHT_KEY, self.LEFT_KEY = False, False

    def draw_text(self, screen, text, size, pos, color, is_centered=True):
        """
        Helper function to draw
        text in display
        """
        font = pygame.font.Font(FONT_NAME, size)

        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect()
        if is_centered:
            text_rect.center = (pos[0], pos[1])
        else:
            text_rect.x, text_rect.y = pos[0], pos[1]
        screen.blit(text_surface, text_rect)

    def get_pix_pos(self, grid_pos):
        """
        Returns the top left corner of
        position in reference to
        grid position
        """
        return [
            (grid_pos[0] * SQUARE_WIDTH) + LEFT_RIGHT_PADDING,
            (grid_pos[1] * SQUARE_HEIGHT) + TOP_BOTTOM_PADDING
        ]

    def draw_current_score(self):
        self.draw_text(
            self.window, f"Current score {self.player.score}",
            CASUAL_TEXT_SIZE-5, CURRENT_SCORE_POS, WHITE, False
        )
