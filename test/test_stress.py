import os
import sys

import creepers_lib
import pygame

from view.view import SimulationView

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def test_stress_creepers_interaction():
    """
    Stress test: Check interactions and updates for a large number of creepers.
    """
    creepers_count = 1000000  # Большое количество криперов
    simulation_fabric = creepers_lib.SimulationFabric()
    simulation_fabric.set_field_params((-100, -100), (100, 100), creepers_lib.DistFunc.Euclid)
    simulation_fabric.set_creeper_params(move_radius=10, explode_radius=5, count=creepers_count)
    simulation_fabric.set_steve_params(move_radius=15, count=10)
    simulation = simulation_fabric.build()

    creepers_manager = simulation.get_creepers_manager()
    initial_positions = [creeper.get_coord() for creeper in creepers_manager.get_creepers()]
    initial_states = [creeper.get_state() for creeper in creepers_manager.get_creepers()]

    for _ in range(100):
        simulation.run_update_field()
        simulation.wait_update_field()

    updated_positions = [creeper.get_coord() for creeper in creepers_manager.get_creepers()]
    updated_states = [creeper.get_state() for creeper in creepers_manager.get_creepers()]

    assert initial_positions != updated_positions, "Creepers' positions should change after multiple updates"

    assert any(
        state != initial_state for state, initial_state in zip(updated_states, initial_states)
    ), "At least one creeper's state should change after multiple updates"

    assert any(
        state == creepers_lib.CreeperState.Explodes for state in updated_states
    ), "At least one creeper should be in the Explodes state after interactions"


def test_stress_creepers_and_steves_interaction():
    """
    Stress test: Simulate interactions between a large number of creepers and Steves.
    """
    creepers_count = 5000
    steves_count = 5000
    simulation_fabric = creepers_lib.SimulationFabric()
    simulation_fabric.set_field_params((-200, -200), (200, 200), creepers_lib.DistFunc.Euclid)
    simulation_fabric.set_creeper_params(move_radius=10, explode_radius=5, count=creepers_count)
    simulation_fabric.set_steve_params(move_radius=15, count=steves_count)
    simulation = simulation_fabric.build()

    creepers_manager = simulation.get_creepers_manager()
    steves_manager = simulation.get_steves_manager()

    for _ in range(100):
        simulation.run_update_field()
        simulation.wait_update_field()

    creeper_states = [creeper.get_state() for creeper in creepers_manager.get_creepers()]
    steve_states = [steve.get_state() for steve in steves_manager.get_steves()]

    assert any(
        state == creepers_lib.CreeperState.Explodes for state in creeper_states
    ), "Some creepers should have exploded after interactions"

    assert all(
        state == creepers_lib.SteveState.Dead for state in steve_states
    ), "Some Steves should have died after interactions with creepers"


def test_stress_limited_space():
    """
    Stress test: Simulate a dense environment with many entities in a small space.
    """
    creepers_count = 50000
    steves_count = 5000
    simulation_fabric = creepers_lib.SimulationFabric()
    simulation_fabric.set_field_params((-10, -10), (10, 10), creepers_lib.DistFunc.Euclid)
    simulation_fabric.set_creeper_params(move_radius=2, explode_radius=1, count=creepers_count)
    simulation_fabric.set_steve_params(move_radius=2, count=steves_count)
    simulation = simulation_fabric.build()

    for _ in range(100):
        simulation.run_update_field()
        simulation.wait_update_field()

    creepers_manager = simulation.get_creepers_manager()
    steves_manager = simulation.get_steves_manager()

    assert len(creepers_manager.get_creepers()) > 0, "Creepers should still exist in the simulation"
    assert len(steves_manager.get_steves()) > 0, "Steves should still exist in the simulation"


def test_stress_rendering():
    """
    Stress test: Render a large number of creepers and Steves.
    """
    creepers_count = 10000
    steves_count = 10000
    simulation_fabric = creepers_lib.SimulationFabric()
    simulation_fabric.set_field_params((-500, -500), (500, 500), creepers_lib.DistFunc.Euclid)
    simulation_fabric.set_creeper_params(move_radius=10, explode_radius=5, count=creepers_count)
    simulation_fabric.set_steve_params(move_radius=15, count=steves_count)
    simulation = simulation_fabric.build()

    pygame.init()
    simulation_view = SimulationView(width=1920, height=1080)
    simulation_view.simulation = simulation
    simulation_view.start_game()

    try:
        start_time = pygame.time.get_ticks()
        for _ in range(10):
            simulation_view.screen.fill((0, 0, 0))
            simulation_view.running_game.creepers_manager.draw_creepers(simulation_view)
            simulation_view.running_game.steve_manager.draw_steves(simulation_view)
            pygame.display.flip()

        end_time = pygame.time.get_ticks()
        duration = end_time - start_time

        assert duration < 5000, f"Rendering took too long: {duration}ms"
    finally:
        pygame.quit()


def test_stress_simulation_run():
    """
    Stress test: Run the full simulation with a large number of creepers and Steves.
    """
    creepers_count = 50000
    steves_count = 2000

    # Настройка симуляции
    simulation_fabric = creepers_lib.SimulationFabric()
    simulation_fabric.set_field_params((-1000, -1000), (1000, 1000), creepers_lib.DistFunc.Euclid)
    simulation_fabric.set_creeper_params(move_radius=10, explode_radius=5, count=creepers_count)
    simulation_fabric.set_steve_params(move_radius=15, count=steves_count)
    simulation = simulation_fabric.build()

    pygame.init()
    simulation_view = SimulationView(width=1920, height=1080)
    simulation_view.simulation = simulation
    simulation_view.thao = 1000

    # Настраиваем параметры отрисовки
    simulation_view.creepers_params.creeper_count = creepers_count
    simulation_view.steve_params.count = steves_count
    simulation_view.start_game()

    try:
        start_time = pygame.time.get_ticks()
        max_duration = 100000

        simulation_view.start_game()

        while pygame.time.get_ticks() - start_time < max_duration:
            for event in pygame.event.get():
                simulation_view.handle_event(event)

            simulation_view.manager.update(1 / 60.0)
            simulation_view.running_game.algo_update(simulation_view.thao)

            simulation_view.screen.fill((0, 0, 0))
            simulation_view.running_game.creepers_manager.draw_creepers(simulation_view)
            simulation_view.running_game.steve_manager.draw_steves(simulation_view)
            pygame.display.flip()
    finally:
        pygame.quit()

    assert simulation_view.running_game is not None, "Simulation should initialize correctly"
