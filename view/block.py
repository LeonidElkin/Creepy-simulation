import pygame


class Block:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, screen, image, zoom_level, offset_x, offset_y):
        screen_x = self.x * zoom_level + offset_x
        screen_y = self.y * zoom_level + offset_y
        scaled_size = int(self.size * zoom_level)
        scaled_image = pygame.transform.scale(image, (scaled_size, scaled_size))
        screen.blit(scaled_image, (screen_x, screen_y))

    def contains(self, x, y):
        return self.x <= x < self.x + self.size and self.y <= y < self.y + self.size
