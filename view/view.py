import os
import sys
from copy import copy

import pygame
import pygame_gui
from creepers import DistFunc

from view import creeper_drawer as drw
from view import image_provider, ui_elems

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
        if pygame.time.get_ticks() - self.explosion_timer > timer:  # 100 ms between frames
            self.explosion_frame_index += 1
            self.explosion_timer = pygame.time.get_ticks()
        return self.explosion_frame_index > frame_count

    def __call__(self, drawer):
        if not self.points:
            return False
        if self._update_frame(len(drawer.images.explosion_frames) - 1):
            return False
        for i in self.points:
            drawer.screen.blit(drawer.images.explosion_frames[self.explosion_frame_index], i)
        return True


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
        self.will_explodes = set()
        self.explode_drawer = DrawExplosion(set())

        self.func_type_map = {
            "Polar": DistFunc.Polar,
            "Euclid": DistFunc.Euclid,
            "Manhattan": DistFunc.Manhattan,
        }
        self.dist_func = self.func_type_map["Polar"]

        self.creepers_provider = None
        # UI elements
        self.ui = ui_elems.UiManager(self)

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
        self.creepers_provider = drw.CreepersManager(self, (self.center_x, self.center_y))

    def draw_background(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((255, 255, 255))

    def run(self):
        running = True
        update_time = 60
        while running:
            time_delta = self.clock.tick(update_time) / 1000.0
            for event in pygame.event.get():
                running = self.handle_event(event)  # Обработка события
                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.draw_background()

            if self.creepers_provider:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_update_time >= self.thao:
                    self.explodes_drawer = DrawExplosion(copy(self.will_explodes))
                    self.will_explodes = set()
                    self.creepers_provider.update_creepers(max(1, self.thao // 16), self)
                    self.last_update_time = pygame.time.get_ticks()
                self.creepers_provider.draw_creepers(self)
                self.explodes_drawer(self)

            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Simulation().run()
