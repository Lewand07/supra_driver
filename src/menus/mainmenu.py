"""
Module with menu class
"""

import pygame
import random

import src.game.race as race
import src.game.racers as racers
from src.constants import (
    FRAME_RATE,
    ROAD_HEIGHT,
    WINDOW_WIDTH,
    CARS_PATH,
    CAR_PREFIX,
    ROAD_PREFIX,
    ROADS_PATH,
    PNG_FORMAT,
    MUSIC_PATH,
    MP3_FORMAT,
    BACKGROUND_PREFIX,
    BACKGROUNDS_PATH,
)


class MainMenu:
    def __init__(self, screen: pygame.Surface) -> None:
        self.__screen = screen
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 40)
        self.initMenu()

    def initMenu(self):
        """
        Init menu components
        """
        self.__background = pygame.image.load(
            BACKGROUNDS_PATH
            + BACKGROUND_PREFIX
            + str(random.randint(1, 2))
            + PNG_FORMAT
        )
        self.__screen.blit(self.__background, self.__background.get_rect())
        self.printText("Press ANY KEY to begin", 300, 320)
        self.printText("    or press ESC to exit", 300, 360)
        pygame.mixer.music.load(MUSIC_PATH + "menu" + MP3_FORMAT)
        pygame.mixer.music.play(-1)

    def printText(self, text: str, x: int, y: int) -> None:
        txt = self.__font.render(text, True, pygame.color.Color("white"))
        self.__screen.blit(txt, (x, y))

    def __call__(self) -> None:
        self.menuLoop()

    def menuLoop(self):
        quitLoop: bool = False
        clock = pygame.time.Clock()
        while not quitLoop:
            clock.tick(FRAME_RATE)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitLoop = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quitLoop = True
                    else:
                        pygame.mixer.music.stop()
                        self.startRace()
                        self.initMenu()

    def startRace(self) -> None:
        road = pygame.image.load(
            ROADS_PATH + ROAD_PREFIX + str(random.randint(1, 4)) + PNG_FORMAT
        )
        car = pygame.image.load(
            CARS_PATH + CAR_PREFIX + "1" + PNG_FORMAT
        ).convert_alpha()
        enemies = []
        for i in range(2, 7):
            enemies.append(
                pygame.image.load(
                    CARS_PATH + CAR_PREFIX + str(i) + PNG_FORMAT
                ).convert_alpha()
            )
        player = racers.Player(car, WINDOW_WIDTH // 2, ROAD_HEIGHT)
        race.Race(self.__screen, road, player, enemies)
