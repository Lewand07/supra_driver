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
    ROAD_HEIGHT,
    WINDOW_WIDTH,
    MUSIC_PATH,
    SOUNDS_PATH,
    CARS_PATH,
    MP3_FORMAT,
    PNG_FORMAT,
)


class Race:
    def __init__(
        self,
        screen: pygame.Surface,
        roadImg: pygame.Surface,
        player: racers.Player,
        enemies: racers.Enemy,
    ) -> None:

        self.__run: bool = True
        self.__gameOver: bool = False
        self.__score: int = 0
        self.__clock = pygame.time.Clock()
        self.__player = player
        self.__playerGroup = pygame.sprite.Group()
        self.__enemies = enemies
        self.__enemiesGroup = pygame.sprite.Group()
        self.__background = roadImg
        self.__backgroundRect = roadImg.get_rect()
        self.__playerGroup.add(self.__player)
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 60)

        self.__crashSound = pygame.mixer.Sound(SOUNDS_PATH + "crash" + MP3_FORMAT)
        self.__accelSound = pygame.mixer.Sound(
            SOUNDS_PATH + "acceleration" + MP3_FORMAT
        )
        self.__driveSound = pygame.mixer.Sound(SOUNDS_PATH + "drive" + MP3_FORMAT)
        pygame.mixer.Sound.set_volume(self.__driveSound, 0.5)
        pygame.mixer.Sound.set_volume(self.__accelSound, 0.5)
        screen.blit(self.__background, self.__backgroundRect)

        self.race(screen)

    def addEnemy(self) -> None:
        """
        Spawn enemy on random X value
        """
        image = random.choice(self.__enemies)
        x = math.floor(
            (ROADSIDE_RIGHT - ROADSIDE_LEFT) * random.random() + ROADSIDE_LEFT
        )
        enemy = racers.Enemy(image, x, 0)
        for vehicle in self.__enemiesGroup:
            if pygame.sprite.collide_rect(enemy, vehicle):
                self.addEnemy()
                return

        self.__enemiesGroup.add(enemy)

    def gameOverMenu(self, screen: pygame.Surface):
        """
        Show game over menu
        """
        text1 = "          Press Y to try again        "
        text2 = "                        or                        "
        text3 = "   Press N to exit to the menu  "
        txt1 = self.__font.render(
            text1, True, pygame.color.Color("white"), pygame.color.Color("black")
        )
        screen.blit(txt1, (ROADSIDE_LEFT, WINDOW_HEIGHT / 8))
        txt2 = self.__font.render(
            text2, True, pygame.color.Color("white"), pygame.color.Color("black")
        )
        screen.blit(txt2, (ROADSIDE_LEFT, WINDOW_HEIGHT / 8 + 60))
        txt3 = self.__font.render(
            text3, True, pygame.color.Color("white"), pygame.color.Color("black")
        )
        screen.blit(txt3, (ROADSIDE_LEFT, WINDOW_HEIGHT / 8 + 120))

    def printScore(self, screen: pygame.Surface) -> None:
        text = "Score: " + str(self.__score)
        txt = self.__font.render(text, True, pygame.color.Color("white"))
        screen.blit(txt, (0, 0))

    def collision(self, screen: pygame.Surface) -> None:
        """
        Handle collision effects
        """
        explosion = pygame.image.load(CARS_PATH + "boom" + PNG_FORMAT).convert_alpha()
        exp = racers.Player(explosion, 0, 0)
        exp.rect = self.__player.rect
        self.__player.kill()
        self.__playerGroup.add(exp)
        self.__playerGroup.draw(screen)
        pygame.mixer.Sound.play(self.__crashSound)
        pygame.display.flip()

    def race(self, screen: pygame.Surface) -> None:
        """
        Race loop
        """
        bg_height = self.__background.get_height()
        tiles = math.ceil(WINDOW_HEIGHT / bg_height)
        i = 0
        scroll = 0
        gameSpeed = SPEED

        pygame.mixer.music.load(MUSIC_PATH + "race" + MP3_FORMAT)
        pygame.mixer.music.play(-1)
        pygame.mixer.Sound.play(self.__driveSound, -1)

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

            if (
                keys[pygame.K_LEFT] or keys[pygame.K_a]
            ) and self.__player.rect.x > ROADSIDE_LEFT:
                self.__player.rect.left -= gameSpeed
            if (
                keys[pygame.K_RIGHT] or keys[pygame.K_d]
            ) and self.__player.rect.x < ROADSIDE_RIGHT:
                self.__player.rect.left += gameSpeed
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.__player.rect.y > 0:
                self.__player.rect.top -= 2 * gameSpeed
                pygame.mixer.Sound.play(self.__accelSound)
            if (
                keys[pygame.K_DOWN] or keys[pygame.K_s]
            ) and self.__player.rect.y < ROAD_HEIGHT:
                self.__player.rect.bottom += gameSpeed

            # scroll road
            if self.__player.rect.y < ROAD_HEIGHT:
                self.__player.rect.y += gameSpeed / 2
            if i < -1:
                i = tiles
            if abs(scroll) + 1 > bg_height:
                scroll = 0
            self.__backgroundRect.y = i * bg_height - scroll
            scroll -= gameSpeed
            i -= 1

            # spawn enemies
            if len(self.__enemiesGroup) < 2:
                self.addEnemy()

            for enemy in self.__enemiesGroup:
                enemy.rect.y += gameSpeed
                if enemy.rect.y >= WINDOW_HEIGHT:
                    enemy.kill()
                    self.__score += 1
                    if self.__score % 8 == 0:
                        gameSpeed += math.floor(SPEED / 5)
                if pygame.sprite.collide_rect(self.__player, enemy):
                    self.__gameOver = True
                    pygame.mixer.Sound.stop(self.__driveSound)
                    self.collision(screen)

            if self.__gameOver:
                self.gameOverMenu(screen)
                pygame.display.flip()

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
                            increaseSpeed = 1.0
                            self.__enemiesGroup.empty()
                            self.__playerGroup.empty()
                            self.__player.rect.center = [WINDOW_WIDTH // 2, ROAD_HEIGHT]
                            self.__playerGroup.add(self.__player)
                            pygame.mixer.Sound.play(self.__driveSound, -1)
                        if event.key == pygame.K_n:
                            # exit the loops
                            self.__gameOver = False
                            self.__run = False
