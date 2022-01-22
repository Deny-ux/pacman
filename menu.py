from numpy import blackman
import pygame
# from game import Game # COMMENT AT ALL COST
from constants import *
import helper_functions
from pygame.math import Vector2 as vec

class Menu:
    def __init__(self, game) -> None:
        self.game = game
        # self.run_display = False
        self.cursor_target = "Start game"
        self.cursor_rect = pygame.Rect(MAIN_START_X_POS + CURSOR_OFFSET_X, MAIN_START_Y_POS, CURSOR_WIDTH, CURSOR_HEIGHT)
        cursor_image = pygame.image.load(CURSOR_IMAGE_PATH)
        self.cursor_image = pygame.transform.scale(cursor_image, (CURSOR_WIDTH, CURSOR_HEIGHT))

    def draw_cursor(self):
        self.game.window.blit(self.cursor_image, (self.cursor_rect.x, self.cursor_rect.y))

    def display_menu(self):
        pass


class MainMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.show_main_menu = True
        # self.state = "MainMenu"

    def check_events(self):
        if self.game.DOWN_KEY:
            if self.cursor_target == "Start game":
                self.cursor_target = "High score"
                self.cursor_rect.x, self.cursor_rect.y = MAIN_HIGH_SCORE_X_POS + CURSOR_OFFSET_X, MAIN_HIGH_SCORE_Y_POS
            elif self.cursor_target == "High score":
                self.cursor_target = "Credits"
                self.cursor_rect.x, self.cursor_rect.y = MAIN_CREDITS_X_POS + CURSOR_OFFSET_X, MAIN_CREDITS_Y_POS
            elif self.cursor_target == "Credits":
                self.cursor_target = "Exit"
                self.cursor_rect.x, self.cursor_rect.y = MAIN_EXIT_X_POS + CURSOR_OFFSET_X, MAIN_EXIT_Y_POS
            elif self.cursor_target == "Exit":
                self.cursor_target = "Start game"
                self.cursor_rect.x, self.cursor_rect.y = MAIN_START_X_POS+ CURSOR_OFFSET_X, MAIN_START_Y_POS
        elif self.game.UP_KEY:
            if self.cursor_target == "Start game":
                self.cursor_target = "Exit"
                self.cursor_rect.x, self.cursor_rect.y = MAIN_EXIT_X_POS + CURSOR_OFFSET_X, MAIN_EXIT_Y_POS
            elif self.cursor_target == "High score":
                self.cursor_target = "Start game"
                self.cursor_rect.x, self.cursor_rect.y = MAIN_START_X_POS + CURSOR_OFFSET_X, MAIN_START_Y_POS
            elif self.cursor_target == "Credits":
                self.cursor_target = "High score"
                self.cursor_rect.x, self.cursor_rect.y = MAIN_HIGH_SCORE_X_POS + CURSOR_OFFSET_X, MAIN_HIGH_SCORE_Y_POS
            elif self.cursor_target == "Exit":
                self.cursor_target = "Credits"
                self.cursor_rect.x, self.cursor_rect.y = MAIN_CREDITS_X_POS + CURSOR_OFFSET_X, MAIN_CREDITS_Y_POS
        elif self.game.ENTER_KEY:
            if self.cursor_target == "Start game":
                ("PRESSED ENTER IS START GAME")
                self.game.current_menu = self.game.choose_game_menu
            elif self.cursor_target == "High score":
                self.game.current_menu = self.game.high_score_menu
            elif self.cursor_target == "Credits":
                self.game.current_menu = self.game.credits_menu
            elif self.cursor_target == "Exit":
                self.game.close_game()


    def display_menu(self):
        while self.game.current_menu == self.game.main_menu :

            self.game.check_events()
            self.check_events()
            self.game.window.fill(BLACK)
            self.game.draw_text(
                self.game.window,f'Hello {self.game.player_name}',
                 MAIN_GREETING_SIZE,  [MAIN_GREETING_X_POS, MAIN_GREETING_Y_POS], ORANGE)
            self.game.draw_text(
                self.game.window, "Start game", MAIN_START_SIZE,
                [MAIN_START_X_POS, MAIN_START_Y_POS], RED, False
            )
            self.game.draw_text(
                self.game.window, "High score", MAIN_HIGH_SCORE_SIZE,
                [MAIN_HIGH_SCORE_X_POS, MAIN_HIGH_SCORE_Y_POS], YELLOW,
                False
            )
            self.game.draw_text(
                self.game.window, "Credits", MAIN_CREDITS_SIZE,
                [MAIN_CREDITS_X_POS, MAIN_CREDITS_Y_POS], YELLOW,
                False
            )
            self.game.draw_text(
                self.game.window, "Exit", MAIN_EXIT_SIZE,
                [MAIN_EXIT_X_POS, MAIN_EXIT_Y_POS], YELLOW,
                False
            )
            self.draw_cursor()
            pygame.display.update()
            self.game.reset_keys()


class CreditsMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)

    def display_menu(self):
        while self.game.current_menu == self.game.credits_menu:
            self.game.window.fill(BLACK)
            self.game.check_events()

            self.check_events()
            self.game.draw_text(
                self.game.window, "Made with great patience", CREDITS_TEXT_SIZE,
                [HALF_DISP_WIDTH, CREDITS_TEXT1_Y_POS], GREEN,
                True
            )
            self.game.draw_text(
                self.game.window, "By Denys Dev", CREDITS_TEXT_SIZE,
                [HALF_DISP_WIDTH, CREDITS_TEXT2_Y_POS], GREEN,
                True
            )
            self.game.draw_text(
                self.game.window, "Press escape to go back", CREDITS_ESCAPE_SIZE,
                [HALF_DISP_WIDTH, CREDITS_ESCAPE_Y_POS], RED,
                True
            )
            pygame.display.update()
            self.game.reset_keys()

    def check_events(self):
        if self.game.ESC_KEY:
            self.game.current_menu = self.game.main_menu


class HighScoreMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.score_list = helper_functions.load_high_score_data_from_file(SCORE_FILE_NAME)

    def display_menu(self):
        self.game.check_events()
        self.check_events()
        self.game.window.fill(BLACK)
        self.game.draw_text(
                self.game.window, "High score", CASUAL_TEXT_SIZE,
                [SCORE_TITLE_X_POS, SCORE_TITLE_Y_POS], ORANGE,
                False
            )
        self.game.draw_text(
                self.game.window, "Press escape to go back", 15,
                [SCORE_ESCAPE_X_POS, SCORE_ESCAPE_Y_POS], GREEN,
                False
            )
        self.display_score_list()
        pygame.display.update()
        self.game.reset_keys()

    def display_score_list(self):
        global j
        score_list = \
            helper_functions.load_high_score_data_from_file(SCORE_FILE_NAME)
        for i, score_item in enumerate(score_list):
            score_name = score_item[0]
            score = str(score_item[1])
            score_pos = f"{str(i+1):>2}   {score_name}"
            self.game.draw_text(
                self.game.window, score_pos, SCORE_TEXT_SIZE,
                [SCORE_LIST_OFFSET, (i+1)*SCORE_ITEM_HEIGHT + SCORE_FIRST_ITEM_Y_POS], ORANGE,
                False
            )
            self.game.draw_text(
                self.game.window, score, SCORE_TEXT_SIZE,
                [SCORE_LIST_OFFSET+ 300, (i+1)*SCORE_ITEM_HEIGHT + SCORE_FIRST_ITEM_Y_POS], ORANGE,
                False
            )



    def check_events(self):
        if self.game.ESC_KEY:
            self.game.current_menu = self.game.main_menu


class SetNameMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.input_rect = pygame.Rect(280, 150, 250, 32)
        self.input_text = ""

    def display_menu(self):

        while self.game.current_menu == self.game.set_name_menu:
            self.game.window.fill(BLACK)
            self.game.draw_text(
            self.game.window, "Type your nickname", CASUAL_TEXT_SIZE,
            [HALF_DISP_WIDTH, 70], ORANGE
            )
            self.game.draw_text(
                self.game.window, "Nickname can not be empty", 12,
                [HALF_DISP_WIDTH, 230], RED
            )
            self.game.draw_text(
                self.game.window, f"Max length of name is {MAX_LEN_NAME}", 12,
                [HALF_DISP_WIDTH, 260], RED
            )
            self.game.draw_text(
                self.game.window, "Press ENTER to continue", 15,
                [HALF_DISP_WIDTH, DISPLAY_HEIGHT-80], ORANGE
            )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.close_game()
                elif event.type == pygame.KEYDOWN:
                    """
                    Text processing from keyboard
                    """
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(self.input_text) > 0:
                            self.game.player_name = self.input_text
                            self.game.current_menu = self.game.main_menu
                        break
                    elif len(self.input_text) < MAX_LEN_NAME:
                        self.input_text += event.unicode
            pygame.draw.rect(self.game.window, YELLOW , self.input_rect,  2)
            text_surface = self.game.font.render(self.input_text, True, (255, 255, 255))
            self.game.window.blit(text_surface, (self.input_rect.x+ 5, self.input_rect.y+5))


            pygame.display.update()
        self.game.reset_keys()  # added just in case of some bugs occur


class ChooseGameMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.cursor_target = "Start new game"
        self.cursor_rect.x, self.cursor_rect.y = \
            CHOOSE_NEW_GAME_X_POS + CURSOR_OFFSET_X, CHOOSE_NEW_GAME_Y_POS

    def display_menu(self):
        while self.game.current_menu == self.game.choose_game_menu and \
            not self.game.playing:
            self.game.window.fill(BLACK)
            self.game.check_events()
            self.check_events()
            self.game.draw_text(
                self.game.window, "Load saved game", CASUAL_TEXT_SIZE,
                [CHOOSE_LOAD_LAST_GAME_X_POS, CHOOSE_LOAD_LAST_GAME_Y_POS], RED,
                False
            )
            self.game.draw_text(
                self.game.window, "Start new game", CASUAL_TEXT_SIZE,
                [CHOOSE_NEW_GAME_X_POS, CHOOSE_NEW_GAME_Y_POS], RED,
                False
            )
            self.game.draw_text(
                self.game.window, "Press escape to go back", CASUAL_TEXT_SIZE-4,
                [CHOOSE_GO_BACK_X_POS, CHOOSE_GO_BACK_Y_POS], GREEN,
                False
            )
            self.draw_cursor()
            pygame.display.update()
            self.game.reset_keys()

    def check_events(self):
        if self.game.DOWN_KEY:
            if self.cursor_target == "Start new game":
                self.cursor_target = "Load saved game"
                self.cursor_rect.x, self.cursor_rect.y = \
                    CHOOSE_LOAD_LAST_GAME_X_POS + CURSOR_OFFSET_X, CHOOSE_LOAD_LAST_GAME_Y_POS
            elif self.cursor_target == "Load saved game":
                self.cursor_target = "Start new game"
                self.cursor_rect.x, self.cursor_rect.y = \
                    CHOOSE_NEW_GAME_X_POS + CURSOR_OFFSET_X, CHOOSE_NEW_GAME_Y_POS
        elif self.game.UP_KEY:
            if self.cursor_target == "Start new game":
                self.cursor_target = "Load saved game"
                self.cursor_rect.x, self.cursor_rect.y = \
                    CHOOSE_LOAD_LAST_GAME_X_POS + CURSOR_OFFSET_X, CHOOSE_LOAD_LAST_GAME_Y_POS
            elif self.cursor_target == "Load saved game":
                self.cursor_target = "Start new game"
                self.cursor_rect.x, self.cursor_rect.y = \
                    CHOOSE_NEW_GAME_X_POS + CURSOR_OFFSET_X, CHOOSE_NEW_GAME_Y_POS
        elif self.game.ESC_KEY:
            self.game.current_menu = self.game.main_menu
        elif self.game.ENTER_KEY:
            if self.cursor_target == "Load saved game":
                self.game.load_saved_game()
                self.game.playing = True
            elif self.cursor_target == "Start new game":
                self.game.start_new_game()
                self.game.playing = True

class FinishedGameMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.cursor_target = "Play again"
        self.cursor_rect.x, self.cursor_rect.y = \
            FINISH_PLAY_AGAIN_POS[0] + CURSOR_OFFSET_X, FINISH_PLAY_AGAIN_POS[1]

    def check_events(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            if self.cursor_target == "Play again":
                self.cursor_target = "Go to main menu"
                self.cursor_rect.x, self.cursor_rect.y = \
                    FINISH_GO_MAIN_POS[0] + CURSOR_OFFSET_X, FINISH_GO_MAIN_POS[1]
            elif self.cursor_target == "Go to main menu":
                self.cursor_target = "Play again"
                self.cursor_rect.x, self.cursor_rect.y = \
                    FINISH_PLAY_AGAIN_POS[0] + CURSOR_OFFSET_X, FINISH_PLAY_AGAIN_POS[1]
        elif self.game.ENTER_KEY:
            if self.cursor_target == "Go to main menu":
                ###### UPDATE ####
                new_score_item = (self.game.player_name, self.game.player.score)
                new_high_score_list = \
                    helper_functions.get_updated_high_score_list(new_score_item, SCORE_FILE_NAME)
                helper_functions.write_high_score_data_to_file(new_high_score_list, SCORE_FILE_NAME)
                self.game.playing = False
                self.game.player.reset()

                self.game.current_menu = self.game.main_menu
            elif self.cursor_target == "Play again":
                saved_lives = self.game.player.lives
                saved_score = self.game.player.score
                self.game.start_new_game(saved_score, saved_lives)
                self.game.playing = True

    def display_menu(self):
        while self.game.current_menu == self.game.finished_game_menu and \
            not self.game.playing:
            self.game.window.fill(BLACK)
            self.game.check_events()
            self.check_events()
            self.game.draw_text(
                self.game.window, "You finished level", CASUAL_TEXT_SIZE,
                [HALF_DISP_WIDTH, 100], WHITE,
                True
            )
            self.game.draw_text(
                self.game.window, "Go to main menu", CASUAL_TEXT_SIZE,
                FINISH_GO_MAIN_POS, RED,
                False
            )
            self.game.draw_text(
                self.game.window, "Start new game", CASUAL_TEXT_SIZE,
                FINISH_PLAY_AGAIN_POS, RED,
                False
            )
            self.draw_cursor()
            pygame.display.update()
            self.game.reset_keys()
import player
###########################
class PauseMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.cursor_target = "Continue"
        self.cursor_rect.x, self.cursor_rect.y = \
        PAUSE_CONTINUE_POS[0] + CURSOR_OFFSET_X, PAUSE_CONTINUE_POS[1]

    def check_events(self):
        if self.game.DOWN_KEY:
            if self.cursor_target == "Continue":
                self.cursor_target = "Save game"
                self.cursor_rect.x, self.cursor_rect.y = PAUSE_SAVE_GAME_POS[0] + CURSOR_OFFSET_X, PAUSE_SAVE_GAME_POS[1]
            elif self.cursor_target == "Save game":
                self.cursor_target = "Go to main menu"
                self.cursor_rect.x, self.cursor_rect.y = PAUSE_GO_MAIN_POS[0] + CURSOR_OFFSET_X, PAUSE_GO_MAIN_POS[1]
            elif self.cursor_target == "Go to main menu":
                self.cursor_target = "Continue"
                self.cursor_rect.x, self.cursor_rect.y = PAUSE_CONTINUE_POS[0] + CURSOR_OFFSET_X, PAUSE_CONTINUE_POS[1]
        elif self.game.UP_KEY:
            if self.cursor_target == "Continue":
                self.cursor_target = "Go to main menu"
                self.cursor_rect.x, self.cursor_rect.y = PAUSE_GO_MAIN_POS[0] + CURSOR_OFFSET_X, PAUSE_GO_MAIN_POS[1]
            elif self.cursor_target == "Save game":
                self.cursor_target = "Continue"
                self.cursor_rect.x, self.cursor_rect.y = PAUSE_CONTINUE_POS[0] + CURSOR_OFFSET_X, PAUSE_CONTINUE_POS[1]
            elif self.cursor_target == "Go to main menu":
                self.cursor_target = "Save game"
                self.cursor_rect.x, self.cursor_rect.y = PAUSE_SAVE_GAME_POS[0] + CURSOR_OFFSET_X, PAUSE_SAVE_GAME_POS[1]
        elif self.game.ENTER_KEY:
            if self.cursor_target == "Continue":
                self.game.playing = True
            elif self.cursor_target == "Save game":
                self.game.save_current_game_to_file(SAVED_GAME_FILE_NAME)
            elif self.cursor_target == "Go to main menu":
                if self.game.player is not None:
                    new_score_item = (self.game.player_name, self.game.player.score)
                    new_high_score_list = \
                        helper_functions.get_updated_high_score_list(new_score_item, SCORE_FILE_NAME)
                    helper_functions.write_high_score_data_to_file(new_high_score_list, SCORE_FILE_NAME)
                self.game.current_menu = self.game.main_menu

    def display_menu(self):

        while self.game.current_menu == self.game.pause_menu and \
            not self.game.playing:
            self.game.window.fill(BLACK)
            self.game.check_events()
            self.check_events()
            self.game.draw_text(
                self.game.window, "PAUSE", CASUAL_TEXT_SIZE+10,
                [HALF_DISP_WIDTH, 100], ORANGE,
                True
            )

            self.game.draw_text(
                self.game.window, "Continue", CASUAL_TEXT_SIZE,
                PAUSE_CONTINUE_POS, YELLOW,
                False
            )
            self.game.draw_text(
                self.game.window, "Save game", CASUAL_TEXT_SIZE,
                PAUSE_SAVE_GAME_POS, YELLOW,
                False
            )
            self.game.draw_text(
                self.game.window, "Go to main menu", CASUAL_TEXT_SIZE,
                PAUSE_GO_MAIN_POS, YELLOW,
                False
            )
            self.draw_cursor()
            pygame.display.update()
            self.game.reset_keys()



class GameOverMenu(Menu):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.cursor_target = "Start new game"
        self.cursor_rect.x, self.cursor_rect.y = \
        GAME_OVER_AGAIN_POS[0] + CURSOR_OFFSET_X, GAME_OVER_AGAIN_POS[1]

    def check_events(self):
        if self.game.DOWN_KEY or self.game.UP_KEY:
            if self.cursor_target == "Start new game":
                self.cursor_target = "Go to main menu"
                self.cursor_rect.x, self.cursor_rect.y = \
                    GAME_OVER_GO_MAIN_POS[0] + CURSOR_OFFSET_X, GAME_OVER_GO_MAIN_POS[1]
            elif self.cursor_target == "Go to main menu":
                self.cursor_target = "Start new game"
                self.cursor_rect.x, self.cursor_rect.y = \
                    GAME_OVER_AGAIN_POS[0] + CURSOR_OFFSET_X, GAME_OVER_AGAIN_POS[1]
        elif self.game.ENTER_KEY:
            if self.game.player is not None:
                new_score_item = (self.game.player_name, self.game.player.score)
                new_high_score_list = \
                    helper_functions.get_updated_high_score_list(new_score_item, SCORE_FILE_NAME)
                helper_functions.write_high_score_data_to_file(new_high_score_list, SCORE_FILE_NAME)
            if self.cursor_target == "Go to main menu":
                self.game.current_menu = self.game.main_menu
            elif self.cursor_target == "Start new game":
                self.game.start_new_game()
                self.game.playing = True

    def display_menu(self):

        while self.game.current_menu == self.game.game_over_menu and \
            not self.game.playing:
            self.game.window.fill(BLACK)
            self.game.check_events()
            self.check_events()
            self.game.draw_text(
                self.game.window, "GAME OVER", CASUAL_TEXT_SIZE+10,
                [HALF_DISP_WIDTH, 100], WHITE,
                True
            )
            self.game.draw_text(
                self.game.window, "Go to main menu", CASUAL_TEXT_SIZE,
                FINISH_GO_MAIN_POS, RED,
                False
            )
            self.game.draw_text(
                self.game.window, "Start new game", CASUAL_TEXT_SIZE,
                FINISH_PLAY_AGAIN_POS, RED,
                False
            )
            self.draw_cursor()
            pygame.display.update()
            self.game.reset_keys()