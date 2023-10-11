class Settings:

    def __init__(self):
        '''Инициализирует настройки игры'''
        # параметры экрана
        self.screen_width = 1000
        self.screen_height = 650
        self.bg_color = (24, 23, 28)

        # настройки корабля
        self.ship_speed = 0.8
        self.ship_limit = 3

        # настройки пули
        self.bullet_speed = 1.5
        self.bullet_wight = 3
        self.bullet_height = 13
        self.bullet_color = (0, 200, 0)
        self.bullets_allowed = 3

        # настройки пришельцев
        self.alien_speed = 0.1
        self.fleet_drop_speed = 10

        # Темп ускорения игры
        self.speedup_scale = 1.5
        # Темп роста стоимости прищельцев
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Инициализирует анстройки изменяющиеся в ходе игры'''
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0

        # fleet_diraction = 1 обозначает движение вправо, -1 влево.
        self.fleet_diraction = 1

        # Подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        '''Увеличивает настройки скорости и стоимости прищельцев'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)