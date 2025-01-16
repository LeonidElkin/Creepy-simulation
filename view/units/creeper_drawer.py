from dataclasses import dataclass

from creepers_lib import CreeperState

from view.logger import logger
from view.units.Entity import EntityDrawer, entity_within_bounds


@dataclass
class CreeperParams:
    radius: float = 20
    radius_explosion: float = 10
    creeper_count: int = 10


class CreeperDrawer(EntityDrawer):
    def __init__(self, position: tuple[float, float], state: CreeperState, drawer):
        super().__init__(position, None, drawer, state)
        self.dx = self.dy = 0
        self.state = state
        self.set_img()

    def set_img(self):
        if self.state in (CreeperState.Walk, CreeperState.Explodes, CreeperState.Dead):
            self.image = self.drawer.image_provider.creeper_image_walk
        elif self.state == CreeperState.Born:
            self.image = self.drawer.image_provider.creeper_image_born
        elif self.state == CreeperState.Sleep:
            self.image = self.drawer.image_provider.creeper_image_sleep
        elif self.state == CreeperState.Hissing:
            self.image = self.drawer.image_provider.creeper_image_hiss
        else:
            logger.error(f"Unknown creeper state, draw bonk: {self.state.name}")
            self.image = self.drawer.image_provider.creeper_image_bonk

    def update(self, new_position: tuple[float, float], steps, state=None):
        self.state = state
        if state == CreeperState.Born:
            self.cur_x, self.cur_y = new_position
            self.target_x, self.target_y = new_position
            self.steps_left = 0
        else:
            if state == CreeperState.Explodes:
                self.drawer.will_explodes.add((self.cur_x, self.cur_y))
            self.target_x, self.target_y = new_position
            self._set_target(steps)

        self.set_img()


class CreepersManager:
    def __init__(self, app, manager, position_shift):
        self.manager = manager
        self.shift = position_shift
        self.creepers = [
            CreeperDrawer(coord, state, app) for coord, state in self._creepers2data(self.manager.get_creepers())
        ]

    def _creepers2data(self, creepers):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        # data = [(shift_coord(steve.get_coord()), steve.get_state()) for steve in creepers]
        # logger.info(f"Processed creeper data: {data}")
        return ((shift_coord(creeper.get_coord()), creeper.get_state()) for creeper in creepers)

    def update_creepers(self, steps):
        logger.debug(f"Updating creepers: total={len(self.creepers)}")
        data = list(self._creepers2data(self.manager.get_creepers()))
        if len(self.creepers) != len(data):
            logger.error(f"Mismatch in creeper counts: {len(self.creepers)} vs {len(data)}")
            return
        for drawer_obj, (coord, state) in zip(self.creepers, data):
            drawer_obj.update(coord, steps, state)
        logger.info("Creepers updated.")

    def draw_creepers(self, drawer):
        for index, creeper in enumerate(self.creepers):
            if entity_within_bounds(creeper, drawer):
                try:
                    # logger.debug(f"Drawing creeper {index}: position=({creeper.cur_x}, {creeper.cur_y})")
                    creeper.draw_step()
                except Exception as e:
                    logger.error(f"Error drawing creeper {index}: {e}")
                    raise
