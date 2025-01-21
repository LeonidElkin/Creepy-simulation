from unittest.mock import Mock, patch

import pygame
import pytest

from view.block import Block
from view.view import DrawExplosion, DrawSparkle, SimulationView


class TestView:
    @pytest.fixture
    def simulation_view(self):
        """Создаёт объект SimulationView для тестов."""
        return SimulationView(width=800, height=600)

    def test_simulation_view_initialization(self, simulation_view):
        """
        Test initialization of SimulationView.
        """
        assert simulation_view.width == 800
        assert simulation_view.height == 600
        assert simulation_view.zoom_level == 1.0
        assert simulation_view.offset_x == 0
        assert simulation_view.offset_y == 0
        assert simulation_view.running_game is None

    def test_simulation_view_handle_event_mouse_zoom(self, simulation_view):
        """Tests mouse handling of zoom events."""
        simulation_view.start_game()
        zoom_in_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 4})
        zoom_out_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 5})

        simulation_view.handle_event(zoom_in_event)
        assert simulation_view.zoom_level > 1.0, "Zoom level should increase after scroll up"

        simulation_view.handle_event(zoom_out_event)
        assert simulation_view.zoom_level == 1.0, "Zoom level should return to 1.0 after scroll down"

    def test_simulation_view_create_block(self, simulation_view):
        """
        Test creation of a block in SimulationView on right mouse click.
        """
        simulation_view.start_game()
        right_click_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"button": 3, "pos": (150, 150)})
        simulation_view.handle_event(right_click_event)

        assert len(simulation_view.waiting_blocks) > 0, "Block should be created on right mouse click"
        block = simulation_view.waiting_blocks[0]
        assert isinstance(block, Block), "Created object should be an instance of Block"


class TestAnimation:
    def test_draw_explosion_with_mocked_timer(self):
        """
        Test DrawExplosion animation with mocked timer.
        """
        points = [(100, 100), (200, 200)]
        explosion = DrawExplosion(points)

        mock_drawer = Mock()
        mock_drawer.zoom_level = 1
        mock_drawer.offset_x = 0
        mock_drawer.offset_y = 0
        mock_drawer.image_provider.explosion_frames = [pygame.Surface((10, 10)) for _ in range(3)]

        with patch("pygame.time.get_ticks", side_effect=[0, 200, 400, 600]):
            explosion.explosion_timer = 0

            assert explosion(mock_drawer) is True, "Explosion animation should be ongoing at frame 0"
            assert explosion(mock_drawer) is True, "Explosion animation should be ongoing at frame 1"
            assert explosion(mock_drawer) is False, "Explosion animation should complete at frame 2"
            assert explosion(mock_drawer) is False, "Explosion animation should remain completed"

    def test_draw_sparkle_with_mocked_timer(self):
        """Tests the rendering of spark animations with timer emulation."""
        points = [(50, 50)]
        sparkle = DrawSparkle(points)

        mock_drawer = Mock()
        mock_drawer.zoom_level = 1
        mock_drawer.offset_x = 0
        mock_drawer.offset_y = 0
        mock_drawer.image_provider.sparkle_frames = [pygame.Surface((5, 5)) for _ in range(3)]

        # Проверяем, что кадры доступны
        assert len(mock_drawer.image_provider.sparkle_frames) > 0, "Sparkle frames must not be empty"

        # Эмулируем вызовы таймера
        with patch("pygame.time.get_ticks", side_effect=[0, 200, 400, 600]):
            sparkle.sparkle_timer = 0  # Синхронизация таймера

            # Первый кадр
            assert sparkle(mock_drawer) is True, "Sparkle animation should be ongoing at frame 0"
            # Второй кадр
            assert sparkle(mock_drawer) is True, "Sparkle animation should be ongoing at frame 1"
            # Завершение
            assert sparkle(mock_drawer) is False, "Sparkle animation should complete at frame 2"
            # После завершения
            assert sparkle(mock_drawer) is False, "Sparkle animation should remain completed"
