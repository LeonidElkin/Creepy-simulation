import pygame

img_size = (20, 20)
big_img_size = (40, 40)
bedrock = (50, 50)


class ImageProvider:
    """
    @class ImageProvider
    @brief Manages game images, including animations and static assets.

    The ImageProvider class loads and scales images from predefined paths, providing
    easy access to them during the game.
    """

    def __init__(self):
        """
        Initializes the ImageProvider object.

        Loads and scales images for explosions, sparkles, and creeper animations.
        """
        self.scale = 1
        _explosion_frames = [
            pygame.image.load(f"view/image/explosion/regularExplosion{i}.png").convert_alpha() for i in range(0, 8)
        ]
        self.explosion_frames = [pygame.transform.scale(frame, img_size) for frame in _explosion_frames]
        _sparkle_frames = [
            pygame.image.load(f"view/image/sparkle/sparkle_{i}.png").convert_alpha() for i in range(1, 8)
        ]
        self.sparkle_frames = [pygame.transform.scale(frame, img_size) for frame in _sparkle_frames]

        self.creeper_image_walk = pygame.transform.scale(
            pygame.image.load("view/image/walk.png").convert_alpha(), img_size
        )
        self.creeper_image_hiss = pygame.transform.scale(
            pygame.image.load("view/image/hiss.png").convert_alpha(), img_size
        )
        self.creeper_image_sleep = pygame.transform.scale(
            pygame.image.load("view/image/sleep.png").convert_alpha(), img_size
        )
        self.creeper_image_born = pygame.transform.scale(
            pygame.image.load("view/image/born.png").convert_alpha(), img_size
        )
        self.creeper_image_bonk = pygame.transform.scale(
            pygame.image.load("view/image/bonk.png").convert_alpha(), img_size
        )
        self.creeper_image_gotosteve = pygame.transform.scale(
            pygame.image.load("view/image/gotosteve.png").convert_alpha(), img_size
        )
        self.steve_image_grave = pygame.transform.scale(
            pygame.image.load("view/image/grave.png").convert_alpha(), big_img_size
        )
        self.ocelot = pygame.transform.scale(pygame.image.load("view/image/ocelot.png").convert_alpha(), img_size)
        self.steve = pygame.transform.scale(pygame.image.load("view/image/steve.png").convert_alpha(), img_size)
        self.bedrock = pygame.transform.scale(pygame.image.load("view/image/bedrock.png").convert_alpha(), bedrock)
        self.bedrock_spawn = pygame.transform.scale(
            pygame.image.load("view/image/bedrock_spawn.png").convert_alpha(), bedrock
        )
        self.background_image = pygame.image.load("view/image/background.jpg").convert()


image_provider = None
