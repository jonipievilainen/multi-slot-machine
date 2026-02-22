# -*- coding: utf-8 -*-
"""Korttikuvausten lataus SVG-cards-1.3 -kansiosta."""

import os
from io import BytesIO

import pygame

# RANKS / SUITS vastaavat poker.py
RANKS = "A 2 3 4 5 6 7 8 9 10 J Q K".split()
SUITS = ["S", "H", "D", "C"]
# Tiedostonimet: rank_of_suit.svg (ace, 2..10, jack, queen, king ja spades, hearts, diamonds, clubs)
RANK_TO_NAME = {
    "A": "ace", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6",
    "7": "7", "8": "8", "9": "9", "10": "10", "J": "jack", "Q": "queen", "K": "king",
}
SUIT_TO_NAME = {"S": "spades", "H": "hearts", "D": "diamonds", "C": "clubs"}

_CARD_CACHE = {}
_CARDS_DIR = None


def _cards_dir():
    global _CARDS_DIR
    if _CARDS_DIR is None:
        _CARDS_DIR = os.path.join(os.path.dirname(__file__), "SVG-cards-1.3")
    return _CARDS_DIR


def _svg_path(rank, suit):
    r = RANK_TO_NAME.get(rank, "ace")
    s = SUIT_TO_NAME.get(suit, "spades")
    base = f"{r}_of_{s}"
    path1 = os.path.join(_cards_dir(), f"{base}.svg")
    if os.path.isfile(path1):
        return path1
    path2 = os.path.join(_cards_dir(), f"{base}2.svg")
    return path2 if os.path.isfile(path2) else path1


def load_card_surface(rank, suit, width, height):
    """Lataa yhden kortin pygame-Surface (width x height). Käyttää cairosvg."""
    key = (rank, suit, width, height)
    if key in _CARD_CACHE:
        return _CARD_CACHE[key]
    path = _svg_path(rank, suit)
    try:
        import cairosvg
        buf = BytesIO()
        cairosvg.svg2png(url=path, output_width=width, output_height=height, write_to=buf)
        buf.seek(0)
        surf = pygame.image.load(buf).convert_alpha()
        _CARD_CACHE[key] = surf
        return surf
    except Exception:
        return None


_BACK_CACHE = {}


def load_card_back_surface(width, height):
    """Piirrettävä kortin selkä (yksinkertainen)."""
    key = (width, height)
    if key in _BACK_CACHE:
        return _BACK_CACHE[key]
    surf = pygame.Surface((width, height))
    surf.fill((40, 60, 100))
    for x in range(0, width, 10):
        for y in range(0, height, 10):
            pygame.draw.rect(surf, (60, 80, 120), (x + 1, y + 1, 6, 6))
    pygame.draw.rect(surf, (255, 255, 255), (0, 0, width, height), 2)
    _BACK_CACHE[key] = surf
    return surf
