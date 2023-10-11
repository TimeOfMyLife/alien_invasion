import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
class AlienInvision:
    ''' Класс для управления ресурсами и поведением игры '''

    def __init__(self):
        ''' Инициализирует игру и создает игровые ресурсы '''
        pygame.init()

        self.settings = Settings()

        # запуск в окне
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # запуск на весь экран
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # создаем новый экземпляр корабля
        self.ship = Ship(self)

        # группа хранения снарядов
        self.bullets = pygame.sprite.Group()

        # группа хранения прищельцев
        self.aliens = pygame.sprite.Group()

        # создание группы инопланетян
        self._create_fleet()

        # создание экземпляра для хранения игровой статистики
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # создание конопки
        self.play_button = Button(self, "Play")

    def run_game(self):
        '''Запуск основного цикла игры'''
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
    def _check_events(self):
        # отслеживание событий клавиатуры и мыши
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        #  реагирует нажатие клавиш
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        #  реагирует отжатие клавиш
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''Создание нового снаряда и включение его в группу bullets'''
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):

        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Проверка попадания в пришельцев
        # При попадании старяда удалить снаряд и прищельца
        collisions = pygame.sprite.groupcollide(self.bullets,
                                                self.aliens,
                                                True,
                                                True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Уничножение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _update_screen(self):
        # при каждом прогоне цикла перерисовывается экран
        self.screen.fill(self.settings.bg_color)
        # отрисовка корабля
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Вывод информации о счете
        self.sb.show_score()
        # Кнопка Play отображается в том случае, если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()

        # отображение последнего прорисованного экрана
        pygame.display.flip()

    def _create_fleet(self):
        '''создает флот прищельцев'''
        # создание прищельца и вычисление количества прищельцев в ряду
        # Интервал между прищельцами равен половине ширины прищельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        avaliable_space_x = self.settings.screen_width - 2 * (alien_width // 3)
        number_aliens_x = int(avaliable_space_x // (alien_width + (alien_width/5)))

        '''Определяет количество рядов на экране'''
        ship_height = self.ship.rect.height
        avaliable_space_y = (self.settings.screen_height - 3 * alien_height - ship_height)
        number_rows = int(avaliable_space_y // (2 * alien_height))

        # Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        '''Создание прищельца и размещение его в ряду'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        print('alien_width:', alien_width)
        alien.x = int((alien_width / 3) + (alien_width + (alien_width / 7)) * alien_number)
        alien.rect.x = alien.x
        alien.rect.y = (alien_height * 1.3) + (alien_height + (alien_height)/2) * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        '''Обновляет позицию всех пришельцев во флоте'''
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # проверить, добрались ли пришельцы до нижнего края экрана
        self._check_aliens_botton()

    def _check_fleet_edges(self):
        '''Реагиркет на достижение прищельцем края экрана'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_diraction()
                break

    def _change_fleet_diraction(self):
        '''Отпускает весь флот и меяет направление флота'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_diraction *= -1

    def _ship_hit(self):
        # уменьшение ships_left
        if self.stats.ships_left > 0:
            # уменьшает Ships left и обновляет панели счета
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # очистка списков прищельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # создние нового флота и размещение кордбля в центре
            self._create_fleet()
            self.ship.center_ship()

            # пауза
            sleep(1)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_botton(self):
        '''Проверяет, добрались ли пришельцы до нижнего края экрана'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # происходит то же, что при столкновении с кораблем
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        '''запкскает новую игру при нажатии на play'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            # Указатель мыши скрывается
            pygame.mouse.set_visible(False)

if __name__ == '__main__':
    # создание экземпляра и запуск игры
    ai = AlienInvision()
    ai.run_game()