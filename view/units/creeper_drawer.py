import pygame
from creepers import CreeperState

from view.logger import logger
from view.units.Entity import EntityDrawer, entity_within_bounds


class CreeperDrawer(EntityDrawer):
    def __init__(self, position: tuple[float, float], state: CreeperState):
        super().__init__(position, None, state)
        self.dx = self.dy = 0
        self.state = state

    def update(self, new_position: tuple[float, float], steps, state=None):
        self.state = state
        if state == CreeperState.Born:
            self.cur_x, self.cur_y = new_position
            self.target_x, self.target_y = new_position
            self.steps_left = 0
        else:
            self.target_x, self.target_y = new_position
            self._set_target(steps)

    def draw_step(self, drawer):
        self.update_position()
        screen_x = self.cur_x * drawer.zoom_level + drawer.offset_x
        screen_y = self.cur_y * drawer.zoom_level + drawer.offset_y
        size = int(20 * drawer.zoom_level)

        if not (0 - size < screen_x < drawer.width and 0 - size < screen_y < drawer.height):
            return  # Крипер вне видимой области

        if self.state == CreeperState.Walk:
            image = drawer.images.creeper_image_walk
        elif self.state == CreeperState.Born:
            image = drawer.images.creeper_image_born
        elif self.state == CreeperState.Sleep:
            image = drawer.images.creeper_image_sleep
        elif self.state == CreeperState.Hissing:
            image = drawer.images.creeper_image_hiss
        elif self.state == CreeperState.Explodes:
            image = drawer.images.creeper_image_walk  # Замените на нужное изображение
        else:
            return

        scaled_image = pygame.transform.scale(image, (size, size))
        drawer.screen.blit(scaled_image, (screen_x, screen_y))


class CreepersManager:
    def __init__(self, app, position_shift):
        self.app = app
        self.shift = position_shift
        self.creepers = [
            CreeperDrawer(coord, state)
            for coord, state in self._creepers2data(app.simulation.get_creepers_manager().get_creepers())
        ]
        app.simulation.run_update_field()

    def _creepers2data(self, creepers):
        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        return ((shift_coord(creeper.get_coord()), creeper.get_state()) for creeper in creepers)

    def update_creepers(self, steps, drawer):
        self.app.simulation.wait_update_field()
        logger.debug(f"Updating creepers: total={len(self.creepers)}")
        data = list(self._creepers2data(self.app.simulation.get_creepers_manager().get_creepers()))
        if len(self.creepers) != len(data):
            logger.error(f"Mismatch in creeper counts: {len(self.creepers)} vs {len(data)}")
            return
        for drawer_obj, (coord, state) in zip(self.creepers, data):
            drawer_obj.update(coord, steps, state)
        self.app.simulation.run_update_field()
        logger.info("Creepers updated.")

    def draw_creepers(self, drawer):
        for index, creeper in enumerate(self.creepers):
            if entity_within_bounds(creeper, drawer):
                try:
                    logger.debug(f"Drawing creeper {index}: position=({creeper.cur_x}, {creeper.cur_y})")
                    creeper.draw_step(drawer)
                except Exception as e:
                    logger.error(f"Error drawing creeper {index}: {e}")
                    raise
