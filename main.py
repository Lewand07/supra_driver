#! /usr/bin/env python3

import pygame
from src.menus.mainmenu import MainMenu


def initGame(screen: pygame.Surface) -> None:
    """
    Main game loop
    """
    # set background
    background = pygame.image.load(
        BACKGROUNDS_PATH + BACKGROUND_PREFIX + str(random.randint(1, 2)) + PNG_FORMAT
    )
    menu = MainMenu(screen, background)
    menu()


if __name__ == "__main__":
    import random
    from src.constants import (
        GAME_TITLE,
        WINDOW_HEIGHT,
        WINDOW_WIDTH,
        BACKGROUND_PREFIX,
        BACKGROUNDS_PATH,
        PNG_FORMAT,
    )

    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption(GAME_TITLE)
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    initGame(screen)

    pygame.quit()
