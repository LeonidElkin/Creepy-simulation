from view.units.creeper_drawer import CreepersManager
from view.units.steve_drawer import SteveManager


class RunningGame:
    def __init__(self, simulation, position_shift):
        self.creepers_manager = CreepersManager(simulation, position_shift)
        self.steve_manager = SteveManager(simulation, position_shift)
