from creepers_lib import CreeperState, DistFunc, SimulationFabric, SteveState


def test_simulation_fabric_build():
    fabric = SimulationFabric()

    fabric.set_field_params((-100, -100), (100, 100), DistFunc.Euclid)

    fabric.set_creeper_params(move_radius=10, explode_radius=5, count=20)

    fabric.set_steve_params(move_radius=15, count=5)

    simulation = fabric.build()

    assert simulation is not None, "Simulation creation failed"


def test_simulation_creepers():
    fabric = SimulationFabric()
    fabric.set_field_params((-50, -50), (50, 50), DistFunc.Polar)
    fabric.set_creeper_params(move_radius=10, explode_radius=5, count=10)
    simulation = fabric.build()

    creepers_manager = simulation.get_creepers_manager()
    creepers = creepers_manager.get_creepers()

    assert len(creepers) == 10, "Incorrect number of creepers"

    for creeper in creepers:
        coord = creeper.get_coord()
        assert isinstance(coord, tuple) and len(coord) == 2, "Invalid creeper coordinates"


def test_simulation_steves():
    fabric = SimulationFabric()
    fabric.set_field_params((-100, -100), (100, 100), DistFunc.Manhattan)
    fabric.set_steve_params(move_radius=20, count=5)
    simulation = fabric.build()

    steves_manager = simulation.get_steves_manager()
    steves = steves_manager.get_steves()

    assert len(steves) == 5, "Incorrect number of Steves"

    for steve in steves:
        coord = steve.get_coord()
        state = steve.get_state()
        assert isinstance(coord, tuple) and len(coord) == 2, "Invalid Steve coordinates"
        assert state in SteveState.__members__.values(), f"Invalid Steve state: {state}"


def test_simulation_async_update():
    fabric = SimulationFabric()
    fabric.set_field_params((-100, -100), (100, 100), DistFunc.Euclid)
    fabric.set_creeper_params(move_radius=10, explode_radius=5, count=20)
    fabric.set_steve_params(move_radius=15, count=5)
    simulation = fabric.build()

    simulation.run_update_field()
    simulation.wait_update_field()

    creepers_manager = simulation.get_creepers_manager()
    steves_manager = simulation.get_steves_manager()

    assert len(creepers_manager.get_creepers()) > 0, "Creepers did not update"
    assert len(steves_manager.get_steves()) > 0, "Steves did not update"


def test_creeper_explodes_state():
    fabric = SimulationFabric()
    creepers_num = 1
    fabric.set_field_params((0, 0), (1, 1), DistFunc.Euclid)
    fabric.set_creeper_params(move_radius=1, explode_radius=5, count=creepers_num)
    fabric.set_steve_params(move_radius=1, count=1)
    simulation = fabric.build()

    simulation.run_update_field()
    simulation.wait_update_field()
    # simulation.run_update_field()
    # simulation.wait_update_field()

    creepers_manager = simulation.get_creepers_manager()
    creepers = creepers_manager.get_creepers()

    explodes_found = any(creeper.get_state() == CreeperState.Explodes for creeper in creepers)
    assert explodes_found, f"No creepers in 'Explodes' state found among {creepers_num} creepers"
