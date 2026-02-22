# -*- coding: utf-8 -*-
"""Yhteinen UI-apuri: piirto, fontit, napot."""

import pygame
import sys

import config


def init_display():
    """Alustaa näytön (tukee Pi framebufferia)."""
    import os
    if sys.platform == "linux" and os.path.exists("/dev/fb0"):
        try:
            os.putenv("SDL_VIDEODRIVER", "fbcon")
            os.putenv("SDL_FBDEV", "/dev/fb0")
        except Exception:
            pass
    pygame.display.init()
    if config.FULLSCREEN:
        flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), flags)
    else:
        screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Retro Uhkapeli")
    pygame.mouse.set_visible(True)
    return screen


def get_fonts():
    """Palauttaa fontit (yrittää käyttää oletusfonttia)."""
    pygame.font.init()
    return {
        "title": pygame.font.Font(None, config.FONT_SIZE_TITLE),
        "menu": pygame.font.Font(None, config.FONT_SIZE_MENU),
        "normal": pygame.font.Font(None, config.FONT_SIZE_NORMAL),
        "small": pygame.font.Font(None, config.FONT_SIZE_SMALL),
    }


def draw_text(surface, text, x, y, font, color=config.COLOR_TEXT, center=False):
    """Piirtää tekstiä. center=True keskitetään x,y."""
    img = font.render(str(text), True, color)
    if center:
        x -= img.get_width() // 2
    surface.blit(img, (x, y))
    return img.get_rect(topleft=(x, y))


def draw_button(surface, rect, text, font, hover=False):
    """Piirtää napon ja palauttaa rect."""
    color = config.COLOR_BUTTON_HOVER if hover else config.COLOR_BUTTON
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, config.COLOR_ACCENT, rect, 2)
    cx = rect.centerx
    cy = rect.centery
    img = font.render(str(text), True, config.COLOR_TEXT)
    surface.blit(img, (cx - img.get_width() // 2, cy - img.get_height() // 2))
    return rect


def draw_credits_bar(surface, credits, fonts):
    """Piirtää credit-palkin yläreunaan."""
    h = 40
    pygame.draw.rect(surface, (30, 30, 40), (0, 0, config.SCREEN_WIDTH, h))
    pygame.draw.line(surface, config.COLOR_ACCENT, (0, h), (config.SCREEN_WIDTH, h), 2)
    text = f"CREDITS: {credits}"
    draw_text(surface, text, 20, 8, fonts["normal"], config.COLOR_CREDITS)
    return h
