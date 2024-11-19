import os
import sys

import image_provider
import pygame
import pygame_gui
import ui_elems
from creeper_drawer import CreepersManager
from creepers import DistFunc

package_path = os.path.dirname(os.path.abspath(__file__))
h, _ = os.path.split(package_path)
sys.path.append(h)
sys.path.append(package_path)


class Simulation:
    def __init__(self, width=1920, height=1080):
        pygame.init()
        self.width = width
        self.height = height
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Creepy Simulation")
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((width, height))
        self.images = image_provider.ImageProvider()
        self.callbacks_animations = []

        try:
            self.background_image = pygame.transform.scale(self.images.background_image, (self.width, self.height))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background_image = None

        self.creeper_count = 10
        self.thao = 2000
        self.radius = 1
        self.radius_explosion = 1
        self.last_update_time = 0

        self.func_type_map = {
            "Polar": DistFunc.Polar,
            "Euclid": DistFunc.Euclid,
            "Manhattan": DistFunc.Manhattan,
        }
        self.dist_func = self.func_type_map["Polar"]

        self.creepers_provider = None
        # UI elements
        self.ui = ui_elems.UiManager(self)

    def register_callback_animation(self, callback):
        self.callbacks_animations.append(callback)

    def draw_callbacks_animations(self):
        self.callbacks_animations = [ani for ani in self.callbacks_animations if ani(self)]

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False  # Выход из игры
        elif event.type in [
            pygame_gui.UI_HORIZONTAL_SLIDER_MOVED,
            pygame_gui.UI_DROP_DOWN_MENU_CHANGED,
            pygame_gui.UI_BUTTON_PRESSED,
        ] and not self.ui.handle_event(event):
            print("unknown ui event")
        return True

    def start_game(self):
        # Инициализация поля и криперов
        self.creepers_provider = CreepersManager(self, (self.center_x, self.center_y))

    def draw_background(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((255, 255, 255))

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                running = self.handle_event(event)  # Обработка события
                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.draw_background()

            if self.creepers_provider:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_update_time >= self.thao:
                    self.last_update_time = current_time
                    self.creepers_provider.update_creepers(max(1, self.thao // 16))

                self.creepers_provider.draw_creepers(self)

            # Рисуем интерфейс
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Simulation().run()
