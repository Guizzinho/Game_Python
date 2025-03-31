import pygame

class Background:
    def __init__(self, image_path, width, height):
        self.image = pygame.image.load(image_path)
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, surface, offset_x, offset_y):
        scaled_width = int(self.width)
        scaled_height = int(self.height)
        scaled_image = pygame.transform.scale(self.image, (scaled_width, scaled_height))
        scaled_rect = pygame.Rect(
            int(-offset_x),
            int(-offset_y),
            scaled_width,
            scaled_height,
        )
        surface.blit(scaled_image, scaled_rect)