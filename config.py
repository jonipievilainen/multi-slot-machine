# -*- coding: utf-8 -*-
"""Asetukset Raspberry Pi 3 -retro-uhkapelialustalle."""

# Näyttö (sopii 7" Pi-näytölle ja pienemmille)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FULLSCREEN = False  # True = kioski-tila Pi:llä, False = ikkuna (debug)

# Värit (retro CRT-tyyli)
COLOR_BG = (20, 20, 30)
COLOR_ACCENT = (255, 200, 50)   # kulta
COLOR_TEXT = (220, 220, 220)
COLOR_TEXT_DIM = (120, 120, 120)
COLOR_BUTTON = (60, 60, 80)
COLOR_BUTTON_HOVER = (90, 90, 110)
COLOR_CREDITS = (80, 255, 120)
COLOR_WIN = (255, 215, 0)

# Pelit
MIN_BET = 1
DEFAULT_CREDITS_ADD = 10

# Fontit (Pygame käyttää oletusfontteja jos muita ei ole)
FONT_SIZE_TITLE = 48
FONT_SIZE_MENU = 32
FONT_SIZE_NORMAL = 24
FONT_SIZE_SMALL = 18
