# -*- coding: utf-8 -*-
"""Video Poker (Jacks or Better) – paytable, HOLD-napit, klassinen arcade-tyyli."""

import random
import math
import pygame

import config
from ui import draw_text, draw_button, draw_button_hold, draw_credits_bar, draw_cash_big, draw_scanlines
from games import card_assets


RANKS = "A 2 3 4 5 6 7 8 9 10 J Q K".split()
SUITS = ["S", "H", "D", "C"]
SUIT_COLORS = {"S": (40, 40, 40), "H": (200, 50, 50), "D": (200, 50, 50), "C": (40, 40, 40)}

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

PAYTABLE_ORDER = [
    "Royal Flush", "Straight Flush", "Four of a Kind", "Full House", "Flush",
    "Straight", "Three of a Kind", "Two Pair", "Jacks or Better",
]


def make_deck():
    deck = []
    for r in RANKS:
        for s in SUITS:
            deck.append((r, s))
    random.shuffle(deck)
    return deck


def eval_hand(cards):
    rank_vals = {r: i for i, r in enumerate(RANKS)}
    ranks = [rank_vals[c[0]] for c in cards]
    suits = [c[1] for c in cards]
    ranks.sort()
    is_flush = len(set(suits)) == 1
    is_straight = False
    if len(set(ranks)) == 5:
        if ranks[4] - ranks[0] == 4:
            is_straight = True
        if ranks == [0, 1, 2, 3, 12]:
            is_straight = True
    counts = {}
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1
    vals = sorted(counts.values(), reverse=True)
    if is_straight and is_flush:
        if ranks[4] == 12 and ranks[3] == 11:
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
    for r, count in counts.items():
        if count == 2 and r >= 9:
            return "Jacks or Better", PAYTABLE["Jacks or Better"]
    return None, 0


def _draw_paytable_full(surface, fonts):
    """Paytable: vasen sarake kädet, oikealla 1-5 kolikon voitot."""
    pw = config.PAYTABLE_PANEL_WIDTH
    x, y = 8, 50
    draw_text(surface, "COINS WAGERED", x + pw // 2, y, fonts["small"], config.COLOR_PAYTABLE_HEADER, center=True)
    y += 20
    # Sarakkeet: käsi ~100px, sitten 1 2 3 4 5
    hand_w = 100
    col_w = 18
    start_col = x + hand_w
    for c in range(5):
        draw_text(surface, str(c + 1), start_col + c * col_w + col_w // 2, y, fonts["small"], config.COLOR_PAYTABLE_HEADER, center=True)
    y += 14
    for hand_name in PAYTABLE_ORDER:
        payout1 = PAYTABLE[hand_name]
        # 1-kolikko sarake korostus
        pygame.draw.rect(surface, config.COLOR_PAYTABLE_HIGHLIGHT_BG, (start_col, y - 2, col_w, 12))
        # Käden nimi (lyhennetty)
        short = hand_name.replace(" of a Kind", "").replace(" or Better", "").replace(" ", " ")
        if len(short) > 12:
            short = short[:10] + ".."
        draw_text(surface, short, x + 4, y - 1, fonts["small"], config.COLOR_PAYTABLE_TEXT)
        for c in range(5):
            val = payout1 * (c + 1)
            draw_text(surface, str(val), start_col + c * col_w + col_w // 2, y - 1, fonts["small"], config.COLOR_PAYTABLE_TEXT, center=True)
        y += 14


def _draw_card(surface, x, y, card_w, card_h, rank, suit, fonts, face_up=True, highlight=False):
    """Piirtää kortin: SVG-kuva tai fallback (selkä). Ei uudelleenjakoefektiä vaihdon yhteydessä."""
    if face_up and rank and suit:
        img = card_assets.load_card_surface(rank, suit, card_w, card_h)
        if img is not None:
            surface.blit(img, (x, y))
        else:
            pygame.draw.rect(surface, config.COLOR_CARD_BG, (x, y, card_w, card_h))
            draw_text(surface, rank, x + card_w // 2, y + 18, fonts["small"], (30, 30, 30), center=True, pixel_scale=config.PIXEL_SCALE)
            draw_text(surface, suit, x + card_w // 2, y + 38, fonts["normal"], SUIT_COLORS.get(suit, (50, 50, 50)), center=True, pixel_scale=config.PIXEL_SCALE)
    else:
        back = card_assets.load_card_back_surface(card_w, card_h)
        surface.blit(back, (x, y))
    border_col = config.COLOR_CARD_HELD if highlight else config.COLOR_CARD_BORDER
    pygame.draw.rect(surface, border_col, (x, y, card_w, card_h), 2)


class PokerGame:
    def __init__(self, screen, clock, fonts):
        self.screen = screen
        self.clock = clock
        self.fonts = fonts
        self.bet = config.MIN_BET
        self.deck = []
        self.hand = []
        self.held = [False] * 5
        self.phase = "shuffle"
        self.result_text = ""
        self.win_amount = 0
        self.result_timer = 0
        self.shuffle_frame = 0
        self.deal_frame = 0
        self.card_w = 80
        self.card_h = 112
        self.slot_positions = []
        self.deck_pos = (0, 0)
        self.hold_rects = []
        self.game_left = config.PAYTABLE_PANEL_WIDTH
        self.game_width = config.SCREEN_WIDTH - self.game_left

    def _get_slot_positions(self):
        start_x = self.game_left + (self.game_width - 5 * self.card_w - 4 * 8) // 2
        return [(start_x + i * (self.card_w + 8), 168) for i in range(5)]

    def _get_hold_rects(self):
        return [
            pygame.Rect(self.slot_positions[i][0], self.slot_positions[i][1] + self.card_h + 4, self.card_w, 28)
            for i in range(5)
        ]

    def _get_deck_pos(self):
        cx = self.game_left + self.game_width // 2 - self.card_w // 2 - 16
        return (cx, 52)

    def run(self, credits):
        if credits < self.bet:
            return credits
        credits -= self.bet
        self.deck = make_deck()
        self.hand = [self.deck.pop() for _ in range(5)]
        self.held = [False] * 5
        self.phase = "shuffle"
        self.result_text = ""
        self.win_amount = 0
        self.result_timer = 0
        self.shuffle_frame = 0
        self.deal_frame = 0
        self.slot_positions = self._get_slot_positions()
        self.hold_rects = self._get_hold_rects()
        self.deck_pos = self._get_deck_pos()

        bottom_y = config.SCREEN_HEIGHT - 52
        back_rect = pygame.Rect(self.game_left + 20, bottom_y, 100, 36)
        action_rect = pygame.Rect(config.SCREEN_WIDTH - 120, bottom_y, 100, 36)
        new_game_rect = pygame.Rect(config.SCREEN_WIDTH - 120, bottom_y, 100, 36)
        cash_center_x = self.game_left + self.game_width // 2

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
                            self.phase = "shuffle"
                            self.result_text = ""
                            self.win_amount = 0
                            self.result_timer = 0
                            self.shuffle_frame = 0
                            self.deal_frame = 0
                        elif back_rect.collidepoint(mouse_pos):
                            return credits
                    elif self.phase == "hold" and action_rect.collidepoint(mouse_pos):
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
                        for i in range(5):
                            if self.hold_rects[i].collidepoint(mouse_pos):
                                self.held[i] = not self.held[i]
                                break

            if self.phase == "shuffle":
                self.shuffle_frame += 1
                if self.shuffle_frame >= config.SHUFFLE_DURATION_FRAMES:
                    self.phase = "dealing"
                    self.deal_frame = 0
            elif self.phase == "dealing":
                self.deal_frame += 1
                total_deal_frames = 5 * config.DEAL_DELAY_FRAMES
                if self.deal_frame >= total_deal_frames:
                    self.phase = "hold"
                    self.result_text = "Valitse HOLD ja paina DEAL"

            if self.result_timer > 0:
                self.result_timer -= 1
                if self.result_timer == 0:
                    self.phase = "finished"

            # Tausta: kehys + sininen pelialue
            self.screen.fill(config.COLOR_BG)
            pygame.draw.rect(self.screen, config.COLOR_SCREEN_BLUE, (self.game_left, 0, self.game_width, config.SCREEN_HEIGHT))
            bar_h = draw_credits_bar(self.screen, credits, self.fonts)

            _draw_paytable_full(self.screen, self.fonts)

            # Oikealla ylhäällä: COIN VALUE, WAGER
            wx = config.SCREEN_WIDTH - 100
            draw_text(self.screen, "COIN VALUE", wx, bar_h + 8, self.fonts["small"], config.COLOR_TEXT_YELLOW)
            draw_text(self.screen, str(self.bet), wx, bar_h + 24, self.fonts["normal"], config.COLOR_TEXT_YELLOW)
            draw_text(self.screen, "WAGER", wx, bar_h + 44, self.fonts["small"], config.COLOR_TEXT_YELLOW)
            draw_text(self.screen, str(self.bet), wx, bar_h + 60, self.fonts["normal"], config.COLOR_TEXT_YELLOW)

            if self.phase not in ("shuffle", "dealing"):
                draw_text(
                    self.screen, self.result_text,
                    cash_center_x, 128,
                    self.fonts["normal"], config.COLOR_WIN if self.win_amount else config.COLOR_TEXT,
                    center=True
                )

            dx, dy = self.deck_pos
            if self.phase == "shuffle":
                wobble = 4 * math.sin(self.shuffle_frame * 0.35)
                for i in range(5):
                    _draw_card(self.screen, int(dx + wobble + i * 2), dy + i * 2, self.card_w, self.card_h, None, None, self.fonts, face_up=False)
                draw_text(self.screen, "Sekoitetaan...", cash_center_x, dy + self.card_h + 6,
                          self.fonts["small"], config.COLOR_TEXT_DIM, center=True)
            elif self.phase == "dealing":
                cards_left = 5 - min(5, (self.deal_frame + config.DEAL_DELAY_FRAMES - 1) // config.DEAL_DELAY_FRAMES)
                for i in range(cards_left):
                    _draw_card(self.screen, dx + i * 2, dy + i * 2, self.card_w, self.card_h, None, None, self.fonts, face_up=False)
                for i in range(5):
                    slot_x, slot_y = self.slot_positions[i]
                    start_f = i * config.DEAL_DELAY_FRAMES
                    end_f = (i + 1) * config.DEAL_DELAY_FRAMES
                    if self.deal_frame >= end_f:
                        _draw_card(self.screen, slot_x, slot_y, self.card_w, self.card_h,
                                   self.hand[i][0], self.hand[i][1], self.fonts, highlight=self.held[i])
                    else:
                        t = (self.deal_frame - start_f) / config.DEAL_DELAY_FRAMES
                        t = t * t
                        cx = int(dx + 2 + (slot_x - (dx + 2)) * t)
                        cy = int(dy + 2 + (slot_y - (dy + 2)) * t)
                        _draw_card(self.screen, cx, cy, self.card_w, self.card_h,
                                   self.hand[i][0], self.hand[i][1], self.fonts)
            else:
                for i, (r, s) in enumerate(self.hand):
                    rx, ry = self.slot_positions[i]
                    _draw_card(self.screen, rx, ry, self.card_w, self.card_h, r, s, self.fonts, highlight=self.held[i])

            # HOLD-napit korttien alla
            if self.phase in ("hold", "result", "finished"):
                for i in range(5):
                    draw_button_hold(self.screen, self.hold_rects[i], "HOLD", self.fonts["small"],
                                    active=self.held[i], hover=self.hold_rects[i].collidepoint(mouse_pos))

            # Alaosa: Takaisin | CASH | DEAL / Uusi peli
            draw_cash_big(self.screen, credits, self.fonts, cash_center_x, bottom_y - 8)
            if self.phase == "hold":
                draw_button(self.screen, action_rect, "DEAL", self.fonts["menu"],
                            action_rect.collidepoint(mouse_pos), style="green")
            elif self.phase == "finished":
                draw_button(self.screen, new_game_rect, "DEAL", self.fonts["menu"],
                            new_game_rect.collidepoint(mouse_pos) and credits >= self.bet, style="green")
            draw_button(self.screen, back_rect, "EXIT", self.fonts["small"],
                        back_rect.collidepoint(mouse_pos), style="grey")

            if config.SCANLINE_ALPHA > 0:
                draw_scanlines(self.screen)
            pygame.display.flip()
        return credits
