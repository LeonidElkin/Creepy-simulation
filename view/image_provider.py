import pygame


class ImageProvider:
    def __init__(self):
        _explosion_frames = [
            pygame.image.load(f"view/image/regularExplosion{i}.png").convert_alpha() for i in range(0, 8)
        ]
        self.explosion_frames = [pygame.transform.scale(frame, (20, 20)) for frame in _explosion_frames]
        self.creeper_image_walk = pygame.transform.scale(
            pygame.image.load("view/image/walk.png").convert_alpha(), (20, 20)
        )
        self.creeper_image_hiss = pygame.transform.scale(
            pygame.image.load("view/image/hiss.png").convert_alpha(), (20, 20)
        )
        self.creeper_image_sleep = pygame.transform.scale(
            pygame.image.load("view/image/sleep.png").convert_alpha(), (20, 20)
        )
        self.creeper_image_born = pygame.transform.scale(
            pygame.image.load("view/image/born.png").convert_alpha(), (20, 20)
        )
        self.background_image = pygame.image.load("view/image/background.jpg").convert()
