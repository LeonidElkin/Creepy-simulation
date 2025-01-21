import pygame


class Block:
    """
    @class Block
    @brief Represents a block with a position and size.

    The Block class provides methods for rendering the block on the screen,
    determining if a point is within the block, and calculating its borders.
    """

    def __init__(self, x, y, size):
        """
        Initializes a Block object.

        @param x: The x-coordinate of the block.
        @param y: The y-coordinate of the block.
        @param size: The size of the block (width and height assumed equal).
        """
        self.x = x
        self.y = y
        self.size = size
        print(self.x, self.y)

    def draw(self, screen, image, zoom_level, offset_x, offset_y):
        """
        Draws the block on the screen using the specified image.

        @param screen: The pygame surface to draw on.
        @param image: The image to use for rendering the block.
        @param zoom_level: The current zoom level for scaling the block.
        @param offset_x: The horizontal offset for positioning the block.
        @param offset_y: The vertical offset for positioning the block.
        """
        screen_x = self.x * zoom_level + offset_x
        screen_y = self.y * zoom_level + offset_y
        scaled_size = int(self.size * zoom_level)
        scaled_image = pygame.transform.scale(image, (scaled_size, scaled_size))
        screen.blit(scaled_image, (screen_x, screen_y))

    def contains(self, x, y):
        """
        Checks if the given point is within the block.

        @param x: The x-coordinate of the point.
        @param y: The y-coordinate of the point.
        @return: True if the point is within the block, otherwise False.
        """
        return self.x <= x < self.x + self.size and self.y <= y < self.y + self.size

    def get_borders(self, offset):
        """
        Calculates the borders of the block, adjusted by the given offset.

        @param offset: A tuple (offset_x, offset_y) to adjust the borders.
        @return: A tuple containing the top-left and bottom-right coordinates of the block.
        """
        return (self.x - 20 - offset[0], self.y - 20 - offset[1]), (
            self.x + self.size - offset[0],
            self.y + self.size - offset[1],
        )
