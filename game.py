# from turtle import width
from turtle import goto
from numpy import empty
import pygame
from pygame.math import Vector2 as vec
from menu import *
from player import *
from constants import *
from menu import *
import helper_functions
import sys
from enemy import Enemy

class Game():
    def __init__(self) -> None:
        pygame.init()
        self.run_menu, self.playing = True, False
        # self.playing, self.run_menu = True, False # CHANGE
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
        # self.current_menu = self.set_name_menu
        self.current_menu = self.set_name_menu
        self.font = pygame.font.Font(FONT_NAME, 20)

    # def load_new_map(self):
        # dict_elements = helper_functions.get_dict_elements_from_map(NEW_MAP_FILE_NAME)
        # dict_elements = helper_functions.load_level1_from_json(NEW_MAP_FILE_NAME)
        # self.walls = dict_elements.get("walls")
        # self.coins = dict_elements.get("coins")
        # self.enemies = dict_elements.get("enemies")
        # self.player.grid_pos = dict_elements.get("player_grid_pos")
        # self.player.pix_pos = self.player.get_pix_pos(self.player.grid_pos)

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

    def draw_energizers(self):
        for energizer in self.energizers:
            pix_pos = self.get_pix_pos(energizer)
            x, y = pix_pos[0], pix_pos[1]
            pygame.draw.circle(
                self.window, PURPLE,
                (x + SQUARE_WIDTH//2, y + SQUARE_HEIGHT//2),
                SQUARE_WIDTH//2-4)


    def run(self):
        while True:
            while self.playing:
                print("You are playing yeaaay")
                self.play()
                pygame.display.update()
            if self.current_menu is not None:
                self.current_menu.display_menu()
            if self.playing == self.run_menu == False:  # Quit the game
                self.close_game()

    def save_current_game_to_file(self, file_name):
        pass

    # def load_game_from_file(self, file_name):

    # def set_enemies(self):
    #     self.enemies = [
    #         Enemy(self, RANDOM_MOTION_MODE, ENEMY_1_START_POS, RED, 1)
    #         # ENEMY_2_START_POS,
    #         # ENEMY_3_START_POS,
    #         # ENEMY_4_START_POS
    #     ]

    def play(self):
        self.draw_walls()
        while self.playing:
            self.window.fill(BLACK)
            self.draw_current_score()
            self.draw_walls()
            self.draw_coins()
            self.draw_energizers()
            self.check_events()
            # self.draw_grid()
            for enemy in self.enemies:
                enemy.update()
            self.player.update()
            self.player.draw()
            if self.game_is_finished():
                self.playing, self.run_menu = False, True
                self.current_menu = self.finished_game_menu
            if self.ESC_KEY:  # MAKE MENU
                self.run_menu, self.playing = True, False

            self.clock.tick(MAX_FPS)  # to control FPS
            pygame.display.update()


    def write_data_from_file(self, file_name, saved_score=0, saved_lives=COUNT_PLAYER_START_LIVES):
        self.enemies.clear()
        dict_elements = helper_functions.load_level_data_from_json(file_name)

        self.walls = dict_elements.get("walls")
        self.coins = dict_elements.get("coins")
        start_player_grid_pos = dict_elements.get("player_grid_pos")
        self.player = Player(self, start_player_grid_pos, saved_score, saved_lives)
        enemies = dict_elements.get("enemies")
        for enemy in enemies:
            self.enemies.append(Enemy(
                self, enemy["movement_mode"],
                enemy["pos"], enemy["color"],
                enemy["speed"]))


        self.energizers = dict_elements.get("energizers")
        self.wall_map = helper_functions.get_walls_list_pos(self.walls)

    def set_data_from_file(self, file_name):
        """
        This function reads a json file with a
        game settings and write these data to variables
        inside classes
        """


    def load_saved_game(self):
        self.write_data_from_file(SAVED_GAME_FILE_NAME)


    def start_new_game(self, saved_score=0, saved_lives=COUNT_PLAYER_START_LIVES):
        self.write_data_from_file(NEW_MAP_FILE_NAME, saved_score, saved_lives)
        # self.load_new_map()
        # self.player.score == 0

    def update_events(self):
        pass

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_game()

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
        print(999999999)
        for enemy in self.enemies:
            enemy.reset_position_and_direction()

    def draw_grid(self):
        for x in range(
            LEFT_RIGHT_PADDING,
            DISPLAY_WIDTH - LEFT_RIGHT_PADDING - SQUARE_WIDTH+1,
            SQUARE_WIDTH):
            for y in range(
            TOP_BOTTOM_PADDING,
            DISPLAY_HEIGHT - TOP_BOTTOM_PADDING - SQUARE_HEIGHT +1,
            SQUARE_HEIGHT):
                pygame.draw.rect(self.window, WHITE,
                (x, y, SQUARE_WIDTH, SQUARE_HEIGHT), 1)

    def game_is_finished(self):
        if len(self.coins) == 0:
            return True
        return False

    def close_game(self):
        pygame.quit()
        sys.exit()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.ENTER_KEY, self.ESC_KEY, self.RIGHT_KEY, self.LEFT_KEY = False, False,  False, False, False, False


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
            (grid_pos[0]* SQUARE_WIDTH) + LEFT_RIGHT_PADDING,
            (grid_pos[1]* SQUARE_HEIGHT) + TOP_BOTTOM_PADDING
        ]

    def draw_current_score(self):
        self.draw_text(
            self.window, f"Current score {self.player.score}",
            CASUAL_TEXT_SIZE-5, CURRENT_SCORE_POS, WHITE, False
        )
