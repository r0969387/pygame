
from settings import *

import pygame

def draw_text(text, size, x, y):
    font = pygame.font.Font(font_second_30, size)

    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect(center=(x, y))

    outline_color = black
    outline_thickness = 2

    for dx, dy in [(-outline_thickness, 0), (outline_thickness, 0), (0, -outline_thickness),
                   (0, outline_thickness),
                   (-outline_thickness, -outline_thickness), (outline_thickness, outline_thickness),
                   (-outline_thickness, outline_thickness), (outline_thickness, -outline_thickness)]:
        outline_surface = font.render(text, True, outline_color)
        outline_rect = outline_surface.get_rect(center=(x + dx, y + dy))
        screen.blit(outline_surface, outline_rect)
    screen.blit(text_surface, text_rect)


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