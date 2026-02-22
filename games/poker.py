# -*- coding: utf-8 -*-
"""Video Poker (Jacks or Better) – yksinkertaistettu 5 korttia, pidä/vaihda."""

import random
import pygame

import config
from ui import draw_text, draw_button, draw_credits_bar


RANKS = "A 2 3 4 5 6 7 8 9 10 J Q K".split()
# Yksi merkki per maa (Pygame default font ei tue unicode-kuvioita)
SUITS = ["S", "H", "D", "C"]  # Spade, Heart, Diamond, Club
SUIT_COLORS = {"S": (200, 200, 200), "H": (220, 80, 80), "D": (220, 80, 80), "C": (200, 200, 200)}
SUIT_NAMES = {"S": "Pata", "H": "Hertta", "D": "Ruutu", "C": "Risti"}

# Jacks or Better -kertoimet (1 panos)
PAYTABLE = {
    "Royal Flush": 250,
    "Straight Flush": 50,
    "Four of a Kind": 25,
    "Full House": 9,
    "Flush": 6,
    "Straight": 4,
    "Three of a Kind": 3,
    "Two Pair": 2,
    "Jacks or Better": 1,
}


def make_deck():
    deck = []
    for r in RANKS:
        for s in SUITS:
            deck.append((r, s))
    random.shuffle(deck)
    return deck


def eval_hand(cards):
    """Arvioi 5 kortin pokerikäsi. Palauttaa (käsi_nimi, kertoin)."""
    rank_vals = {r: i for i, r in enumerate(RANKS)}
    ranks = [rank_vals[c[0]] for c in cards]
    suits = [c[1] for c in cards]
    ranks.sort()

    is_flush = len(set(suits)) == 1
    is_straight = False
    if len(set(ranks)) == 5:
        if ranks[4] - ranks[0] == 4:
            is_straight = True
        if ranks == [0, 1, 2, 3, 12]:  # A-2-3-4-5
            is_straight = True

    counts = {}
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1
    vals = sorted(counts.values(), reverse=True)

    if is_straight and is_flush:
        if ranks[4] == 12 and ranks[3] == 11:  # royal
            return "Royal Flush", PAYTABLE["Royal Flush"]
        return "Straight Flush", PAYTABLE["Straight Flush"]
    if vals[0] == 4:
        return "Four of a Kind", PAYTABLE["Four of a Kind"]
    if vals[0] == 3 and vals[1] == 2:
        return "Full House", PAYTABLE["Full House"]
    if is_flush:
        return "Flush", PAYTABLE["Flush"]
    if is_straight:
        return "Straight", PAYTABLE["Straight"]
    if vals[0] == 3:
        return "Three of a Kind", PAYTABLE["Three of a Kind"]
    if vals[0] == 2 and vals[1] == 2:
        return "Two Pair", PAYTABLE["Two Pair"]
    # Jacks or Better = pari J, Q, K tai A
    for r, count in counts.items():
        if count == 2 and r >= 9:  # 9=10, 10=J, 11=Q, 12=K, 0=A
            return "Jacks or Better", PAYTABLE["Jacks or Better"]
    return None, 0


class PokerGame:
    def __init__(self, screen, clock, fonts):
        self.screen = screen
        self.clock = clock
        self.fonts = fonts
        self.bet = config.MIN_BET
        self.deck = []
        self.hand = []
        self.held = [False] * 5
        self.phase = "deal"   # deal -> hold -> draw -> result
        self.result_text = ""
        self.win_amount = 0
        self.result_timer = 0

    def run(self, credits):
        if credits < self.bet:
            return credits
        credits -= self.bet
        self.deck = make_deck()
        self.hand = [self.deck.pop() for _ in range(5)]
        self.held = [False] * 5
        self.phase = "hold"
        self.result_text = "Pidä kortit (klikkaa) ja paina VAIHDA"
        self.win_amount = 0
        self.result_timer = 0

        back_rect = pygame.Rect(20, config.SCREEN_HEIGHT - 60, 120, 40)
        action_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 80, config.SCREEN_HEIGHT - 60, 160, 40)
        new_game_rect = pygame.Rect(config.SCREEN_WIDTH // 2 - 100, config.SCREEN_HEIGHT - 60, 200, 40)

        while True:
            self.clock.tick(30)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return credits
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return credits
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if back_rect.collidepoint(mouse_pos):
                        return credits
                    if self.phase == "finished":
                        if new_game_rect.collidepoint(mouse_pos) and credits >= self.bet:
                            credits -= self.bet
                            self.deck = make_deck()
                            self.hand = [self.deck.pop() for _ in range(5)]
                            self.held = [False] * 5
                            self.phase = "hold"
                            self.result_text = "Pidä kortit (klikkaa) ja paina VAIHDA"
                            self.win_amount = 0
                            self.result_timer = 0
                        elif back_rect.collidepoint(mouse_pos):
                            return credits
                    elif self.phase == "hold" and action_rect.collidepoint(mouse_pos):
                        # Vaihda ei-pidetyt
                        for i in range(5):
                            if not self.held[i]:
                                self.hand[i] = self.deck.pop()
                        hand_name, mult = eval_hand(self.hand)
                        self.win_amount = self.bet * mult if mult else 0
                        credits += self.win_amount
                        self.result_text = f"{hand_name}: +{self.win_amount}" if hand_name else "Ei voittoa"
                        self.phase = "result"
                        self.result_timer = 120
                    elif self.phase == "hold":
                        # Toggle hold kortille
                        card_w = 70
                        start_x = (config.SCREEN_WIDTH - 5 * card_w - 4 * 10) // 2
                        for i in range(5):
                            rx = start_x + i * (card_w + 10)
                            if 200 <= mouse_pos[1] <= 200 + 100 and rx <= mouse_pos[0] <= rx + card_w:
                                self.held[i] = not self.held[i]
                                break

            if self.result_timer > 0:
                self.result_timer -= 1
                if self.result_timer == 0:
                    self.phase = "finished"  # Näytetään Uusi peli / Takaisin

            self.screen.fill(config.COLOR_BG)
            bar_h = draw_credits_bar(self.screen, credits, self.fonts)

            draw_text(
                self.screen, "POKERI (Jacks or Better)",
                config.SCREEN_WIDTH // 2, bar_h + 25,
                self.fonts["title"], config.COLOR_ACCENT, center=True
            )
            draw_text(
                self.screen, self.result_text,
                config.SCREEN_WIDTH // 2, 140,
                self.fonts["normal"], config.COLOR_WIN if self.win_amount else config.COLOR_TEXT,
                center=True
            )

            card_w, card_h = 70, 100
            start_x = (config.SCREEN_WIDTH - 5 * card_w - 4 * 10) // 2
            for i, (r, s) in enumerate(self.hand):
                rx = start_x + i * (card_w + 10)
                ry = 180
                rect = pygame.Rect(rx, ry, card_w, card_h)
                col = (60, 70, 90) if self.held[i] else (50, 50, 65)
                pygame.draw.rect(self.screen, col, rect)
                pygame.draw.rect(self.screen, config.COLOR_ACCENT if self.held[i] else (100, 100, 120), rect, 2)
                draw_text(self.screen, r, rx + card_w // 2, ry + 25, self.fonts["small"], config.COLOR_TEXT, center=True)
                draw_text(self.screen, s, rx + card_w // 2, ry + 50, self.fonts["normal"], SUIT_COLORS.get(s, (200,200,200)), center=True)
                if self.held[i]:
                    draw_text(self.screen, "PIDETTY", rx + card_w // 2, ry + 82, self.fonts["small"], config.COLOR_ACCENT, center=True)

            if self.phase == "hold":
                draw_button(self.screen, action_rect, "VAIHDA", self.fonts["menu"],
                            action_rect.collidepoint(mouse_pos))
            elif self.phase == "finished":
                draw_button(self.screen, new_game_rect, "Uusi peli", self.fonts["menu"],
                            new_game_rect.collidepoint(mouse_pos) and credits >= self.bet)
            draw_button(self.screen, back_rect, "Takaisin", self.fonts["small"],
                        back_rect.collidepoint(mouse_pos))

            pygame.display.flip()
        return credits
