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
        self.set_img(state)

    def set_img(self, prev):
        """
        Updates the image associated with the creeper based on its current state.

        @param prev: The previous state of the creeper.
        """
        if self.state == CreeperState.Walk:
            self.image = self.drawer.image_provider.creeper_image_walk
        elif self.state == CreeperState.Born:
            self.image = self.drawer.image_provider.creeper_image_born
        elif self.state == CreeperState.Sleep:
            self.image = self.drawer.image_provider.creeper_image_sleep
        elif self.state == CreeperState.Hissing:
            self.image = self.drawer.image_provider.creeper_image_hiss
        elif self.state == CreeperState.GoToSteve:
            self.image = self.drawer.image_provider.creeper_image_gotosteve
        elif self.state == CreeperState.Bonk:
            self.image = self.drawer.image_provider.creeper_image_bonk
        elif self.state in (CreeperState.Explodes, CreeperState.Dead):
            self.image = prev
        else:
            logger.error(f"Unknown creeper state, draw bonk: {self.state.name}")
            self.image = self.drawer.image_provider.creeper_image_gotosteve

    def update(self, new_position: tuple[float, float], steps, state=None):
        """
        Updates the position and state of the creeper.

        @param position: The new position of the creeper.
        @param state: The new state of the creeper.
        """
        prev = self.image
        self.state = state
        if state == CreeperState.Born:
            self.cur_x, self.cur_y = new_position
            self.target_x, self.target_y = new_position
            self.steps_left = 0
        else:
            self.target_x, self.target_y = new_position
            self._set_target(steps)

        self.set_img(prev)

        if state == CreeperState.Explodes:
            self.drawer.will_explodes.add(new_position)

        if state == CreeperState.Bonk and prev != self.image:
            self.drawer.will_sparkle.add(new_position)


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