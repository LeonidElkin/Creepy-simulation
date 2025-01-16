from creepers_lib import SteveState

from view.logger import logger
from view.units.Entity import EntityDrawer, entity_within_bounds


class SteveDrawer(EntityDrawer):
    def __init__(self, position: tuple[float, float], state: SteveState, drawer):
        super().__init__(position, None, drawer, state)
        self.dx = self.dy = 0
        self.state = state
        self.set_img()

    def set_img(self):
        self.image = self.drawer.image_provider.steve

        if self.state not in (SteveState.Walk, SteveState.Born):
            logger("invalid steve state")

    def update(self, new_position: tuple[float, float], steps, state=None):
        self.state = state
        self.target_x, self.target_y = new_position
        self._set_target(steps)

        self.set_img()


class SteveManager:
    def __init__(self, app, manager, position_shift):
        self.manager = manager
        self.shift = position_shift
        steves_data = self.manager.get_steves()
        if not steves_data:
            logger.error("No steve data received from simulation!")
        self.steves = [SteveDrawer(coord, state, app) for coord, state in self._steves2data(self.manager.get_steves())]

    def _steves2data(self, steves):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        # data = [(shift_coord(steve.get_coord()), steve.get_state()) for steve in steves]
        # logger.info(f"Processed steves data: {data}")
        return ((shift_coord(steve.get_coord()), steve.get_state()) for steve in steves)

    def update_steves(self, steps):
        data = list(self._steves2data(self.manager.get_steves()))
        if len(self.steves) != len(data):
            logger.error(f"Mismatch in steve counts: {len(self.steves)} vs {len(data)}")
            return

        for steve_obj, (coord, state) in zip(self.steves, data):
            try:
                steve_obj.update(coord, steps, state)
            except Exception as e:
                logger.exception(f"Error updating steve: {e}")
                raise

        logger.info("Steves updated.")

    def draw_steves(self, drawer):
        for index, steve in enumerate(self.steves):
            if entity_within_bounds(steve, drawer):
                try:
                    # logger.debug(f"Drawing steve {index}: position=({steve.cur_x}, {steve.cur_y})")
                    steve.draw_step()
                except Exception as e:
                    logger.error(f"Error drawing steve {index}: {e}")
                    raise
