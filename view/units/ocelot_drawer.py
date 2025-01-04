import pygame


class OcelotDrawer:
    def __init__(self, position: tuple[float, float]):
        self.cur_x, self.cur_y = position
        self.target_x, self.target_y = position
        self.steps_left = 0

    def update(self, new_position: tuple[float, float], steps, drawer):
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

        # Проверяем, находится ли Оцелот в пределах экрана
        if not (0 - size < screen_x < drawer.width and 0 - size < screen_y < drawer.height):
            return  # Оцелот вне видимой области

        image = pygame.transform.scale(drawer.images.ocelot, (size, size))
        drawer.screen.blit(image, (screen_x, screen_y))


class OcelotManager:
    def __init__(self, app, position_shift):
        self.shift = position_shift
        # Инициализация оцелотов случайными координатами
        self.ocelots = [
            OcelotDrawer((app.width // 2 + i * 50, app.height // 2 + i * 50))
            for i in range(app.creeper_count // 10)  # Допустим, один оцелот на 10 криперов
        ]

    def update_ocelots(self, steps, drawer):
        for ocelot in self.ocelots:
            new_x = ocelot.cur_x + (steps % 10 - 5)
            new_y = ocelot.cur_y + (steps % 10 - 5)
            ocelot.update((new_x, new_y), steps, drawer)

    def draw_ocelots(self, drawer):
        # Вычисляем границы видимой области
        scaled_width = drawer.width / drawer.zoom_level
        scaled_height = drawer.height / drawer.zoom_level
        left_bound = -drawer.offset_x / drawer.zoom_level
        top_bound = -drawer.offset_y / drawer.zoom_level
        right_bound = left_bound + scaled_width
        bottom_bound = top_bound + scaled_height

        for ocelot in self.ocelots:
            if left_bound <= ocelot.cur_x <= right_bound and top_bound <= ocelot.cur_y <= bottom_bound:
                ocelot.draw_step(drawer)
