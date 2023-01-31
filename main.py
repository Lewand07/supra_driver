#! /usr/bin/env python3

import pygame
from src.menus.mainmenu import MainMenu

if __name__ == "__main__":
    from src.constants import (
        GAME_TITLE,
        WINDOW_HEIGHT,
        WINDOW_WIDTH,
    )

    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption(GAME_TITLE)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    menu = MainMenu(screen)
    menu()

    pygame.quit()
