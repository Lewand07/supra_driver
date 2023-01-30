#! /usr/bin/env python3

import pygame
import pygamepopup

def mainLoop() -> None:
    """
    Main game loop
    """


if __name__ == "__main__":
    import random

    from src.constants import (
        GAME_TITLE,
        WINDOW_HEIGHT,
        WINDOW_WIDTH
    )

    pygame.init()
    pygamepopup.init()

    pygame.display.set_caption(GAME_TITLE)
    mainScreen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    background = pygame.image.load("res/backgrounds/background_" + str(random.randint(1, 2)) + ".png")
    bgRect = background.get_rect()
    mainScreen.fill([255, 255, 255])
    mainScreen.blit(background, bgRect)
    pygame.display.update()
    
    while(1): pass

    pygame.quit()