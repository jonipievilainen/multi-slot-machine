# -*- coding: utf-8 -*-
"""Yhteinen UI: video poker -tyyli (sininen, keltainen, vihreä/harmaa)."""

import pygame
import sys

import config


def init_display():
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
    pygame.font.init()
    return {
        "title": pygame.font.Font(None, config.FONT_SIZE_TITLE),
        "menu": pygame.font.Font(None, config.FONT_SIZE_MENU),
        "normal": pygame.font.Font(None, config.FONT_SIZE_NORMAL),
        "small": pygame.font.Font(None, config.FONT_SIZE_SMALL),
    }


def _scale_surface(surf, scale):
    if scale <= 1:
        return surf
    w, h = surf.get_size()
    return pygame.transform.scale(surf, (w * scale, h * scale))


def draw_text(surface, text, x, y, font, color=config.COLOR_TEXT, center=False, pixel_scale=None):
    if pixel_scale is None:
        pixel_scale = config.PIXEL_SCALE
    img = font.render(str(text), True, color)
    if pixel_scale > 1:
        img = _scale_surface(img, pixel_scale)
    if center:
        x -= img.get_width() // 2
    surface.blit(img, (x, y))
    return img.get_rect(topleft=(x, y))


def draw_button(surface, rect, text, font, hover=False, style="green"):
    """style: 'green' (DEAL/HOLD) tai 'grey' (ADD COIN, Takaisin)."""
    if style == "green":
        color = config.COLOR_BUTTON_GREEN_HOVER if hover else config.COLOR_BUTTON_GREEN
        text_color = config.COLOR_TEXT
    else:
        color = config.COLOR_BUTTON_GREY_HOVER if hover else config.COLOR_BUTTON_GREY
        text_color = config.COLOR_TEXT
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, config.COLOR_BORDER, rect, 2)
    img = font.render(str(text), True, text_color)
    img = _scale_surface(img, config.PIXEL_SCALE)
    cx = rect.centerx - img.get_width() // 2
    cy = rect.centery - img.get_height() // 2
    surface.blit(img, (cx, cy))
    return rect


def draw_button_hold(surface, rect, text, font, active=False, hover=False):
    """HOLD-nappi: vihreä, keltainen reuna kun aktiivinen."""
    color = config.COLOR_BUTTON_GREEN_HOVER if hover else config.COLOR_BUTTON_GREEN
    pygame.draw.rect(surface, color, rect)
    border_col = config.COLOR_CARD_HELD if active else config.COLOR_BORDER
    pygame.draw.rect(surface, border_col, rect, 3)
    img = font.render(str(text), True, config.COLOR_TEXT)
    img = _scale_surface(img, config.PIXEL_SCALE)
    cx = rect.centerx - img.get_width() // 2
    cy = rect.centery - img.get_height() // 2
    surface.blit(img, (cx, cy))
    return rect


def draw_credits_bar(surface, credits, fonts):
    """Yläpalkki: tumma, CASH keltainen."""
    h = 44
    pygame.draw.rect(surface, config.COLOR_BG, (0, 0, config.SCREEN_WIDTH, h))
    pygame.draw.line(surface, config.COLOR_BORDER, (0, h), (config.SCREEN_WIDTH, h), 2)
    draw_text(surface, f"CASH  {credits}", 24, 10, fonts["normal"], config.COLOR_TEXT_YELLOW, pixel_scale=config.PIXEL_SCALE)
    return h


def draw_cash_big(surface, credits, fonts, center_x, y):
    """Iso keltainen CASH-näyttö (pelin alaosa)."""
    text = f"CASH  {credits}"
    draw_text(surface, text, center_x, y, fonts["title"], config.COLOR_TEXT_YELLOW, center=True)

def draw_scanlines(surface, alpha=None):
    if alpha is None:
        alpha = config.SCANLINE_ALPHA
    if alpha <= 0:
        return
    w, h = surface.get_size()
    sl = pygame.Surface((w, h))
    sl.set_alpha(alpha)
    for y in range(0, h, 4):
        pygame.draw.line(sl, (0, 0, 0), (0, y), (w, y), 1)
    surface.blit(sl, (0, 0))
