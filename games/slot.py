# -*- coding: utf-8 -*-
"""Hedelmäpeli (slot machine) – kolme rullaa, vedä vipu (pelaa)."""

import random
import pygame

import config
from ui import draw_text, draw_button, draw_credits_bar


# Symbolit tekstinä (Pygame default font ei tue emojeja)
SYMBOLS = ["CHER", "LEM", "ORA", "GRAP", "GEM", "7"]
PAYOUT = {
    "7": 10,
    "GEM": 5,
    "GRAP": 4,
    "ORA": 3,
    "LEM": 2,
    "CHER": 2,
}


class SlotGame:
    def __init__(self, screen, clock, fonts):
        self.screen = screen
        self.clock = clock
        self.fonts = fonts
        self.bet = config.MIN_BET
        self.reels = [random.choice(SYMBOLS) for _ in range(3)]
        self.spinning = False
        self.spin_frame = 0
        self.result_message = ""
        self.result_timer = 0

    def run(self, credits):
        """Pelin pääsilmukka. Palauttaa päivitetyn credit-määrän."""
        play_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 100, 380, 200, 50)
        back_rect = pygame.Rect(20, config.SCREEN_HEIGHT - 60, 120, 40)

        while True:
            dt = self.clock.tick(30) / 1000.0
            mouse_pos = pygame.mouse.get_pos()

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
                        self.spin(credits)

            if self.spinning:
                self.spin_frame += 1
                if self.spin_frame <= 20:
                    self.reels = [random.choice(SYMBOLS) for _ in range(3)]
                else:
                    self.spinning = False
                    self.reels = [random.choice(SYMBOLS) for _ in range(3)]
                    win = self._check_win()
                    if win > 0:
                        credits += win
                        self.result_message = f"VOITTO: {win}!"
                    else:
                        self.result_message = "Ei voittoa"
                    self.result_timer = 90  # ~3 s

            if self.result_timer > 0:
                self.result_timer -= 1

            # Piirto
            self.screen.fill(config.COLOR_BG)
            bar_h = draw_credits_bar(self.screen, credits, self.fonts)

            draw_text(
                self.screen, "HEDELMÄPELI",
                config.SCREEN_WIDTH // 2, bar_h + 25,
                self.fonts["title"], config.COLOR_ACCENT, center=True
            )
            draw_text(
                self.screen, f"Panos: {self.bet}",
                config.SCREEN_WIDTH // 2, bar_h + 65,
                self.fonts["normal"], config.COLOR_TEXT_DIM, center=True
            )

            # Rullat (iso fontti symbolille – käytä normal/suurta)
            slot_w = 120
            slot_h = 100
            start_x = (config.SCREEN_WIDTH - 3 * slot_w - 40) // 2
            for i, sym in enumerate(self.reels):
                rx = start_x + i * (slot_w + 20)
                ry = 180
                rect = pygame.Rect(rx, ry, slot_w, slot_h)
                pygame.draw.rect(self.screen, (40, 40, 55), rect)
                pygame.draw.rect(self.screen, config.COLOR_ACCENT, rect, 2)
                # Symboli tekstinä (emoji voi näkyä fontista riippuen)
                draw_text(self.screen, sym, rx + slot_w // 2, ry + slot_h // 2 - 15,
                          self.fonts["title"], config.COLOR_TEXT, center=True)

            if self.result_timer > 0 and self.result_message:
                color = config.COLOR_WIN if "VOITTO" in self.result_message else config.COLOR_TEXT
                draw_text(
                    self.screen, self.result_message,
                    config.SCREEN_WIDTH // 2, 300,
                    self.fonts["menu"], color, center=True
                )

            if not self.spinning and credits >= self.bet:
                draw_button(self.screen, play_rect, "PELAA", self.fonts["menu"],
                            play_rect.collidepoint(mouse_pos))
            else:
                draw_button(self.screen, play_rect, "PELAA" if self.spinning else "Lisää credittejä",
                            self.fonts["menu"], False)

            draw_button(self.screen, back_rect, "Takaisin", self.fonts["small"],
                        back_rect.collidepoint(mouse_pos))

            pygame.display.flip()
        return credits

    def spin(self, credits):
        self.spinning = True
        self.spin_frame = 0
        self.result_message = ""
        self.result_timer = 0

    def _check_win(self):
        if self.reels[0] == self.reels[1] == self.reels[2]:
            return self.bet * PAYOUT.get(self.reels[0], 1)
        return 0
