# -*- coding: utf-8 -*-
"""
Retro uhkapelialusta – Raspberry Pi 3.
Käyttäjä lisää credittejä ja valitsee valikosta Pokerin tai hedelmäpelin (slot).
"""

import pygame
import sys

import config
from ui import init_display, get_fonts, draw_text, draw_button, draw_credits_bar, draw_scanlines


def run_main_menu(screen, clock, fonts):
    """Päävalikko: lisää credittejä, valitse Poker tai Slot."""
    credits = 0
    menu_items = [
        ("Lisää credittejä", "add"),
        ("POKERI", "poker"),
        ("HEDELMÄPELI (SLOT)", "slot"),
        ("Lopeta", "quit"),
    ]
    button_height = 50
    button_width = 400
    start_y = 120
    spacing = 60
    buttons = []
    for i, (label, key) in enumerate(menu_items):
        rect = pygame.Rect(
            (config.SCREEN_WIDTH - button_width) // 2,
            start_y + i * spacing,
            button_width,
            button_height,
        )
        buttons.append((rect, label, key))

    while True:
        # Tapahtumat
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, label, key in buttons:
                    if rect.collidepoint(mouse_pos):
                        if key == "add":
                            credits += config.DEFAULT_CREDITS_ADD
                        elif key == "poker":
                            if credits < config.MIN_BET:
                                continue  # ei riitä credittejä
                            from games.poker import PokerGame
                            game = PokerGame(screen, clock, fonts)
                            credits = game.run(credits)
                        elif key == "slot":
                            if credits < config.MIN_BET:
                                continue
                            from games.slot import SlotGame
                            game = SlotGame(screen, clock, fonts)
                            credits = game.run(credits)
                        elif key == "quit":
                            return
                        break

        # Piirto: sininen tausta, keltainen otsikko, vihreä/harmaa napit
        screen.fill(config.COLOR_BG)
        pygame.draw.rect(screen, config.COLOR_SCREEN_BLUE, (0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        bar_height = draw_credits_bar(screen, credits, fonts)

        draw_text(
            screen, "RETRO UHKAPELI",
            config.SCREEN_WIDTH // 2, bar_height + 30,
            fonts["title"], config.COLOR_TEXT_YELLOW, center=True
        )
        if credits < config.MIN_BET:
            draw_text(
                screen, "Lisaa creditteja pelataksesi",
                config.SCREEN_WIDTH // 2, bar_height + 75,
                fonts["small"], config.COLOR_TEXT_DIM, center=True
            )

        for rect, label, key in buttons:
            hover = rect.collidepoint(mouse_pos)
            if key == "poker" or key == "slot":
                if credits < config.MIN_BET:
                    hover = False
            style = "green" if key in ("poker", "slot") else "grey"
            if key == "quit":
                style = "grey"
            draw_button(screen, rect, label, fonts["menu"], hover, style=style)

        if config.SCANLINE_ALPHA > 0:
            draw_scanlines(screen)
        pygame.display.flip()
        clock.tick(30)


def main():
    pygame.init()
    screen = init_display()
    clock = pygame.time.Clock()
    fonts = get_fonts()
    run_main_menu(screen, clock, fonts)
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
