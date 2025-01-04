import pygame


class EntityDrawer:
    def __init__(self, position: tuple[float, float], image, state=None):
        self.cur_x, self.cur_y = position
        self.target_x, self.target_y = position
        self.steps_left = 0
        self.image = image
        self.state = state

    def update(self, new_position: tuple[float, float], steps, state=None):
        self.target_x, self.target_y = new_position
        self.state = state
        self._set_target(steps)

    def _set_target(self, steps):
        self.steps_left = steps
        if steps > 0:
            self.dx = (self.target_x - self.cur_x) / steps
            self.dy = (self.target_y - self.cur_y) / steps
        else:
            self.dx = self.dy = 0

    def update_position(self):
        if self.steps_left > 0:
            self.cur_x += self.dx
            self.cur_y += self.dy
            self.steps_left -= 1
        return self.steps_left > 0

    def draw_step(self, drawer):
        self.update_position()

        screen_x = self.cur_x * drawer.zoom_level + drawer.offset_x
        screen_y = self.cur_y * drawer.zoom_level + drawer.offset_y

        size = int(20 * drawer.zoom_level)

        # Проверяем, находится ли объект в пределах экрана
        if not (0 - size < screen_x < drawer.width and 0 - size < screen_y < drawer.height):
            return  # Объект вне видимой области

        scaled_image = pygame.transform.scale(self.image, (size, size))
        drawer.screen.blit(scaled_image, (screen_x, screen_y))


def entity_within_bounds(entity, drawer):
    # Вычисляем границы видимой области
    scaled_width = drawer.width / drawer.zoom_level
    scaled_height = drawer.height / drawer.zoom_level
    left_bound = -drawer.offset_x / drawer.zoom_level
    top_bound = -drawer.offset_y / drawer.zoom_level
    right_bound = left_bound + scaled_width
    bottom_bound = top_bound + scaled_height
    return left_bound <= entity.cur_x <= right_bound and top_bound <= entity.cur_y <= bottom_bound
