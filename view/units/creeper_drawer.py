from dataclasses import dataclass

from creepers_lib import CreeperState

from view.logger import logger
from view.units.entity_drawer import EntityDrawer, entity_within_bounds


@dataclass
class CreeperParams:
    """
    @class CreeperParams
    @brief Configuration parameters for creepers.

    Defines the default parameters such as radius, explosion radius, and creeper count.
    """

    radius: float = 20
    radius_explosion: float = 10
    creeper_count: int = 10


class CreeperDrawer(EntityDrawer):
    """
    @class CreeperDrawer
    @brief Manages the rendering and state transitions of individual creepers.

    The CreeperDrawer class extends the EntityDrawer to handle specific behaviors
    and visuals associated with creepers.
    """

    def __init__(self, position: tuple[float, float], state: CreeperState, drawer):
        """
        Initializes a CreeperDrawer object.

        @param position: The initial position of the creeper.
        @param state: The current state of the creeper (e.g., Walk, Born, Sleep).
        @param drawer: The drawer object managing rendering.
        """
        super().__init__(position, None, drawer)
        self.dx = self.dy = 0
        self.state = state
        self.image = self.get_img(state, None)

    def get_img(self, state, prev):
        """
        Updates the image associated with the creeper based on its current state.

        @param prev: The previous state of the creeper.
        """
        if prev == CreeperState.Born or prev is None:
            prev = CreeperState.Walk

        if state == CreeperState.Walk:
            image = self.drawer.image_provider.creeper_image_walk
        elif state == CreeperState.Born:
            image = self.drawer.image_provider.creeper_image_born
        elif state == CreeperState.Sleep:
            image = self.drawer.image_provider.creeper_image_sleep
        elif state == CreeperState.Hissing:
            image = self.drawer.image_provider.creeper_image_hiss
        elif state == CreeperState.GoToSteve:
            image = self.drawer.image_provider.creeper_image_gotosteve
        elif state == CreeperState.Bonk:
            image = self.drawer.image_provider.creeper_image_bonk
        elif state in (CreeperState.Explodes, CreeperState.Dead):
            image = self.get_img(prev, None)
        else:
            logger.error(f"Unknown creeper state, draw bonk: {self.state.name}")
            image = self.drawer.image_provider.creeper_image_gotosteve
        return image

    def update(self, new_position: tuple[float, float], steps, new_state=None):
        """
        Updates the position and state of the creeper.

        @param new_position: The new position of the creeper.
        @param steps: frames between algo updates.
        @param new_state: The new state of the creeper.
        """
        if new_state == CreeperState.Born:
            self.cur_x, self.cur_y = new_position
            self.target_x, self.target_y = new_position
            self.steps_left = 0
        else:
            self.target_x, self.target_y = new_position
            self._set_target(steps)

        self.image = self.get_img(new_state, self.state)
        self.state = new_state

        if new_state == CreeperState.Explodes:
            self.drawer.will_explodes.add(new_position)

        if new_state == CreeperState.Bonk and self.state != new_state:
            self.drawer.will_sparkle.add(new_position)
        self.state = new_state


class CreepersManager:
    """
    @class CreepersManager
    @brief Handles the collection of creepers and their interactions.

    The CreepersManager class manages a collection of CreeperDrawer objects,
    updating their states and rendering them within the simulation.
    """

    def __init__(self, app, manager, position_shift):
        """
        Initializes the CreepersManager object.

        @param app: The application managing the simulation.
        @param manager: The underlying creepers manager from the simulation library.
        @param position_shift: The positional offset for rendering creepers.
        """
        self.manager = manager
        self.shift = position_shift
        self.creepers = [
            CreeperDrawer(coord, state, app) for coord, state in self._creepers2data(self.manager.get_creepers())
        ]

    def _creepers2data(self, creepers):
        """
        Converts creepers data into coordinates and states, applying positional shift.

        @param creepers: The list of creepers from the simulation library.
        @return: A generator yielding shifted coordinates and states for each creeper.
        """

        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        # data = [(shift_coord(steve.get_coord()), steve.get_state()) for steve in creepers]
        # logger.info(f"Processed creeper data: {data}")
        return ((shift_coord(creeper.get_coord()), creeper.get_state()) for creeper in creepers)

    def update_creepers(self, steps):
        """
        Updates the states and positions of all creepers.

        @param steps: The number of steps for updating creeper positions.
        """
        logger.debug(f"Updating creepers: total={len(self.creepers)}")
        data = list(self._creepers2data(self.manager.get_creepers()))
        if len(self.creepers) != len(data):
            logger.error(f"Mismatch in creeper counts: {len(self.creepers)} vs {len(data)}")
            return
        for drawer_obj, (coord, state) in zip(self.creepers, data):
            drawer_obj.update(coord, steps, state)
        logger.info("Creepers updated.")

    def draw_creepers(self, drawer):
        """
        Renders all creepers on the provided drawer surface.

        @param drawer: The drawing surface or manager responsible for rendering.
        """
        for index, creeper in enumerate(self.creepers):
            if entity_within_bounds(creeper, drawer):
                try:
                    # logger.debug(f"Drawing creeper {index}: position=({creeper.cur_x}, {creeper.cur_y})")
                    creeper.draw_step()
                except Exception as e:
                    logger.error(f"Error drawing creeper {index}: {e}")
                    raise
