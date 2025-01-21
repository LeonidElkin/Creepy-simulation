import os
import sys
from unittest.mock import Mock

from creepers_lib import CreeperState, SteveState

from view.units.creeper_drawer import CreeperDrawer, CreepersManager
from view.units.steve_drawer import SteveDrawer, SteveManager

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


class TestCreeper:
    def test_creeper_drawer_initialization(self):
        """Test initialization of CreeperDrawer."""
        mock_drawer = Mock()
        mock_drawer.image_provider.creeper_image_walk = "walk_image"
        mock_drawer.image_provider.creeper_image_born = "born_image"

        creeper = CreeperDrawer((0, 0), CreeperState.Walk, mock_drawer)

        assert creeper.cur_x == 0
        assert creeper.cur_y == 0
        assert creeper.state == CreeperState.Walk
        assert creeper.image == "walk_image"

    def test_creeper_drawer_update(self):
        """Test the update method of CreeperDrawer."""
        mock_drawer = Mock()
        mock_drawer.image_provider.creeper_image_walk = "walk_image"
        creeper = CreeperDrawer((0, 0), CreeperState.Walk, mock_drawer)

        creeper.update((10, 10), 5, CreeperState.Walk)

        assert creeper.target_x == 10
        assert creeper.target_y == 10
        assert creeper.steps_left == 5

        creeper.update((20, 20), 5, CreeperState.Born)
        assert creeper.target_x == 20
        assert creeper.target_y == 20
        assert creeper.steps_left == 0

    def test_creepers_manager_initialization(self):
        """Test initialization of CreepersManager."""
        mock_app = Mock()
        mock_manager = Mock()
        mock_manager.get_creepers.return_value = [Mock(get_coord=lambda: (0, 0), get_state=lambda: CreeperState.Walk)]
        creepers_manager = CreepersManager(mock_app, mock_manager, (5, 5))

        assert len(creepers_manager.creepers) == 1
        assert creepers_manager.creepers[0].cur_x == 5
        assert creepers_manager.creepers[0].cur_y == 5

    def test_creepers_manager_update(self):
        """Test the update_creepers method."""
        mock_app = Mock()
        mock_manager = Mock()
        mock_manager.get_creepers.return_value = [Mock(get_coord=lambda: (0, 0), get_state=lambda: CreeperState.Walk)]
        creepers_manager = CreepersManager(mock_app, mock_manager, (5, 5))

        mock_manager.get_creepers.return_value = [Mock(get_coord=lambda: (10, 10), get_state=lambda: CreeperState.Born)]
        creepers_manager.update_creepers(steps=10)

        assert creepers_manager.creepers[0].target_x == 15
        assert creepers_manager.creepers[0].target_y == 15


class TestSteve:
    def test_steve_drawer_initialization(self):
        """Test initialization of SteveDrawer."""
        mock_drawer = Mock()
        mock_drawer.image_provider.steve = "steve_image"
        steve = SteveDrawer((0, 0), SteveState.Walk, mock_drawer)

        assert steve.cur_x == 0
        assert steve.cur_y == 0
        assert steve.image == "steve_image"

    def test_steve_drawer_update(self):
        """Test the update method of SteveDrawer."""
        mock_drawer = Mock()
        mock_drawer.image_provider.steve = "steve_image"
        steve = SteveDrawer((0, 0), SteveState.Walk, mock_drawer)

        steve.update((10, 10), 5, SteveState.Born)

        assert steve.target_x == 10
        assert steve.target_y == 10
        assert steve.steps_left == 5

    def test_steve_manager_initialization(self):
        """Test initialization of SteveManager."""
        mock_app = Mock()
        mock_manager = Mock()
        mock_manager.get_steves.return_value = [Mock(get_coord=lambda: (0, 0), get_state=lambda: SteveState.Walk)]
        steve_manager = SteveManager(mock_app, mock_manager, (5, 5))

        assert len(steve_manager.steves) == 1
        assert steve_manager.steves[0].cur_x == 5
        assert steve_manager.steves[0].cur_y == 5

    def test_steve_manager_update(self):
        """Test the update_steves method."""
        mock_app = Mock()
        mock_manager = Mock()
        mock_manager.get_steves.return_value = [Mock(get_coord=lambda: (0, 0), get_state=lambda: SteveState.Walk)]
        steve_manager = SteveManager(mock_app, mock_manager, (5, 5))

        mock_manager.get_steves.return_value = [Mock(get_coord=lambda: (10, 10), get_state=lambda: SteveState.Dead)]
        steve_manager.update_steves(steps=10)

        assert steve_manager.steves[0].target_x == 15
        assert steve_manager.steves[0].target_y == 15
