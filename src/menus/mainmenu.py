import pygame
import src.game.race as race
import src.game.racers as racers
from src.constants import (
    FRAME_RATE,
    ROAD_HEIGHT,
    WINDOW_WIDTH,
    CARS_PATH,
    CAR_PREFIX,
    PNG_FORMAT,
)


class MainMenu:
    def __init__(self, screen: pygame.Surface, background: pygame.Surface) -> None:
        self.__screen = screen
        self.__background = background
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 60)
        self.initMenu()

    def initMenu(self):
        self.__screen.blit(self.__background, self.__background.get_rect())
        self.printText("Press ANY KEY to begin", 200, 100)
        self.printText("    or press ESC to exit", 200, 200)

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
                        self.startRace()
                        self.initMenu()

    def startRace(self):
        road = pygame.image.load("res/roads/road_1L.png")
        car = pygame.image.load("res/cars/car_1.png").convert_alpha()
        enemies = []
        for i in range(2, 7):
            enemies.append(
                pygame.image.load(
                    CARS_PATH + CAR_PREFIX + str(i) + PNG_FORMAT
                ).convert_alpha()
            )
        player = racers.Player(car, WINDOW_WIDTH // 2, ROAD_HEIGHT)
        racing = race.Race(self.__screen, road, player, enemies)
