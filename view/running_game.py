from dataclasses import astuple

import creepers_lib

from view.logger import logger
from view.units.creeper_drawer import CreepersManager
from view.units.steve_drawer import SteveManager


class RunningGame:
    """
    @class RunningGame
    @brief Manages the main game loop and interactions within the simulation.

    The RunningGame class handles the initialization, management, and updates of the simulation,
    including managing creepers and Steves.
    """

    simulation: creepers_lib.Simulation

    def __init__(self, app, position_shift):
        """
        Initializes the RunningGame object.

        @param app: The main application object providing game settings and context.
        @param position_shift: The positional offset for rendering objects.
        """
        self.app = app
        self.offset = position_shift
        self.start_game()
        self.creepers_manager = CreepersManager(app, self.simulation.get_creepers_manager(), position_shift)
        self.steve_manager = SteveManager(app, self.simulation.get_steves_manager(), position_shift)
        self.simulation.run_update_field()
        self.last_update_time = 0

    def start_game(self):
        """
        Initializes the simulation with the configured parameters.

        Sets up the simulation field, distance function, and parameters for creepers and Steves.
        """
        simulationFabric = creepers_lib.SimulationFabric()

        width = self.app.width
        height = self.app.height
        dist_func = self.app.dist_func
        simulationFabric.set_field_params((-width // 2, -height // 2), (width // 2, height // 2), dist_func)
        logger.info(f"Field params set: width={width}, height={height}, dist_func={dist_func}")
        simulationFabric.set_creeper_params(*astuple(self.app.creepers_params))
        simulationFabric.set_steve_params(*astuple(self.app.steve_params))

        self.app.blocks.extend(self.app.waiting_blocks)
        self.app.waiting_blocks = []
        for block in self.app.blocks:
            simulationFabric.set_bedrock(*block.get_borders(self.offset))
        print(self.app.creepers_params)

        self.simulation = simulationFabric.build()
        logger.info("Simulation initialized")

    def algo_update(self, thao):
        """
        Updates the simulation state and manages rendering of objects.

        @param current_time: The current time in milliseconds.
        """
        self.simulation.wait_update_field()
        for block in self.app.waiting_blocks:
            self.simulation.set_bedrock(*block.get_borders(self.offset))
        self.app.blocks.extend(self.app.waiting_blocks)
        self.app.waiting_blocks = []

        self.steve_manager.update_steves(max(1, thao // 16))
        self.creepers_manager.update_creepers(max(1, thao // 16))
        self.simulation.run_update_field()

    def step_draw(self):
        """
        Renders the simulation objects on the given surface.

        @param surface: The pygame surface to draw on.
        """
        self.creepers_manager.draw_creepers(self.app)
        self.steve_manager.draw_steves(self.app)
