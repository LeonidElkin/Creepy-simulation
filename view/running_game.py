from dataclasses import astuple

import creepers_lib

from view.logger import logger
from view.units.creeper_drawer import CreepersManager
from view.units.steve_drawer import SteveManager


class RunningGame:
    def __init__(self, app, position_shift):
        self.app = app
        self.simulation: creepers_lib.Simulation = self.start_game()
        self.creepers_manager = CreepersManager(self.simulation.get_creepers_manager(), position_shift)
        self.steve_manager = SteveManager(self.simulation.get_steves_manager(), position_shift)
        self.simulation.run_update_field()
        self.last_update_time = 0

    def start_game(self):
        simulationFabric = creepers_lib.SimulationFabric()

        width = self.app.width
        height = self.app.height
        dist_func = self.app.dist_func
        simulationFabric.set_field_params((-width // 2, -height // 2), (width // 2, height // 2), dist_func)
        logger.info(f"Field params set: width={width}, height={height}, dist_func={dist_func}")
        simulationFabric.set_creeper_params(*astuple(self.app.creepers_params))
        simulationFabric.set_steve_params(self.app.radius, 10)

        return simulationFabric.build()

    def algo_update(self, thao):
        self.simulation.wait_update_field()
        self.steve_manager.update_steves(max(1, thao // 16))
        self.creepers_manager.update_creepers(max(1, thao // 16))
        self.simulation.run_update_field()

    def step_draw(self):
        self.creepers_manager.draw_creepers(self.app)
        self.steve_manager.draw_steves(self.app)
