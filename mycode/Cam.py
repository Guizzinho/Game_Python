from mycode.Const import WIN_WIDTH, WIN_HEIGHT
import pygame

class Camera:
    def __init__(self, level_width, level_height):
        self.level_width = level_width
        self.level_height = level_height
        self.offset_x = 0
        self.offset_y = 0
        self.smooth_speed = 0.1

    def update(self, target):
        player_x = target.rect.centerx
        player_y = target.rect.centery

        screen_width = pygame.display.get_surface().get_width()
        screen_height = pygame.display.get_surface().get_height()

        target_offset_x = player_x - screen_width // 2
        target_offset_y = player_y - screen_height // 2

        self.offset_x += (target_offset_x - self.offset_x) * self.smooth_speed
        self.offset_y += (target_offset_y - self.offset_y) * self.smooth_speed

        self.offset_x = max(0, min(self.offset_x, self.level_width - screen_width))
        self.offset_y = max(0, min(self.offset_y, self.level_height - screen_height))