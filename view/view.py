import math
import os
import sys

import pygame
import pygame_gui
from creepers import CreeperState, DistFunc, Field

package_path = os.path.dirname(os.path.abspath(__file__))
h, _ = os.path.split(package_path)
sys.path.append(h)


class CreeperDraw:
    def __init__(self, pos_x, pos_y, explosion_frames=None):
        self.explosion_frames = explosion_frames
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.target_x = pos_x
        self.target_y = pos_y
        self.dx = 0
        self.dy = 0
        self.steps_left = 0
        self.state = CreeperState.Walk
        self.explosion_frame_index = 0
        self.explosion_timer = 0

    def start_explosion(self):
        self.state = CreeperState.Explodes
        self.explosion_frame_index = 0
        self.explosion_timer = pygame.time.get_ticks()

    def update_explosion(self):
        timer = 100
        if self.state == CreeperState.Explodes:
            if pygame.time.get_ticks() - self.explosion_timer > timer:  # 100 ms between frames
                self.explosion_frame_index += 1
                self.explosion_timer = pygame.time.get_ticks()
            if self.explosion_frame_index >= len(self.explosion_frames):
                self.state = CreeperState.Born  # Change to a different state after the explosion
                self.explosion_frame_index = len(self.explosion_frames) - 1  # Keep last frame if needed

    def draw(self, screen, center_x, center_y):
        if self.state == CreeperState.Explodes:
            screen.blit(
                self.explosion_frames[self.explosion_frame_index],
                (int(self.pos_x + center_x), int(self.pos_y + center_y)),
            )

    def set_target(self, target_x, target_y, steps=10):
        if steps <= 0:
            steps = 1  # Минимальное количество шагов
        self.target_x = target_x
        self.target_y = target_y
        self.dx = (self.target_x - self.pos_x) / steps
        self.dy = (self.target_y - self.pos_y) / steps
        self.steps_left = steps
        self.state = CreeperState.Walk

    def update_position(self):
        if self.steps_left > 0:
            if not (math.isnan(self.dx) or math.isnan(self.dy)):
                self.pos_x += self.dx
                self.pos_y += self.dy
            # else:
            # print(
            #     f"Invalid dx/dy values: dx={self.dx}, dy={self.dy}, target_x: {self.target_x},
            #     target_y:{self.target_y}")
            self.steps_left -= 1
        return self.steps_left > 0


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

        try:
            self.background_image = pygame.image.load("view/image/background.jpg").convert()
            self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            self.background_image = None

        self.creeper_count = 10
        self.thao = 2000
        self.radius = 1
        self.radius_explosion = 1
        self.distribution = "Euclid"
        self.last_update_time = pygame.time.get_ticks()
        self.creepers = []
        self.explosion_frames = [
            pygame.image.load(f"view/image/regularExplosion{i}.png").convert_alpha() for i in range(0, 8)
        ]
        self.explosion_frames = [pygame.transform.scale(frame, (20, 20)) for frame in self.explosion_frames]
        try:
            self.creeper_image_walk = pygame.image.load("view/image/walk.png").convert_alpha()
            self.creeper_image_walk = pygame.transform.scale(self.creeper_image_walk, (20, 20))
            self.creeper_image_hiss = pygame.image.load("view/image/hiss.png").convert_alpha()
            self.creeper_image_hiss = pygame.transform.scale(self.creeper_image_hiss, (20, 20))
            self.creeper_image_sleep = pygame.image.load("view/image/sleep.png").convert_alpha()
            self.creeper_image_sleep = pygame.transform.scale(self.creeper_image_sleep, (20, 20))
            self.creeper_image_born = pygame.image.load("view/image/born.png").convert_alpha()
            self.creeper_image_born = pygame.transform.scale(self.creeper_image_born, (20, 20))
        except pygame.error as e:
            print(f"Error loading image: {e}")
            pygame.quit()
            sys.exit()
        self.field = Field(
            (width, height),
            creepers_num=self.creeper_count,
            explosion_radius=self.radius_explosion,
            move_radius=self.radius,
            func_type=DistFunc.Manhattan,
        )
        # Initialize creepers
        self.create_creepers()

        # UI elements
        self.create_ui_elements()

    def create_ui_elements(self):
        # Создаем слайдеры и кнопки
        self.creeper_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), (400, 40)),
            start_value=self.creeper_count,
            value_range=(1, 50000),
            manager=self.manager,
        )
        self.creeper_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((420, 10), (200, 40)),
            text=f"Creepers: {self.creeper_count}",
            manager=self.manager,
        )

        self.thao_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 60), (400, 40)),
            start_value=self.thao // 1000,
            value_range=(0.1, 5),
            manager=self.manager,
        )
        self.thao_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((420, 60), (200, 40)),
            text=f"Thao: {self.thao / 1000:.1f} s",
            manager=self.manager,
        )

        self.radius_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 110), (400, 40)),
            start_value=self.radius,
            value_range=(1, 100),
            manager=self.manager,
        )
        self.radius_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((420, 110), (200, 40)),
            text=f"Radius: {self.radius}",
            manager=self.manager,
        )

        self.radius_explosion_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 160), (400, 40)),
            start_value=self.radius_explosion,
            value_range=(1, 100),
            manager=self.manager,
        )
        self.radius_explosion_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((420, 160), (200, 40)),
            text=f"Radius explosion: {self.radius_explosion}",
            manager=self.manager,
        )

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 210), (150, 40)),
            text="Start Simulation",
            manager=self.manager,
        )

        # # Создаем выпадающий список для выбора распределения
        # self.distribution_dropdown = pygame_gui.elements.UIDropDownMenu(
        #     options_list=["Polar", "Euclid", "Manhattan"],
        #     starting_option="Manhattan",
        #     relative_rect=pygame.Rect((10, 260), (400, 40)),
        #     manager=self.manager,
        # )
        # self.distribution_label = pygame_gui.elements.UILabel(
        #     relative_rect=pygame.Rect((420, 260), (200, 40)),
        #     text="Distribution: Manhattan",
        #     manager=self.manager,
        # )

    def create_creepers(self):
        creepers_data = self.field.get_creepers()
        self.creepers = []
        for data in creepers_data:
            x, y = data.get_coord()
            if not (math.isnan(x) or math.isnan(y)):  # Проверяем, что координаты валидны
                self.creepers.append(
                    CreeperDraw(
                        pos_x=x,
                        pos_y=y,
                        explosion_frames=self.explosion_frames,
                    )
                )
            else:
                print(f"Invalid creeper coordinates: ({x}, {y})")

    def update_targets(self):
        self.field.update_field()
        creepers_data = self.field.get_creepers()
        for creeper, data in zip(self.creepers, creepers_data):
            x, y = data.get_coord()
            state = data.get_state()
            # print(f"Creeper {creeper} target: {x}, {y}")
            if math.isnan(y):
                print(data.get_coord())
            creeper.set_target(x, y, steps=max(1, self.thao // 16))

            creeper.state = state
            if state == CreeperState.Explodes:
                creeper.start_explosion()

    def animate_creeper_positions(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill((255, 255, 255))  # Белый фон

        moving = False
        for creeper in self.creepers:
            if creeper.update_position():
                moving = True
            x, y = creeper.pos_x + self.center_x, creeper.pos_y + self.center_y

            if not (math.isnan(x) or math.isnan(y)):
                if creeper.state == CreeperState.Walk:
                    self.screen.blit(self.creeper_image_walk, (int(x), int(y)))
                elif creeper.state == CreeperState.Explodes:
                    creeper.update_explosion()
                    creeper.draw(self.screen, self.center_x, self.center_y)
                elif creeper.state == CreeperState.Born:
                    self.screen.blit(self.creeper_image_born, (int(x), int(y)))
                elif creeper.state == CreeperState.Sleep:
                    self.screen.blit(self.creeper_image_sleep, (int(x), int(y)))
                elif creeper.state == CreeperState.Hissing:
                    self.screen.blit(self.creeper_image_hiss, (int(x), int(y)))
            else:
                print(f"Invalid creeper position: ({x}, {y})")
        return moving

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            return False  # Выход из игры
        elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            self.handle_slider_moved(event)
        elif event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            self.handle_dropdown_changed(event)
        elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.start_button:
            self.start_game()
        return True

    def handle_slider_moved(self, event):
        if event.ui_element == self.creeper_slider:
            self.creeper_count = int(event.value)
            self.creeper_label.set_text(f"Creepers: {self.creeper_count}")
        elif event.ui_element == self.thao_slider:
            self.thao = int(event.value * 1000)
            self.thao_label.set_text(f"Thao: {self.thao / 1000:.1f} s")
        elif event.ui_element == self.radius_slider:
            self.radius = int(event.value)
            self.radius_label.set_text(f"Radius: {self.radius}")
        elif event.ui_element == self.radius_explosion_slider:
            self.radius_explosion = int(event.value)
            self.radius_explosion_label.set_text(f"Radius explosion: {self.radius_explosion}")

    def handle_dropdown_changed(self, event):
        if event.ui_element == self.distribution_dropdown:
            self.distribution = event.text
            self.distribution_label.set_text(f"Distribution: {self.distribution}")

    def start_game(self):
        func_type_map = {
            "Polar": DistFunc.Polar,
            "Euclid": DistFunc.Euclid,
            "Manhattan": DistFunc.Manhattan,
        }
        func_type = func_type_map.get(self.distribution, DistFunc.Manhattan)

        # Инициализация поля и криперов
        self.field = Field(
            (self.width, self.height),
            creepers_num=self.creeper_count,
            explosion_radius=self.radius_explosion,
            move_radius=self.radius,
            func_type=func_type,
        )
        self.field.update_field()
        self.create_creepers()
        self.update_targets()

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                running = self.handle_event(event)  # Обработка события

            self.manager.process_events(event)
            self.manager.update(time_delta)

            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time >= self.thao:
                self.last_update_time = current_time
                self.update_targets()

            moving = self.animate_creeper_positions()
            if not moving:
                self.update_targets()

            # Рисуем интерфейс
            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Simulation().run()
