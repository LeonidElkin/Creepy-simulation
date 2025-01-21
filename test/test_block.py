import pygame
import pytest

from view.block import Block


class TestBlock:
    @pytest.fixture
    def block(self):
        """Creates a test Block object."""
        return Block(10, 20, 30)

    def test_block_initialization(self, block):
        """Проверяет инициализацию блока."""
        assert block.x == 10, "X-coordinate should be initialized correctly"
        assert block.y == 20, "Y-coordinate should be initialized correctly"
        assert block.size == 30, "Size should be initialized correctly"

    def test_block_contains(self, block):
        """Checks the contains method."""
        # Точка внутри блока
        assert block.contains(15, 25), "Point inside the block should return True"
        # Точка на границе блока
        assert not block.contains(40, 25), "Point on the right edge should return False"
        assert not block.contains(15, 50), "Point on the bottom edge should return False"
        # Точка вне блока
        assert not block.contains(0, 0), "Point outside the block should return False"

    def test_block_get_borders(self, block):
        """Checks the get_borders method."""
        borders = block.get_borders((5, 5))
        assert borders == ((-15, -5), (35, 45)), f"Borders should be ((-15, -5), (35, 45)), got {borders}"

    def test_block_draw(self, block):
        """Checks the draw method."""
        # Создаём тестовый экран и изображение
        pygame.init()
        screen = pygame.Surface((100, 100))
        image = pygame.Surface((30, 30))
        image.fill((255, 0, 0))

        # Эмулируем вызов draw
        block.draw(screen, image, zoom_level=1, offset_x=0, offset_y=0)

        # Проверяем, что блок отрисован
        screen_color = screen.get_at((10, 20))
        assert screen_color == (255, 0, 0, 255), "Block should be drawn on the screen"
        pygame.quit()
