import pygame


class EntityDrawer:
    """
    @class EntityDrawer
    @brief Base class for drawing and updating the position of entities in the simulation.

    The EntityDrawer class manages the position, movement, and rendering of entities.
    """

    def __init__(self, position: tuple[float, float], image, drawer):
        """
        Initializes an EntityDrawer object.

        @param position: The initial position of the entity.
        @param image: The image used for rendering the entity.
        @param drawer: The drawer object managing the rendering context.
        """
        self.drawer = drawer
        self.cur_x, self.cur_y = position
        self.target_x, self.target_y = position
        self.steps_left = 0
        self.image = image

    def update(self, new_position: tuple[float, float], steps, new_state=None):
        """
        Updates the target position and movement steps for the entity.

        @param new_position: The new target position of the entity.
        @param steps: The number of steps required to reach the target position.
        @param new_state: Optional state information for the entity.
        """
        self.target_x, self.target_y = new_position
        self._set_target(steps)

    def _set_target(self, steps):
        """
        Configures the movement steps and direction to the target position.

        @param steps: The number of steps to reach the target position.
        """
        self.steps_left = steps
        if steps > 0:
            self.dx = (self.target_x - self.cur_x) / steps
            self.dy = (self.target_y - self.cur_y) / steps
        else:
            self.dx = self.dy = 0

    def update_position(self):
        """
        Updates the current position of the entity based on its movement steps.

        @return: True if the entity has remaining steps to move, otherwise False.
        """
        if self.steps_left > 0:
            self.cur_x += self.dx
            self.cur_y += self.dy
            self.steps_left -= 1
        return self.steps_left > 0

    def draw_step(self):
        """
        Updates the position and renders the entity on the screen.

        Ensures that the entity is only rendered if it is within the visible bounds.
        """
        self.update_position()

        screen_x = self.cur_x * self.drawer.zoom_level + self.drawer.offset_x
        screen_y = self.cur_y * self.drawer.zoom_level + self.drawer.offset_y

        size = int(self.image.get_size()[0] * self.drawer.zoom_level)

        # Проверяем, находится ли объект в пределах экрана
        if not (0 - size < screen_x < self.drawer.width and 0 - size < screen_y < self.drawer.height):
            return  # Объект вне видимой области

        scaled_image = pygame.transform.scale(self.image, (size, size))
        self.drawer.screen.blit(scaled_image, (screen_x, screen_y))


def entity_within_bounds(entity, drawer):
    """
    Checks if an entity is within the visible bounds of the drawer.

    @param entity: The entity to check.
    @param drawer: The drawer object managing the rendering context.
    @return: True if the entity is within the visible bounds, otherwise False.
    """
    # Вычисляем границы видимой области
    scaled_width = drawer.width / drawer.zoom_level
    scaled_height = drawer.height / drawer.zoom_level
    left_bound = -drawer.offset_x / drawer.zoom_level
    top_bound = -drawer.offset_y / drawer.zoom_level
    right_bound = left_bound + scaled_width
    bottom_bound = top_bound + scaled_height
    return left_bound <= entity.cur_x <= right_bound and top_bound <= entity.cur_y <= bottom_bound
