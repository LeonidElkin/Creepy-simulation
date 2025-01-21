import os
import sys

import creepers_lib
import pygame
import pytest

from view.view import SimulationView

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


@pytest.fixture
def simulation():
    simulation_fabric = creepers_lib.SimulationFabric()
    simulation_fabric.set_field_params((-10, -10), (10, 10), creepers_lib.DistFunc.Euclid)
    simulation_fabric.set_creeper_params(move_radius=10, explode_radius=5, count=20)
    simulation_fabric.set_steve_params(move_radius=15, count=5)
    simulation = simulation_fabric.build()

    return simulation


@pytest.fixture
def simulation_view(simulation):
    return SimulationView(width=50, height=50)


def test_creepers_update(simulation, simulation_view):
    """
    Test that creepers update their positions after a simulation step.
    """
    creepers_manager = simulation.get_creepers_manager()
    initial_positions = [creeper.get_coord() for creeper in creepers_manager.get_creepers()]

    simulation.run_update_field()
    simulation.wait_update_field()
    updated_positions = [creeper.get_coord() for creeper in creepers_manager.get_creepers()]

    assert initial_positions != updated_positions, "Creepers' positions should change after update"


def test_creepers_interaction(simulation):
    """
    Test that creepers update their state after interaction.
    """
    creepers_manager = simulation.get_creepers_manager()

    simulation.run_update_field()
    simulation.wait_update_field()

    for creeper in creepers_manager.get_creepers():
        assert creeper.get_state() is not None, "Creeper's's state should be updated"


def test_steves_interaction(simulation):
    """
    Test that Steves update their state after interaction.
    """
    steves_manager = simulation.get_steves_manager()

    simulation.run_update_field()

    for steve in steves_manager.get_steves():
        assert steve.get_state() is not None, "Steve's state should be updated"


def test_simulation_entity_counts(simulation):
    """
    Test that the number of creepers and Steves matches the simulation parameters.
    """
    creepers_manager = simulation.get_creepers_manager()
    steves_manager = simulation.get_steves_manager()

    assert len(creepers_manager.get_creepers()) == 20, "Creeper count should match simulation parameters"
    assert len(steves_manager.get_steves()) == 5, "Steve count should match simulation parameters"


def test_rendering(simulation_view):
    simulation_view.start_game()
    simulation_view.draw_background()

    assert simulation_view.running_game is not None, "Game should start successfully"


def test_game_restart(simulation_view):
    """
    Test that restarting the game resets simulation parameters.
    """
    simulation_view.start_game()
    initial_creeper_count = simulation_view.creepers_params.creeper_count

    # Эмулировать изменение параметра
    simulation_view.creepers_params.creeper_count = 10

    # Перезапустить игру
    simulation_view.start_game()

    assert (
        simulation_view.creepers_params.creeper_count == initial_creeper_count
    ), "Creeper count should reset after restarting the game"


def test_zoom_and_camera_movement(simulation_view):
    """
    Test zoom level.
    """
    simulation_view.start_game()

    for _ in range(3):  # Увеличиваем зум трижды
        zoom_in_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 4, "pos": (400, 300)})
        simulation_view.handle_event(zoom_in_event)

    assert simulation_view.zoom_level > 1, f"Zoom level should be greater than 1.1, got {simulation_view.zoom_level}"
