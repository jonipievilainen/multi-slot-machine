# -*- coding: utf-8 -*-
"""Asetukset – video poker / 80-luku arcade -tyyli (sininen näyttö, keltainen teksti)."""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FULLSCREEN = False

# Resoluutio: 1 = tarkka (ei skaalausta), 2 = pixel-art
PIXEL_SCALE = 1
SCANLINE_ALPHA = 18

# Video poker -tyyli: syvä sininen pelialue, keltainen teksti, vihreä/harmaa
COLOR_BG = (24, 28, 48)            # tumma kehys (musta-harmaa)
COLOR_SCREEN_BLUE = (20, 50, 130)  # pelin syvä sininen tausta
COLOR_BG_PANEL = (30, 60, 120)     # paneelit sinisellä
COLOR_TEXT = (255, 255, 255)        # valkoinen
COLOR_TEXT_YELLOW = (255, 255, 0)   # keltainen (otsikot, CASH)
COLOR_TEXT_DIM = (180, 180, 200)
COLOR_BUTTON_GREEN = (40, 140, 60)   # HOLD, DEAL
COLOR_BUTTON_GREEN_HOVER = (60, 180, 80)
COLOR_BUTTON_GREY = (80, 80, 90)     # ADD COIN, Takaisin
COLOR_BUTTON_GREY_HOVER = (110, 110, 120)
COLOR_CARD_BG = (220, 220, 230)      # kortin harmaa
COLOR_CARD_BORDER = (255, 255, 255)  # kortin valkoinen reuna
COLOR_CARD_HELD = (255, 255, 0)     # HOLD valittu (keltainen reuna)
COLOR_CREDITS = (255, 255, 0)       # CASH keltainen
COLOR_WIN = (255, 255, 0)
COLOR_PAYTABLE_HEADER = (255, 255, 255)
COLOR_PAYTABLE_HIGHLIGHT_BG = (120, 40, 40)  # 1 kolikko -sarake (tummanpunainen)
COLOR_PAYTABLE_TEXT = (255, 255, 200)
COLOR_BORDER = (255, 255, 255)

# Yhteensopivuus (vanhat nimet)
COLOR_ACCENT = COLOR_TEXT_YELLOW
COLOR_ACCENT2 = COLOR_BUTTON_GREEN
COLOR_ACCENT3 = COLOR_TEXT_YELLOW
COLOR_BUTTON = COLOR_BUTTON_GREY
COLOR_BUTTON_HOVER = COLOR_BUTTON_GREY_HOVER
COLOR_BORDER_ALT = COLOR_CARD_BORDER

MIN_BET = 1
DEFAULT_CREDITS_ADD = 10

# Fonttikoot natiiviresoluutiolla (800x480)
FONT_SIZE_TITLE = 42
FONT_SIZE_MENU = 28
FONT_SIZE_NORMAL = 22
FONT_SIZE_SMALL = 18

# Paytable-paneelin leveys (vasemmalla)
PAYTABLE_PANEL_WIDTH = 200

SHUFFLE_DURATION_FRAMES = 45
DEAL_DELAY_FRAMES = 8
SLOT_REEL_SPEED = 18
SLOT_STOP_DELAY = 15
