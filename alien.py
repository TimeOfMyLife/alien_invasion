import os

import pygame
from pygame.sprite import Sprite
from helper import Helper
class Alien(Sprite):

    '''Класс, представляющий одного прищельца'''
    def __init__(self, ai_game):
        """Инициализирует прищельца и задает его начальную позицию"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # загрузка изображения прищельца и назначение атрибута rect
        helper = Helper()
        self.image = pygame.image.load(helper.resource_path(os.path.join('images', 'alien.png')))
        self.rect = self.image.get_rect()

        # каждый новый прищелец появиться в левом верхнем углу экрана
        self.rect.x = self.rect.width / 2
        self.rect.y = self.rect.height / 2

        # сохранение точной горизонтальной позиции прищельца
        self.x = float(self.rect.x)


    def update(self):
        '''перемещение прищельца влево или право'''
        self.x += (self.settings.alien_speed * self.settings.fleet_diraction)
        self.rect.x = self.x


    def check_edges(self):
        '''возвращает True если прищелец находится у края'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True