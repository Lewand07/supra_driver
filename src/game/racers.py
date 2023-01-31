import pygame


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, carImg, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        image_scale = 128 / carImg.get_rect().width
        new_width = carImg.get_rect().width * image_scale
        new_height = carImg.get_rect().height * image_scale
        self.image = pygame.transform.scale(carImg, (new_width, new_height))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


class Player(Vehicle):
    def __init__(self, carImg, x, y) -> None:
        super().__init__(carImg, x, y)


class Enemy(Vehicle):
    def __init__(self, carImg, x, y) -> None:
        super().__init__(carImg, x, y)
