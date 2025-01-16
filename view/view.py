import os
import sys
from copy import copy

import pygame
import pygame_gui
from creepers_lib import DistFunc

from view.block import Block
from view.image_provider import ImageProvider
from view.logger import logger
from view.running_game import RunningGame
from view.units.creeper_drawer import CreeperParams
from view.units.steve_drawer import SteveParams

package_path = os.path.dirname(os.path.abspath(__file__))
h, _ = os.path.split(package_path)
sys.path.append(h)
sys.path.append(package_path)


class DrawExplosion:
    def __init__(self, points):
        self.explosion_frame_index = 0
        self.points = points
        self.explosion_timer = pygame.time.get_ticks()

    def _update_frame(self, frame_count):
        timer = 100
        if pygame.time.get_ticks() - self.explosion_timer > timer:
            self.explosion_frame_index += 1
            self.explosion_timer = pygame.time.get_ticks()
        return self.explosion_frame_index > frame_count

    def __call__(self, drawer):
        if not self.points:
            return False
        if self._update_frame(len(drawer.image_provider.explosion_frames) - 1):
            return False

        for i in self.points:
            drawer.screen.blit(drawer.image_provider.explosion_frames[self.explosion_frame_index], i)
        # frame = drawer.image_provider.explosion_frames[self.explosion_frame_index]
        # scaled_size = int(frame.get_width() * drawer.zoom_level), int(frame.get_height() * drawer.zoom_level)
        # scaled_frame = pygame.transform.scale(frame, scaled_size)
        #
        # for point in self.points:
        #     screen_x = point[0] * drawer.zoom_level + drawer.offset_x
        #     screen_y = point[1] * drawer.zoom_level + drawer.offset_y
        #     drawer.screen.blit(scaled_frame, (screen_x, screen_y))

        return True


class DrawSparkle:
    def __init__(self, points):
        self.sparkle_frame_index = 0
        self.points = points
        self.sparkle_timer = pygame.time.get_ticks()

    def _update_frame(self, frame_count):
        timer = 100
        if pygame.time.get_ticks() - self.sparkle_timer > timer:
            self.sparkle_frame_index += 1
            self.sparkle_timer = pygame.time.get_ticks()
        return self.sparkle_frame_index > frame_count

    def __call__(self, drawer):
        if not self.points:
            return False
        if self._update_frame(len(drawer.images.sparkle_frames) - 1):
            return False

        frame = drawer.images.explosion_frames[self.sparkle_frame_index]
        scaled_size = int(frame.get_width() * drawer.zoom_level), int(frame.get_height() * drawer.zoom_level)
        scaled_frame = pygame.transform.scale(frame, scaled_size)

        for point in self.points:
            screen_x = point[0] * drawer.zoom_level + drawer.offset_x
            screen_y = point[1] * drawer.zoom_level + drawer.offset_y
            drawer.screen.blit(scaled_frame, (screen_x, screen_y))

        return True


class SimulationView:
    def __init__(self, width=1920, height=1080):
        import ui_elems

        pygame.init()
        self.running_game = None
        self.width = width
        self.height = height
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Creepy Simulation")
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((width, height))
        self.image_provider = ImageProvider()
        self.explodes_drawer = DrawExplosion(set())
        # Another objects
        self.blocks = []

        try:
            self.background_image = pygame.transform.scale(
                self.image_provider.background_image, (self.width, self.height)
            )
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background_image.fill((0, 100, 200))
            self.background_image = None

        # Zoom and pan variables
        self.zoom_level = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.dragging = False
        self.last_mouse_pos = None

        # Params
        self.creepers_params = CreeperParams()
        self.steve_params = SteveParams()
        self.thao = 2000
        self.radius = 20
        self.last_update_time = 0
        self.will_explodes = set()

        self.func_type_map = {
            "Polar": DistFunc.Polar,
            "Euclid": DistFunc.Euclid,
            "Manhattan": DistFunc.Manhattan,
        }
        self.dist_func = self.func_type_map["Polar"]

        # UI elements
        self.ui = ui_elems.UiManager(self)
        self.parameters = {
            "radius": self.radius,
            "thao": self.thao,
        }
        self.params = None
        self.simulation = None

    def _handle_mouse_button_down(self, event):
        right_button = 3
        if event.button == 1 and self.zoom_level > 1.0:  # Dragging только при zoom_level > 1.0
            self.dragging = True
            self.last_mouse_pos = event.pos
        elif event.button in (4, 5):  # Zoom in (4) или zoom out (5)
            self._handle_zoom(event)
        elif event.button == right_button:  # Правая кнопка мыши для создания блока
            self._create_block(event)
        return True

    def _handle_mouse_button_up(self, event):
        if event.button == 1:
            self.dragging = False
        return True

    def _handle_mouse_motion(self, event):
        if self.last_mouse_pos and self.zoom_level > 1.0:
            dx = event.pos[0] - self.last_mouse_pos[0]
            dy = event.pos[1] - self.last_mouse_pos[1]

            # Вычисление пределов смещения
            scaled_width = int(self.width * self.zoom_level)
            scaled_height = int(self.height * self.zoom_level)
            max_offset_x = 0
            max_offset_y = 0
            min_offset_x = self.width - scaled_width
            min_offset_y = self.height - scaled_height

            # Применяем смещение c учетом ограничений
            self.offset_x = max(min(self.offset_x + dx, max_offset_x), min_offset_x)
            self.offset_y = max(min(self.offset_y + dy, max_offset_y), min_offset_y)

            self.last_mouse_pos = event.pos
        return True

    def _handle_zoom(self, event):
        previous_zoom = self.zoom_level
        zoom_in = 4
        zoom_factor = 1.1 if event.button == zoom_in else 0.9
        self.zoom_level = max(min(self.zoom_level * zoom_factor, 5.0), 1.0)

        # Координаты мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Смещение до изменения масштаба
        rel_x = (mouse_x - self.offset_x) / previous_zoom
        rel_y = (mouse_y - self.offset_y) / previous_zoom

        # Смещение после изменения масштаба
        self.offset_x = mouse_x - rel_x * self.zoom_level
        self.offset_y = mouse_y - rel_y * self.zoom_level

        # Если возвращаемся к масштабу 1.0, сбросить смещение
        if self.zoom_level == 1.0:
            self.offset_x = 0
            self.offset_y = 0

    def _create_block(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Рассчитываем мировые координаты c учетом зума и смещения
        world_x = (mouse_x - self.offset_x) / self.zoom_level
        world_y = (mouse_y - self.offset_y) / self.zoom_level

        block_size = 50
        grid_x = int(world_x // block_size) * block_size
        grid_y = int(world_y // block_size) * block_size

        self.blocks.append(Block(grid_x, grid_y, block_size))

    def _handle_ui_event(self, event):
        if not self.ui.handle_event(event):
            print("unknown ui event")
        return True

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return self._handle_mouse_button_down(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            return self._handle_mouse_button_up(event)
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            return self._handle_mouse_motion(event)
        elif event.type in [
            pygame_gui.UI_HORIZONTAL_SLIDER_MOVED,
            pygame_gui.UI_DROP_DOWN_MENU_CHANGED,
            pygame_gui.UI_BUTTON_PRESSED,
        ]:
            return self._handle_ui_event(event)
        return True

    def start_game(self):
        logger.debug("Starting game...")
        # Инициализация поля и криперов, Steve
        self.running_game = RunningGame(self, (self.center_x, self.center_y))
        logger.info("Game initialized successfully.")

    def draw_background(self):
        if self.zoom_level < 1.0:  # фон всегда покрывает весь экран
            # Масштабируем фон до размеров экрана
            scaled_background = pygame.transform.scale(self.background_image, (self.width, self.height))
            display_rect = scaled_background.get_rect()
            display_rect.topleft = (0, 0)
        else:
            # Масштабируем фон c учетом текущего зума
            scaled_width = int(self.width * self.zoom_level)
            scaled_height = int(self.height * self.zoom_level)
            scaled_background = pygame.transform.scale(self.background_image, (scaled_width, scaled_height))

            # Учет смещения
            display_rect = scaled_background.get_rect()
            display_rect.topleft = (self.offset_x, self.offset_y)

            # Избегаем белых полей
            display_rect.left = max(min(display_rect.left, 0), self.width - display_rect.width)
            display_rect.top = max(min(display_rect.top, 0), self.height - display_rect.height)

        self.screen.fill((0, 0, 0))  # Устанавливаем черный фон вместо белого
        self.screen.blit(scaled_background, display_rect)

    def run(self):
        running = True
        update_time = 60
        font = pygame.font.SysFont(None, 30)
        while running:
            time_delta = self.clock.tick(update_time) / 1000.0
            for event in pygame.event.get():
                running = self.handle_event(event)  # Обработка события
                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.draw_background()

            for block in self.blocks:
                block.draw(self.screen, self.image_provider.bedrock, self.zoom_level, self.offset_x, self.offset_y)

            if self.running_game:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_update_time >= self.thao:
                    self.explodes_drawer = DrawExplosion(copy(self.will_explodes))
                    self.will_explodes = set()
                    self.running_game.algo_update(self.thao)
                    self.last_update_time = pygame.time.get_ticks()
                self.running_game.step_draw()

                if self.explodes_drawer:
                    self.explodes_drawer(self)

            self.manager.draw_ui(self.screen)

            fps = self.clock.get_fps()
            fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
            self.screen.blit(fps_text, (1820, 10))

            pygame.display.flip()

        pygame.quit()


def run():
    SimulationView().run()


if __name__ == "__main__":
    run()
