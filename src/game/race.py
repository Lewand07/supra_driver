import pygame
import math
import random
import src.game.racers as racers
from src.constants import (
    FRAME_RATE,
    SPEED,
    WINDOW_HEIGHT,
    ROADSIDE_LEFT,
    ROADSIDE_RIGHT,
    ROAD_HEIGHT
    )

class Race():
    def __init__(self, \
                screen : pygame.Surface, \
                roadImg : pygame.Surface, \
                player : racers.Player, \
                enemies : racers.Enemy) -> None:
        
        self.__run : bool = True
        self.__gameOver : bool = False
        self.__score : int = 0
        self.__clock = pygame.time.Clock()
        self.__player = player
        self.__playerGroup = pygame.sprite.Group()
        self.__enemies = enemies
        self.__enemiesGroup = pygame.sprite.Group()
        self.__background = roadImg
        self.__backgroundRect = roadImg.get_rect()
        self.__playerGroup.add(self.__player)
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 60)
        screen.blit(self.__background, self.__backgroundRect)
        self.race(screen)

    def addEnemy(self) -> None:
        image = random.choice(self.__enemies)
        x = math.floor((ROADSIDE_RIGHT - ROADSIDE_LEFT)* random.random() + ROADSIDE_LEFT)
        enemy = racers.Enemy(image, x, 0)
        self.__enemiesGroup.add(enemy)

    def printScore(self, screen: pygame.Surface) -> None:
        text = "Score: " + str(self.__score)
        txt = self.__font.render(text, True, pygame.color.Color("white"))
        screen.blit(txt, (0, 0))

    def race(self, screen : pygame.Surface) -> None:
        """
        Race loop
        """
        bg_height = self.__background.get_height()
        tiles = math.ceil(WINDOW_HEIGHT  / bg_height)
        i = 0
        scroll = 0
        
        while self.__run:
            self.__clock.tick(FRAME_RATE)
            
            # draw objects
            screen.blit(self.__background, self.__backgroundRect)
            self.__playerGroup.draw(screen)
            self.__enemiesGroup.draw(screen)
            self.printScore(screen)
            pygame.display.flip()

            # handle keys
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__run = False
            
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.__player.rect.x > ROADSIDE_LEFT:
                self.__player.rect.left -= SPEED
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.__player.rect.x < ROADSIDE_RIGHT:
                self.__player.rect.left += SPEED
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.__player.rect.y > 0:
                self.__player.rect.top -= 2 * SPEED
            if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.__player.rect.y < ROAD_HEIGHT:
                self.__player.rect.bottom += SPEED

            # scroll road
            if self.__player.rect.y < ROAD_HEIGHT:
                self.__player.rect.y += SPEED / 2
            if i < -1: i = tiles
            if abs(scroll) + 1 > bg_height: scroll = 0
            self.__backgroundRect.y = i * bg_height - scroll
            scroll -= SPEED 
            i -= 1

            # spawn enemies
            if len(self.__enemiesGroup) < 2:
                self.addEnemy()
            
            for enemy in self.__enemiesGroup:
                enemy.rect.y += SPEED
                if enemy.rect.y >= WINDOW_HEIGHT:
                    enemy.kill()
                    self.__score += 1

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
                            #self.__enemiesGroup.empty()
                            self.__player.rect.center = [0, 0]
                        elif event.key == pygame.K_n:
                            # exit the loops
                            self.__gameOver = False
                            self.__run = False
            
            
        

