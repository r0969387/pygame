'''     Settings for the game     '''
import pygame
import sys
from menu import *

from settings import *
import random

from pygame import mixer

pygame.mixer.pre_init(44100, -16, 4, 3072)
mixer.init()
pygame.init()
pygame.font.init()

# controlling condition of the game
game_started = False
'''Game over and win scenario, 0 - means no game_over,  1 - means player won and -1 means player lost'''
game_over = 0

clock = pygame.time.Clock()
fps = 60

screen_width = 1200
screen_height = 700

# define fonts
font_second_30 = 'fonts/8-BIT WONDER.TTF'


bg = pygame.image.load('images/rada_bg_for_game.png')


pygame.mixer.music.load('sounds/gimn_ukrani_-_gimn_ukrani_(z3.fm).mp3')
pygame.mixer.music.set_volume(0.15)

# sounds
pygame.mixer.music.load('sounds/music for game.mp3')
pygame.mixer.music.set_volume(0.1)

missile_sound = pygame.mixer.Sound('sounds/final_missile_sound.mp3')
missile_sound.set_volume(0.100)

explotion_sound = pygame.mixer.Sound('sounds/explosion_sound.wav')
explotion_sound.set_volume(0.3)

damage_sound = pygame.mixer.Sound('sounds/damage_sound.mp3')
damage_sound.set_volume(0.2)

revo_healing = pygame.mixer.Sound('sounds/revo_healing.mp3')
revo_healing.set_volume(0.5)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Invaders')

revo_red_sound = pygame.mixer.Sound('sounds/revo_red_sound.mp3')
revo_red_sound.set_volume(0.7)

bullets_boost_sound = pygame.mixer.Sound('sounds/america sound (1).mp3')
bullets_boost_sound.set_volume(0.9)

machine_gun = pygame.mixer.Sound('sounds/machine_gun.mp3')
machine_gun.set_volume(0.2)

music_game_loop = pygame.mixer.Sound('sounds/music for game_loop.mp3')
music_game_loop.set_volume(0.04)

red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)

alien_cooldown = 1500
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()

MAX_HEATLH = 20

points = 0  # points of dead russians

difficulty_timer = pygame.time.get_ticks()  # Timer to increase difficulty
difficulty_interval_aliens = 5000  # Increase difficulty every 2 seconds
difficulty_timer_revo_gray = pygame.time.get_ticks()
difficulty_interval_revo_gray = 30000
difficulty_timer_revo_red = pygame.time.get_ticks()
difficulty_interval_revo_red = 60000
difficulty_timer_boost = pygame.time.get_ticks()
difficulty_interval_boost = 60000



spaceship_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_bullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
revo_group = pygame.sprite.Group()
revo_red_group = pygame.sprite.Group()
bullets_boost_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
boss_bullets_group = pygame.sprite.Group()


num_aliens = 1
num_revo = 1
num_revo_red = 1
num_bullets_boost = 1

boss_spawned = False
boss_alive = True

points = 0


