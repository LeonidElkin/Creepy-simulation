import pygame


class ImageProvider:
    def __init__(self):
        self.scale = 1
        _explosion_frames = [
            pygame.image.load(f"view/image/explosion/regularExplosion{i}.png").convert_alpha() for i in range(0, 8)
        ]
        self.explosion_frames = [pygame.transform.scale(frame, (20, 20)) for frame in _explosion_frames]
        _sparkle_frames = [
            pygame.image.load(f"view/image/sparkle/sparkle_{i}.png").convert_alpha() for i in range(1, 8)
        ]
        self.sparkle_frames = [pygame.transform.scale(frame, (20, 20)) for frame in _sparkle_frames]

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
        self.creeper_image_bonk = pygame.transform.scale(
            pygame.image.load("view/image/bonk.png").convert_alpha(), (20, 20)
        )
        self.ocelot = pygame.transform.scale(pygame.image.load("view/image/ocelot.png").convert_alpha(), (20, 20))
        self.steve = pygame.transform.scale(pygame.image.load("view/image/steve.png").convert_alpha(), (20, 20))
        self.bedrock = pygame.transform.scale(pygame.image.load("view/image/bedrock.png").convert_alpha(), (20, 20))
        self.background_image = pygame.image.load("view/image/background.jpg").convert()

    def scale_image(self, scale):
        self.scale = scale
        size = int(20 * scale)
        self.creeper_image_walk = pygame.transform.scale(
            pygame.image.load("view/image/walk.png").convert_alpha(), (size, size)
        )
        self.creeper_image_hiss = pygame.transform.scale(
            pygame.image.load("view/image/hiss.png").convert_alpha(), (size, size)
        )
        self.creeper_image_sleep = pygame.transform.scale(
            pygame.image.load("view/image/sleep.png").convert_alpha(), (size, size)
        )
        self.creeper_image_born = pygame.transform.scale(
            pygame.image.load("view/image/born.png").convert_alpha(), (size, size)
        )
        self.creeper_image_bonk = pygame.transform.scale(
            pygame.image.load("view/image/bonk.png").convert_alpha(), (size, size)
        )
        self.ocelot = pygame.transform.scale(pygame.image.load("view/image/ocelot.png").convert_alpha(), (size, size))
        self.steve = pygame.transform.scale(pygame.image.load("view/image/steve.png").convert_alpha(), (size, size))
        self.explosion_frames = [pygame.transform.scale(frame, (size, size)) for frame in self.explosion_frames]
        self.sparkle_frames = [pygame.transform.scale(frame, (size, size)) for frame in self.sparkle_frames]

        self.bedrock = pygame.transform.scale(pygame.image.load("view/image/bedrock.png").convert_alpha(), (size, size))
