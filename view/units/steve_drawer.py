from view.units.Entity import EntityDrawer, entity_within_bounds


class SteveDrawer(EntityDrawer):
    def __init__(self, position: tuple[float, float], image):
        super().__init__(position, image)

    def draw_step(self, drawer):
        super().draw_step(drawer)


class SteveManager:
    def __init__(self, app, position_shift):
        self.app = app
        self.shift = position_shift
        self.steves = [
            SteveDrawer(coord, app.images.steve) for coord, _ in self._steves2data(app.simulation.get_steves())
        ]

    def _steves2data(self, steves):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        return ((shift_coord(steve.get_coord()), steve.get_state()) for steve in steves)

    def update_steves(self, steps, drawer):
        self.app.simulation.wait_update_field()
        for steve_obj, (coord, _) in zip(self.steves, self._steves2data(self.app.simulation.get_steves())):
            steve_obj.update(coord, steps)
        self.app.simulation.run_update_field()

    def draw_steves(self, drawer):
        for steve in self.steves:
            if entity_within_bounds(steve, drawer):
                steve.draw_step(drawer)
