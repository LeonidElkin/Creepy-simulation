import pygame
from creepers import SteveState

from view.logger import logger
from view.units.Entity import EntityDrawer, entity_within_bounds


class SteveDrawer(EntityDrawer):
    def __init__(self, position: tuple[float, float], image):
        super().__init__(position, image)

    def draw_step(self, drawer):
        self.update_position()
        screen_x = self.cur_x * drawer.zoom_level + drawer.offset_x
        screen_y = self.cur_y * drawer.zoom_level + drawer.offset_y
        size = int(20 * drawer.zoom_level)

        if not (0 - size < screen_x < drawer.width and 0 - size < screen_y < drawer.height):
            return  # Крипер вне видимой области

        if self.state in (SteveState.Walk, SteveState.Born):
            image = drawer.images.steve
        else:
            return

        scaled_image = pygame.transform.scale(image, (size, size))
        drawer.screen.blit(scaled_image, (screen_x, screen_y))


class SteveManager:
    def __init__(self, app, position_shift):
        self.app = app
        self.shift = position_shift
        steves_data = app.simulation.get_steves_manager().get_steves()
        if not steves_data:
            logger.error("No steve data received from simulation!")
        self.steves = [SteveDrawer(coord, app.images.steve) for coord, _ in self._steves2data(steves_data)]

    def _steves2data(self, steves):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        # data = [(shift_coord(steve.get_coord()), steve.get_state()) for steve in steves]
        # logger.info(f"Processed steves data: {data}")
        return ((shift_coord(steve.get_coord()), steve.get_state()) for steve in steves)

    def update_steves(self, steps):
        # self.app.simulation.wait_update_field()
        logger.info(f"Updating steves: total={len(self.steves)}")

        data = list(self._steves2data(self.app.simulation.get_steves()))
        if len(self.steves) != len(data):
            logger.error(f"Mismatch in steve counts: {len(self.steves)} vs {len(data)}")
            return

        for steve_obj, (coord, _) in zip(self.steves, data):
            logger.info(f"Updating steve: {steve_obj}, coord: {coord}")
            try:
                steve_obj.update(coord, steps)
            except Exception as e:
                logger.exception(f"Error updating steve: {e}")
                raise

        # self.app.simulation.run_update_field()
        logger.info("Steves updated.")

    def draw_steves(self, drawer):
        for index, steve in enumerate(self.steves):
            if entity_within_bounds(steve, drawer):
                try:
                    logger.debug(f"Drawing steve {index}: position=({steve.cur_x}, {steve.cur_y})")
                    steve.draw_step(drawer)
                except Exception as e:
                    logger.error(f"Error drawing steve {index}: {e}")
                    raise
