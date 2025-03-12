import pygame
import sys
from pygame import mixer
from settings import *
from draw_text import *

# pygame.mixer.music.load('sounds/gimn_ukrani_-_gimn_ukrani_(z3.fm).mp3')
# pygame.mixer.music.set_volume(0.15)

# narodna_kosatska = pygame.mixer.Sound('sounds/ukranski_narodni.mp3')
# narodna_kosatska.set_volume(0.25)


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100



    def draw_cursor(self):
        self.game.draw_text_main_white_custom('*', 15, self.cursor_rect.x + 10, self.cursor_rect.y - 10)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 10
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 90
        self.quitx, self.quity = self.mid_w, self.mid_h + 130
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

        self.start_button_rect = pygame.Rect(self.startx - 60, self.starty - 25, 120, 25)
        self.options_button_rect = pygame.Rect(self.optionsx - 60, self.optionsy - 25, 120, 25)
        self.credits_button_rect = pygame.Rect(self.creditsx - 60, self.creditsy - 20, 120, 25)
        self.quit_button_rect = pygame.Rect(self.quitx - 60, self.quity - 20, 120, 25)




    def display_menu(self):
        self.run_display = True
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(1)
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.game.BG, (0, 0))

            self.game.draw_text_titile_white_custom1("Verhovna Rada", 100, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 200)

            self.game.draw_text_titile_white_custom2("Start Game", 40, self.startx, self.starty)

            self.game.draw_text_titile_white_custom2("Settings", 40, self.optionsx, self.optionsy)

            self.game.draw_text_titile_white_custom2("Credits", 40, self.creditsx, self.creditsy)

            self.game.draw_text_titile_white_custom2("Quit", 40, self.quitx, self.quity)

            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if self.start_button_rect.collidepoint(mouse_pos):
            if mouse_click[0]:
                self.run_display = False
                self.game.playing = True
                self.game.game_loop()

        elif self.options_button_rect.collidepoint(mouse_pos):
            if mouse_click[0]:
                self.game.cur_menu = self.game.options
                self.run_display = False

        elif self.credits_button_rect.collidepoint(mouse_pos):
            if mouse_click[0]:
                self.game.cur_menu = self.game.credits
                self.run_display = False

        elif self.quit_button_rect.collidepoint(mouse_pos):
            if mouse_click[0]:
                pygame.quit()
                sys.exit()
            self.run_display = False


        # Handle cursor navigation using keyboard
        self.move_cursor()

        if self.game.START_KEY:
            if self.state == 'Start':
                self.run_display = False
                self.game.playing = True
                self.game.game_loop()


            elif self.state == 'Options':
                self.game.cur_menu = self.game.options
            elif self.state == 'Credits':
                self.game.cur_menu = self.game.credits
            elif self.state == 'Quit':
                pygame.quit()
                sys.exit()
            self.run_display = False


    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = 'Quit'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Quit':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'



class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 60
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 100
        self.backx, self.backy = self.mid_w, self.mid_h + 140

        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

        self.volume_button_rect = pygame.Rect(self.volx - 90, self.voly - 30, 170, 30)
        self.controls_button_rect = pygame.Rect(self.controlsx - 90, self.controlsy - 30, 170, 30)
        self.back_button_rect = pygame.Rect(self.backx - 60, self.backy - 30, 110, 30)


    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.game.BG, (0, 0))

            self.game.draw_text_main_white_custom('Options', 30, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 30)
            self.game.draw_text_main_white_custom("Volume", 20, self.volx, self.voly - 15)
            self.game.draw_text_main_white_custom("Controls", 20, self.controlsx, self.controlsy - 15)
            self.game.draw_text_main_white_custom("Back", 20, self.backx, self.backy - 15)

            self.draw_cursor()
            self.blit_screen()



    def check_input(self):

        # mouse_pos = pygame.mouse.get_pos()
        # mouse_click = pygame.mouse.get_pressed()

        # if self.volume_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
        #     self.volume_loop()
        # elif self.controls_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
        #     self.controls_loop()
        # elif self.back_button_rect.collidepoint(mouse_pos) and mouse_click[0]:
        #     self.game.cur_menu = self.game.main_menu
        #     self.run_display = False


        if self.game.BACK_KEY:
            self.game.cur_menu = self.game.main_menu
            self.run_display = False

        if self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy)
                self.state = 'Back'
            elif self.state == 'Back':
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = 'Volume'

        elif self.game.UP_KEY:
            if self.state == 'Back':
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = 'Controls'
            elif self.state == 'Controls':
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
                self.state = 'Volume'
            elif self.state == 'Volume':
                self.cursor_rect.midtop = (self.backx + self.offset, self.backy)
                self.state = 'Back'

        if self.game.START_KEY:
            if self.state == 'Volume':
                self.run_display = False
                self.volume_loop()
            elif self.state == 'Controls':
                self.run_display = False
                self.controls_loop()
            elif self.state == 'Back':
                self.game.cur_menu = self.game.main_menu
                self.run_display = False


    """Display the volume menu (black screen, stop music)"""
    def volume_loop(self):
        volume_state = 'Quiet'
        self.cursor_rect.midtop = (self.game.SCREEN_WIDTH / 2 - 100, self.game.SCREEN_HEIGHT / 2 - 60)
        music_was_playing = pygame.mixer.music.get_busy()  # Check if music was playing before
        if music_was_playing:
            pygame.mixer.music.stop()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            volume_state = self.check_input_volume(volume_state)
            self.game.display.fill((0, 0, 0))
            self.game.draw_text_main_white('Volume Settings', 30, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 250)
            self.game.draw_text_main_white("Quiet", 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 70)
            self.game.draw_text_main_white("Normal", 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2)
            self.game.draw_text_main_white("Loud", 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 + 70)
            self.draw_cursor()

            if self.game.BACK_KEY:
                # Exit volume control screen
                self.run_display = False
                # Reset cursor to "Volume" option
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

            if self.game.BACK_KEY:
                # Exit volume control screen
                self.run_display = False
            self.blit_screen()

        if music_was_playing:
            pygame.mixer.music.play(-1)

    def check_input_volume(self, volume_state):
        if self.game.UP_KEY:
            if volume_state == 'Normal':
                volume_state = 'Quiet'
                self.cursor_rect.midtop = (self.game.SCREEN_WIDTH / 2 - 100, self.game.SCREEN_HEIGHT / 2 - 60)
            elif volume_state == 'Loud':
                volume_state = 'Normal'
                self.cursor_rect.midtop = (self.game.SCREEN_WIDTH / 2 - 100, self.game.SCREEN_HEIGHT / 2)
        elif self.game.DOWN_KEY:
            if volume_state == 'Quiet':
                volume_state = 'Normal'
                self.cursor_rect.midtop = (self.game.SCREEN_WIDTH / 2 - 100, self.game.SCREEN_HEIGHT / 2 + 10)
            elif volume_state == 'Normal':
                volume_state = 'Loud'
                self.cursor_rect.midtop = (self.game.SCREEN_WIDTH / 2 - 100, self.game.SCREEN_HEIGHT / 2 + 60 + 20)

        elif self.game.START_KEY:
            if volume_state == 'Quiet':
                pygame.mixer.music.set_volume(0.05)  # Set volume to low
            elif volume_state == 'Normal':
                pygame.mixer.music.set_volume(0.15)  # Set volume to normal
            elif volume_state == 'Loud':
                pygame.mixer.music.set_volume(0.5)  # Set volume to loud

        return volume_state

    """Display the control menu (black screen, stop music)"""
    def controls_loop(self):
        if pygame.mixer.music.get_busy():  # Check if music was playing before
            pygame.mixer.music.stop()
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.game.display.fill((0, 0, 0))  # Black screen

            self.game.draw_text_main_white('Controls Settings', 35, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 250)
            self.game.draw_text_main_white('Movement ', 25, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 150)
            self.game.draw_text_main_white('W , S forward and backward A , D left and right', 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 100)
            self.game.draw_text_main_white('Shooting', 25, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 50)
            self.game.draw_text_main_white('Left mouse button', 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2)

            if self.game.BACK_KEY:
                # Exit volume control screen
                self.run_display = False
                pygame.mixer.music.play()
            self.blit_screen()




class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sounds/ukranski_narodni.mp3')  # Use the same file for music playback
            pygame.mixer.music.play(-1)  # Loop the music
            pygame.mixer.music.set_volume(0.15)  # Set volume to match other music
        while self.run_display:
            self.game.check_events()
            if self.game.BACK_KEY:
                self.game.cur_menu = self.game.main_menu
                self.run_display = False
            if self.game.BACK_KEY:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('sounds/gimn_ukrani_-_gimn_ukrani_(z3.fm).mp3')  # Use the same file for music playback
                self.game.cur_menu = self.game.main_menu
                self.run_display = False
            self.blit_screen()
            self.game.display.blit(self.game.BG_CREDITS, (0, 0))
            self.game.draw_text_main_white_custom('Credits', 30, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 200)

            self.game.draw_text_main_for_credits('Ой на Горі тай Женці жнуть', 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 150)
            self.game.draw_text_main_for_credits('А попід Горою яром долиною Козаки йдуть', 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 120)
            self.game.draw_text_main_for_credits('Гей долиною гей широкою Козаки йдуть', 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 90)
            self.game.draw_text_main_for_credits('Попереду Дорошенко', 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 - 30)
            self.game.draw_text_main_for_credits('Веде своє військо військо запорізьке хорошенько', 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2)
            self.game.draw_text_main_for_credits('Гей долиною гей широкою хорошенько !', 20, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 + 30)


            self.game.draw_text_main_white_custom('SLAVA UKRAINE', 25, self.game.SCREEN_WIDTH / 2, self.game.SCREEN_HEIGHT / 2 + 80)

