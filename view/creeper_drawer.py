import pygame
from creepers import CreeperState, Field


class CreeperDrawer:
    def __init__(self, position: tuple[float, float], state: CreeperState):
        self.cur_x, self.cur_y = position
        self.state = state
        self.target_x, self.target_y = position
        self.steps_left = 0

    def update(self, new_position: tuple[float, float], state: CreeperState, steps, drawer):
        self.state = state
        if state == CreeperState.Born:
            self.cur_x, self.cur_y = new_position
        elif state == CreeperState.Explodes:
            drawer.will_explodes.add(new_position)
        self.target_x, self.target_y = new_position
        self._set_target(steps)

    def _set_target(self, steps):
        self.steps_left = steps
        if not steps:
            return
        self.dx = (self.target_x - self.cur_x) / steps
        self.dy = (self.target_y - self.cur_y) / steps

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

        # Проверяем, находится ли крипер в пределах экрана
        if not (0 - size < screen_x < drawer.width and 0 - size < screen_y < drawer.height):
            return  # Крипер вне видимой области

        if self.state in {CreeperState.Walk, CreeperState.Explodes}:
            image = pygame.transform.scale(drawer.images.creeper_image_walk, (size, size))
            drawer.screen.blit(image, (screen_x, screen_y))
        elif self.state == CreeperState.Born:
            image = pygame.transform.scale(drawer.images.creeper_image_born, (size, size))
            drawer.screen.blit(image, (screen_x, screen_y))
        elif self.state == CreeperState.Sleep:
            image = pygame.transform.scale(drawer.images.creeper_image_sleep, (size, size))
            drawer.screen.blit(image, (screen_x, screen_y))
        elif self.state == CreeperState.Hissing:
            image = pygame.transform.scale(drawer.images.creeper_image_hiss, (size, size))
            drawer.screen.blit(image, (screen_x, screen_y))


class CreepersManager:
    def __init__(self, app, position_shift):
        self.field = Field(
            (app.width, app.height),
            creepers_num=app.creeper_count,
            explosion_radius=app.radius_explosion,
            move_radius=app.radius,
            dist_func=app.dist_func,
        )
        self.shift = position_shift
        self.creepers = [CreeperDrawer(coord, state) for coord, state in self._creepers2data(self.field.get_creepers())]
        self.field.run_update_field()

    def _creepers2data(self, creepers):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        return ((shift_coord(creeper.get_coord()), creeper.get_state()) for creeper in creepers)

    def update_creepers(self, steps, drawer):
        self.field.wait_update_field()
        for drawers, (coord, state) in zip(self.creepers, self._creepers2data(self.field.get_creepers())):
            drawers.update(coord, state, steps, drawer)
        self.field.run_update_field()

    def draw_creepers(self, drawer):
        # Вычисляем границы видимой области
        scaled_width = drawer.width / drawer.zoom_level
        scaled_height = drawer.height / drawer.zoom_level
        left_bound = -drawer.offset_x / drawer.zoom_level
        top_bound = -drawer.offset_y / drawer.zoom_level
        right_bound = left_bound + scaled_width
        bottom_bound = top_bound + scaled_height

        for creeper in self.creepers:
            if left_bound <= creeper.cur_x <= right_bound and top_bound <= creeper.cur_y <= bottom_bound:
                creeper.draw_step(drawer)
