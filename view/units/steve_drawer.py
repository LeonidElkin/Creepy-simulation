from dataclasses import dataclass

from creepers_lib import SteveState

from view.logger import logger
from view.units.entity_drawer import EntityDrawer, entity_within_bounds


@dataclass
class SteveParams:
    """
    @class SteveParams
    @brief Configuration parameters for Steves.

    Defines the default parameters such as radius and count.
    """

    radius: float = 20
    count: int = 0


class SteveDrawer(EntityDrawer):
    """
    @class SteveDrawer
    @brief Manages the rendering and state transitions of individual Steves.

    The SteveDrawer class extends the EntityDrawer to handle specific behaviors
    and visuals associated with Steves.
    """

    def __init__(self, position: tuple[float, float], state: SteveState, drawer):
        """
        Initializes a SteveDrawer object.

        @param position: The initial position of the Steve.
        @param state: The current state of the Steve (e.g., Walk, Born, Dead).
        @param drawer: The drawer object managing rendering.
        """
        super().__init__(position, None, drawer)
        self.dx = self.dy = 0
        self.state = state
        self.image = self.get_img(state)

    def get_img(self, state):
        """
        Updates the image associated with the Steve based on its current state.
        """
        if state == SteveState.Dead:
            image = self.drawer.image_provider.steve_image_grave
        elif state == SteveState.Walk:
            image = self.drawer.image_provider.steve
        else:
            logger.error(f"invalid steve state {self.state}")
            image = self.drawer.image_provider.bedrock
        return image

    def update(self, new_position: tuple[float, float], steps, new_state=None):
        """
        Updates the position and state of the Steve.

        @param new_position: The new position of the Steve.
        @param steps: Number of steps to reach the target position.
        @param new_state: The new state of the Steve.
        """

        self.state = new_state
        self.target_x, self.target_y = new_position
        self._set_target(steps)

        self.image = self.get_img(new_state)


class SteveManager:
    """
    @class SteveManager
    @brief Handles the collection of Steves and their interactions.

    The SteveManager class manages a collection of SteveDrawer objects,
    updating their states and rendering them within the simulation.
    """

    def __init__(self, app, manager, position_shift):
        """
        Initializes the SteveManager object.

        @param app: The application managing the simulation.
        @param manager: The underlying Steve manager from the simulation library.
        @param position_shift: The positional offset for rendering Steves.
        """
        self.manager = manager
        self.shift = position_shift
        steves_data = self.manager.get_steves()
        if not steves_data:
            logger.error("No steve data received from simulation!")
        self.steves = [SteveDrawer(coord, state, app) for coord, state in self._steves2data(self.manager.get_steves())]

    def _steves2data(self, steves):
        """
        Converts Steves data into coordinates and states, applying positional shift.

        @param steves: The list of Steves from the simulation library.
        @return: A generator yielding shifted coordinates and states for each Steve.
        """

        def shift_coord(coord):
            return coord[0] + self.shift[0], coord[1] + self.shift[1]

        # data = [(shift_coord(steve.get_coord()), steve.get_state()) for steve in steves]
        # logger.info(f"Processed steves data: {data}")
        return ((shift_coord(steve.get_coord()), steve.get_state()) for steve in steves)

    def update_steves(self, steps):
        """
        Updates the states and positions of all Steves.

        @param steps: The number of steps for updating Steve positions.
        """
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
        """
        Renders all Steves on the provided drawer surface.

        @param drawer: The drawing surface or manager responsible for rendering.
        """
        for index, steve in enumerate(self.steves):
            if entity_within_bounds(steve, drawer):
                try:
                    # logger.debug(f"Drawing steve {index}: position=({steve.cur_x}, {steve.cur_y})")
                    steve.draw_step()
                except Exception as e:
                    logger.error(f"Error drawing steve {index}: {e}")
                    raise
