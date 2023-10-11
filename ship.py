import os

import pygame
from pygame.sprite import Sprite
from helper import Helper

class Ship(Sprite):
    '''Класс управления кораблем'''

    def __init__(self, ai_game):
        '''инициализирует корабль и задает его начальное положение'''
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # загружает изображение корабля и получает прямоугольник(габариты модели)
        helper = Helper()
        self.image = pygame.image.load(helper.resource_path(os.path.join('images', 'ship.png')))

        self.rect = self.image.get_rect()
        # каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom
        # сохранение вещественной координаты корабля
        self.x = float(self.rect.x)
        # флаги перемещений
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        '''рисует корабль в текущей позиции'''
        self.screen.blit(self.image, self.rect)
    def update(self):
        #обновляется атрибут x, не rect.x
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def center_ship(self):
        '''Размещает корабль в центре нижней стороны'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)