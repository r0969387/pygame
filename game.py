import pygame
import sys
from menu import *
from pygame.locals import *
import random
from pygame import mixer
from settings import *


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 1200, 700
        self.display = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.window = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.font_name = 'fonts/8-BIT WONDER.TTF'
        self.font_name1 = 'fonts/AmazDooMLeft.ttf'
        self.font_name2 = 'fonts/kinryu_karasu27.ttf'
        self.WHITE, self.BLACK, self.RED = (224, 224, 224), (0, 0, 0), (255, 0, 0)
        self.BG = pygame.image.load('images/BG better 2.jpg')
        self.BG = pygame.transform.scale(self.BG, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.BG_CREDITS = pygame.image.load('images/image for credirs.jpg')
        self.background_gameloop = pygame.image.load('images/background for game_loop.png')
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.cur_menu = self.main_menu
        pygame.display.set_caption('Political Game')
        icon = pygame.image.load('images/ukraine.png')
        pygame.display.set_icon(icon)

        # Initialize sprite groups

        self.play_button_rect = pygame.Rect(self.SCREEN_WIDTH / 2 - 60, self.SCREEN_HEIGHT / 2 - 90, 120, 40)
        self.state = "menu"  # Initially set the state to menu

    def game_loop(self):
        # globals of my game

        global game_started, game_over, spaceship
        global last_alien_shot, countdown, last_count
        global alien_group, bullet_group, alien_bullet_group, explosion_group
        global revo_group, revo_red_group, bullets_boost_group, points

        # end of globals

        play_rect = pygame.image.load('images/plat Rect2.png')
        play_rect = pygame.transform.scale(play_rect, (180, 130))

        # self.back_button_rect = pygame.Rect(self.SCREEN_WIDTH / 2 - 100, self.SCREEN_HEIGHT / 2 + 20, 200, 30)

        while self.playing:
            pygame.mixer.music.stop()
            music_game_loop.play()
            self.check_events()
            if self.BACK_KEY:
                if self.state == "game_screen":
                    self.state = "menu"
                else:
                    self.playing = False
                    music_game_loop.stop()

            if self.state == "menu":
                self.display.blit(self.background_gameloop, (0, 0))
                self.draw_text_main_white_custom('Space Democracy', 35, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 250)
                play_button_x = self.SCREEN_WIDTH / 2 - 86
                play_button_y = self.SCREEN_HEIGHT / 2 - 129
                self.display.blit(play_rect, (play_button_x, play_button_y))
                self.draw_text_main_white_custom('Play', 25, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - 70)
                # self.draw_text_main_white_custom('Back', 20, self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + 30)


                mouse_pos = pygame.mouse.get_pos()
                mouse_click = pygame.mouse.get_pressed()

                if self.play_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
                    self.state = "game_screen"
                    music_game_loop.stop()


            elif self.state == "game_screen":
                music_game_loop.stop()
                # game file
                import logic




            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.cur_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_s:
                    self.DOWN_KEY = True
                if event.key == pygame.K_w:
                    self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text_titile(self, text, size, x, y):
        font = pygame.font.Font(self.font_name1, size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


    def draw_text_titile_white_custom1(self, text, size, x, y):
        font = pygame.font.Font(self.font_name1, size)

        # Create the main black text surface
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x, y))

        # Create the white outline by rendering the text slightly offset multiple times
        outline_color = self.BLACK
        outline_thickness = 3  # Thickness of the outline

        # Render the white outline by offsetting the text and keeping the same center
        for dx, dy in [(-outline_thickness, 0), (outline_thickness, 8), (0, -outline_thickness), (8, outline_thickness),
                       (-outline_thickness, -outline_thickness), (outline_thickness, outline_thickness),
                       (-outline_thickness, outline_thickness), (outline_thickness, -outline_thickness)]:
            outline_surface = font.render(text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(x + dx, y + dy))
            self.display.blit(outline_surface, outline_rect)

        # Now draw the main black text in the center
        self.display.blit(text_surface, text_rect)

    def draw_text_titile_white_custom2(self, text, size, x, y):
        font = pygame.font.Font(self.font_name1, size)

        # Create the main black text surface
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x, y))

        # Create the white outline by rendering the text slightly offset multiple times
        outline_color = self.BLACK
        outline_thickness = 1  # Thickness of the outline

        # Render the white outline by offsetting the text and keeping the same center
        for dx, dy in [(-outline_thickness, 0), (outline_thickness, 4), (0, -outline_thickness), (4, outline_thickness),
                       (-outline_thickness, -outline_thickness), (outline_thickness, outline_thickness),
                       (-outline_thickness, outline_thickness), (outline_thickness, -outline_thickness)]:
            outline_surface = font.render(text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(x + dx, y + dy))
            self.display.blit(outline_surface, outline_rect)

        # Now draw the main black text in the center
        self.display.blit(text_surface, text_rect)

    def draw_text_main_white_custom(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)

        # Create the main black text surface
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x, y))

        # Create the white outline by rendering the text slightly offset multiple times
        outline_color = self.BLACK
        outline_thickness = 2  # Thickness of the outline

        # Render the white outline by offsetting the text and keeping the same center
        for dx, dy in [(-outline_thickness, 0), (outline_thickness, 0), (0, -outline_thickness), (0, outline_thickness),
                       (-outline_thickness, -outline_thickness), (outline_thickness, outline_thickness),
                       (-outline_thickness, outline_thickness), (outline_thickness, -outline_thickness)]:
            outline_surface = font.render(text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(x + dx, y + dy))
            self.display.blit(outline_surface, outline_rect)

        # Now draw the main black text in the center
        self.display.blit(text_surface, text_rect)


    def draw_text_main_white(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_text_main(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)


    def draw_text_main_for_credits(self, text, size, x, y):
        font = pygame.font.Font(self.font_name2, size)

        # Create the main black text surface
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x, y))

        # Create the white outline by rendering the text slightly offset multiple times
        outline_color = self.BLACK
        outline_thickness = 2  # Thickness of the outline

        # Render the white outline by offsetting the text and keeping the same center
        for dx, dy in [(-outline_thickness, 0), (outline_thickness, 0), (0, -outline_thickness), (0, outline_thickness),
                       (-outline_thickness, -outline_thickness), (outline_thickness, outline_thickness),
                       (-outline_thickness, outline_thickness), (outline_thickness, -outline_thickness)]:
            outline_surface = font.render(text, True, outline_color)
            outline_rect = outline_surface.get_rect(center=(x + dx, y + dy))
            self.display.blit(outline_surface, outline_rect)

        for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, 0), (0, 0)]:
            thick_surface = font.render(text, True, self.WHITE)
            thick_rect = thick_surface.get_rect(center=(x + dx, y + dy))
            self.display.blit(thick_surface, thick_rect)

        # Now draw the main black text in the center
        self.display.blit(text_surface, text_rect)

