# -*- coding: utf-8 -*-
"""Hedelmäpeli (slot) – visuaaliset pyörivät rullat, 80-luku pixel-tyyli."""

import random
import pygame

import config
from ui import draw_text, draw_button, draw_credits_bar, draw_scanlines
from games import fruit_assets


SYMBOLS = ["CHER", "LEM", "ORA", "GRAP", "GEM", "7"]
PAYOUT = {"7": 10, "GEM": 5, "GRAP": 4, "ORA": 3, "LEM": 2, "CHER": 2}

# Rullan korkeus yhdelle symbolille (pikseliä)
SYMBOL_HEIGHT = 72
# Kuinka monta symbolia rullassa (toistuu)
REEL_LENGTH = 20
# Näkyvissä 3 symbolia per rulla (keskimmäinen = tulos)
VISIBLE_SYMBOLS = 3


def _build_reel_strip(final_symbol):
    """Rulla jossa final_symbol on varmasti jossain (indeksissä REEL_LENGTH//2)."""
    strip = [random.choice(SYMBOLS) for _ in range(REEL_LENGTH)]
    strip[REEL_LENGTH // 2] = final_symbol
    return strip


class SlotGame:
    def __init__(self, screen, clock, fonts):
        self.screen = screen
        self.clock = clock
        self.fonts = fonts
        self.bet = config.MIN_BET
        self.reels = [random.choice(SYMBOLS) for _ in range(3)]
        self.reel_strips = [_build_reel_strip(s) for s in self.reels]
        self.reel_offsets = [0.0, 0.0, 0.0]  # symboli-indeksi (float), pyörii
        self.reel_speeds = [0.0, 0.0, 0.0]
        self.stopped = [True, True, True]
        self.stop_started = [False, False, False]  # pysaytys kaynnistyy perakkain
        self.spinning = False
        self.result_message = ""
        self.result_timer = 0
        self.stop_frame = 0
        self.slot_w = 110
        self.slot_h = SYMBOL_HEIGHT * VISIBLE_SYMBOLS
        self.reel_start_x = (config.SCREEN_WIDTH - 3 * self.slot_w - 2 * 16) // 2
        self.icon_w = self.slot_w - 12
        self.icon_h = SYMBOL_HEIGHT - 8

    def run(self, credits):
        play_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 100, 380, 200, 50)
        back_rect = pygame.Rect(20, config.SCREEN_HEIGHT - 60, 120, 40)

        while True:
            self.clock.tick(30)
            mouse_pos = pygame.mouse.get_pos()
            dt = 1.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return credits
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return credits
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_rect.collidepoint(mouse_pos):
                        return credits
                    if play_rect.collidepoint(mouse_pos) and not self.spinning and credits >= self.bet:
                        credits -= self.bet
                        self._start_spin()

            if self.spinning:
                self.stop_frame += 1
                for i in range(3):
                    if not self.stopped[i]:
                        self.reel_offsets[i] += self.reel_speeds[i]
                        if self.reel_offsets[i] >= REEL_LENGTH:
                            self.reel_offsets[i] -= REEL_LENGTH
                        # Pysaytys alkaa vain kun tämä rulla on vuorossa (rulla 0, sitten 1, sitten 2)
                        stop_at = [30, 30 + config.SLOT_STOP_DELAY, 30 + 2 * config.SLOT_STOP_DELAY]
                        if self.stop_frame >= stop_at[i]:
                            self.stop_started[i] = True
                        if self.stop_started[i]:
                            if self.reel_speeds[i] > 0.06:
                                self.reel_speeds[i] *= 0.90
                            else:
                                self.reel_speeds[i] = 0
                                self.reel_offsets[i] = REEL_LENGTH // 2 - 0.5  # keski = tulos
                                self.stopped[i] = True
                if all(self.stopped):
                    self.spinning = False
                    self.reels = [
                        self.reel_strips[i][(int(self.reel_offsets[i]) + 1) % REEL_LENGTH]
                        for i in range(3)
                    ]
                    win = self._check_win()
                    if win > 0:
                        credits += win
                        self.result_message = f"VOITTO: {win}!"
                    else:
                        self.result_message = "Ei voittoa"
                    self.result_timer = 90

            if self.result_timer > 0:
                self.result_timer -= 1

            self.screen.fill(config.COLOR_BG)
            pygame.draw.rect(self.screen, config.COLOR_SCREEN_BLUE, (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
            bar_h = draw_credits_bar(self.screen, credits, self.fonts)

            draw_text(
                self.screen, "HEDELMAPELI",
                config.SCREEN_WIDTH // 2, bar_h + 22,
                self.fonts["title"], config.COLOR_TEXT_YELLOW, center=True
            )
            draw_text(
                self.screen, f"Panos: {self.bet}",
                config.SCREEN_WIDTH // 2, bar_h + 58,
                self.fonts["normal"], config.COLOR_TEXT_DIM, center=True
            )

            # Kolme rullaa: ikkuna jossa symbolit liikkuvat (harmaa laatikko, valkoinen reuna)
            for r in range(3):
                rx = self.reel_start_x + r * (self.slot_w + 16)
                ry = 165
                pygame.draw.rect(self.screen, config.COLOR_CARD_BG, (rx, ry, self.slot_w, self.slot_h))
                pygame.draw.rect(self.screen, config.COLOR_CARD_BORDER, (rx, ry, self.slot_w, self.slot_h), 3)
                # Piirrä näkyvät symbolit (scroll) – hedelmäkuvat
                base = self.reel_offsets[r]
                for v in range(VISIBLE_SYMBOLS + 1):
                    idx = (int(base) + v) % REEL_LENGTH
                    sym = self.reel_strips[r][idx]
                    py_ = ry + v * SYMBOL_HEIGHT - (base % 1.0) * SYMBOL_HEIGHT
                    if py_ + SYMBOL_HEIGHT >= ry and py_ < ry + self.slot_h:
                        img = fruit_assets.load_fruit_surface(sym, self.icon_w, self.icon_h)
                        if img is not None:
                            ix = rx + (self.slot_w - self.icon_w) // 2
                            self.screen.blit(img, (ix, int(py_) + (SYMBOL_HEIGHT - self.icon_h) // 2))
                        else:
                            draw_text(
                                self.screen, sym,
                                rx + self.slot_w // 2, int(py_) + SYMBOL_HEIGHT // 2 - 12,
                                self.fonts["normal"], config.COLOR_TEXT, center=True
                            )

            if self.result_timer > 0 and self.result_message:
                color = config.COLOR_WIN if "VOITTO" in self.result_message else config.COLOR_TEXT
                draw_text(
                    self.screen, self.result_message,
                    config.SCREEN_WIDTH // 2, 305,
                    self.fonts["menu"], color, center=True
                )

            if not self.spinning and credits >= self.bet:
                draw_button(self.screen, play_rect, "PELAA", self.fonts["menu"],
                            play_rect.collidepoint(mouse_pos), style="green")
            else:
                draw_button(self.screen, play_rect,
                            "PELAA" if self.spinning else "Lisaa creditteja",
                            self.fonts["menu"], False, style="green")
            draw_button(self.screen, back_rect, "EXIT", self.fonts["small"],
                        back_rect.collidepoint(mouse_pos), style="grey")

            if config.SCANLINE_ALPHA > 0:
                draw_scanlines(self.screen)
            pygame.display.flip()
        return credits

    def _start_spin(self):
        self.reels = [random.choice(SYMBOLS) for _ in range(3)]
        self.reel_strips = [_build_reel_strip(s) for s in self.reels]
        self.reel_offsets = [0.0, 0.0, 0.0]
        self.reel_speeds = [config.SLOT_REEL_SPEED / SYMBOL_HEIGHT * 2] * 3
        self.stopped = [False, False, False]
        self.spinning = True
        self.result_message = ""
        self.result_timer = 0
        self.stop_started = [False, False, False]
        self.stop_frame = 0

    def _check_win(self):
        if self.reels[0] == self.reels[1] == self.reels[2]:
            return self.bet * PAYOUT.get(self.reels[0], 1)
        return 0
