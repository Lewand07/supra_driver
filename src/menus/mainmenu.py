import pygame
import src.game.race as race
import src.game.racers as racers
from src.constants import (
    FRAME_RATE
)

class MainMenu():
    def __init__(self, screen : pygame.Surface, background : pygame.Surface) -> None:
        self.__screen = screen
        self.__screen.blit(background, background.get_rect())
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 60)
    
    def printText(self, text : str, x : int, y : int) -> None:
        txt = self.__font.render(text, True, pygame.color.Color("white"))
        self.__screen.blit(txt, (x, y))

    def __call__(self) -> None:
        self.printText("Press ANY KEY to begin", 200, 100)
        
        self.menuLoop()
        

    def menuLoop(self):
        quitLoop : bool = False
        clock = pygame.time.Clock()
        while not quitLoop:
            clock.tick(FRAME_RATE)
            pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quitLoop = True
                if event.type == pygame.KEYDOWN:
                    self.startRace()
                    quitLoop = True

    def startRace(self):
        road = pygame.image.load("res/roads/road_1.png")
        car = pygame.image.load("res/cars/car_1.png").convert_alpha()
        player = racers.Player(car, 500, 500)
        racing = race.Race(self.__screen, road, player)