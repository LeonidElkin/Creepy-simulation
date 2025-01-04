from units.Entity import EntityDrawer

from view.units.Entity import entity_within_bounds


class OcelotDrawer(EntityDrawer):
    def __init__(self, position: tuple[float, float], image):
        super().__init__(position, image)

    def draw_step(self, drawer):
        # Вызываем базовый метод отрисовки
        super().draw_step(drawer)


class OcelotManager:
    def __init__(self, app, position_shift):
        self.shift = position_shift
        # Инициализация оцелотов случайными координатами
        self.ocelots = [
            OcelotDrawer((app.width // 2 + i * 50, app.height // 2 + i * 50))
            for i in range(app.creeper_count // 10)  # Допустим, один оцелот на 10 криперов
        ]

    def _creepers2data(self, creepers):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        return ((shift_coord(creeper.get_coord()), creeper.get_state()) for creeper in creepers)

    def update_ocelots(self, steps, drawer):
        for ocelot in self.ocelots:
            new_x = ocelot.cur_x + (steps % 10 - 5)
            new_y = ocelot.cur_y + (steps % 10 - 5)
            ocelot.update((new_x, new_y), steps, drawer)

    def draw_ocelots(self, drawer):
        for ocelot in self.ocelots:
            if entity_within_bounds(ocelot, drawer):
                ocelot.draw_step(drawer)
