import pygame
import math
import src.game.racers as racers
from src.constants import (
    FRAME_RATE,
    SPEED,
    WINDOW_HEIGHT
    )

class Race():
    def __init__(self, \
                screen : pygame.Surface, \
                roadImg : pygame.Surface, \
                player : racers.Player) -> None:
        
        self.__run : bool = True
        self.__gameOver : bool = False
        self.__score : int = 0
        self.__clock = pygame.time.Clock()
        self.__player = player
        self.__playerGroup = pygame.sprite.Group()
        self.__enemiesGroup = pygame.sprite.Group()
        self.__background = roadImg
        self.__backgroundRect = roadImg.get_rect()
        self.__playerGroup.add(self.__player)
        
        screen.blit(self.__background, self.__backgroundRect)
        self.race(screen)


    def race(self, screen : pygame.Surface) -> None:
        """
        Race loop
        """
        bg_height = self.__background.get_height()
        i = 0

        scroll = 0
        tiles = math.ceil(WINDOW_HEIGHT  / bg_height) + 1 
        
        
        while self.__run:
            self.__clock.tick(FRAME_RATE)
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__run = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.__player.rect.left -= SPEED
                        
                    elif event.key == pygame.K_RIGHT:
                        self.__player.rect.right += SPEED

            if i >= tiles: i = 0
            if abs(scroll) + 1 > bg_height: scroll = 0
            
            self.__backgroundRect.y = i * bg_height + scroll
            screen.blit(self.__background, self.__backgroundRect)         
            self.__playerGroup.draw(screen)
            pygame.display.update()
            
            scroll -= (SPEED / 4)
            i += 1

            while self.__gameOver:
                self.__clock.tick(FRAME_RATE)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.__run = False
                        self.__gameOver = False
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            # reset the game
                            self.__gameOver = False
                            self.__score = 0
                            #vehicle_group.empty()
                            self.__player.rect.center = [0, 0]
                        elif event.key == pygame.K_n:
                            # exit the loops
                            self.__gameOver = False
                            self.__run = False
            
            
        

