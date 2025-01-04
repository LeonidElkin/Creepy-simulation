from view.units.Entity import EntityDrawer, entity_within_bounds


class SteveDrawer(EntityDrawer):
    def __init__(self, position: tuple[float, float], image):
        super().__init__(position, image)

    def draw_step(self, drawer):
        # Вызываем базовый метод отрисовки
        super().draw_step(drawer)


class SteveManager:
    def __init__(self, app, position_shift):
        self.shift = position_shift
        # Инициализация Стивов случайными координатами
        self.steve = [
            SteveDrawer((app.width // 2 + i * 50, app.height // 2 + i * 50))
            for i in range(app.creeper_count // 10)  # Допустим, один Стив на 10 криперов
        ]

    def _creepers2data(self, creepers):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        return ((shift_coord(creeper.get_coord()), creeper.get_state()) for creeper in creepers)

    def update_steves(self, steps, drawer):
        for steve in self.steve:
            new_x = steve.cur_x + (steps % 10 - 5)
            new_y = steve.cur_y + (steps % 10 - 5)
            steve.update((new_x, new_y), steps, drawer)

    def draw_steves(self, drawer):
        for steve in self.steve:
            if entity_within_bounds(steve, drawer):
                steve.draw_step(drawer)
