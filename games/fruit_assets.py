# -*- coding: utf-8 -*-
"""Hedelmäkuvien lataus 10_fruit_icons -kansiosta."""

import os

import pygame

SYMBOLS = ["CHER", "LEM", "ORA", "GRAP", "GEM", "7"]
# set1_01.png ... set1_06.png vastaavat CHER, LEM, ORA, GRAP, GEM, 7
_IMAGE_CACHE = {}
_ICONS_DIR = None


def _icons_dir():
    global _ICONS_DIR
    if _ICONS_DIR is None:
        _ICONS_DIR = os.path.join(os.path.dirname(__file__), "10_fruit_icons")
    return _ICONS_DIR


def load_fruit_surface(symbol, width, height):
    """Lataa yhden symbolin kuvan skaalattuna. symbol in SYMBOLS."""
    key = (symbol, width, height)
    if key in _IMAGE_CACHE:
        return _IMAGE_CACHE[key]
    idx = SYMBOLS.index(symbol) if symbol in SYMBOLS else 0
    path = os.path.join(_icons_dir(), f"set1_{idx + 1:02d}.png")
    if not os.path.isfile(path):
        return None
    try:
        img = pygame.image.load(path).convert_alpha()
        surf = pygame.transform.smoothscale(img, (width, height))
        _IMAGE_CACHE[key] = surf
        return surf
    except Exception:
        return None
