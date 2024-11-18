import os
import sys

package_path = os.path.dirname(os.path.abspath(__file__))
h, _ = os.path.split(package_path)
sys.path.append(h)

from enum import Enum

import pygame
import pygame_gui
from creepers import *


class State(Enum):
    BORN = "Born"
    HISS = "Hiss"
    SLEEP = "Sleep"
    WALK = "Walk"
    EXPLOSION = "Explosion"


class CreeperDraw:
    def __init__(self, pos_x=0, pos_y=0, explosion_frames=None):
        self.explosion_frames = explosion_frames
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.target_x = pos_x
        self.target_y = pos_y
        self.dx = 0
        self.dy = 0
        self.steps_left = 0
        self.state = State.WALK
        self.explosion_frame_index = 0
        self.explosion_timer = 0

    def start_explosion(self):
        self.state = State.EXPLOSION
        self.explosion_frame_index = 0
        self.explosion_timer = pygame.time.get_ticks()

    def update_explosion(self):
        timer = 100
        if self.state == State.EXPLOSION:
            if pygame.time.get_ticks() - self.explosion_timer > timer:  # 100 ms between frames
                self.explosion_frame_index += 1
                self.explosion_timer = pygame.time.get_ticks()
            if self.explosion_frame_index >= len(self.explosion_frames):
                self.state = State.BORN  # Change to a different state after the explosion
                self.explosion_frame_index = len(self.explosion_frames) - 1  # Keep last frame if needed

    def draw(self, screen, center_x, center_y):
        if self.state == State.EXPLOSION:
            screen.blit(
                self.explosion_frames[self.explosion_frame_index],
                (int(self.pos_x + center_x), int(self.pos_y + center_y)),
            )

    def set_target(self, target_x, target_y, center_x, center_y, steps=10):
        self.target_x = target_x - center_x
        self.target_y = target_y - center_y
        self.dx = (self.target_x - self.pos_x) / steps
        self.dy = (self.target_y - self.pos_y) / steps
        self.steps_left = steps
        self.state = State.WALK

    def update_position(self):
        if self.steps_left > 0:
            self.pos_x += self.dx
            self.pos_y += self.dy
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

        self.creeper_count = 1000
        self.thao = 2000
        self.radius = 1
        self.radius_explosion = 1
        self.last_update_time = pygame.time.get_ticks()
        self.creepers = []
        self.explosion_frames = [
            pygame.image.load(f"view/image/regularExplosion{i}.png").convert_alpha() for i in range(0, 8)
        ]
        self.explosion_frames = [pygame.transform.scale(frame, (20, 20)) for frame in self.explosion_frames]
        try:
            self.creeper_image_walk = pygame.image.load("view/image/walk.png").convert_alpha()
            self.creeper_image_walk = pygame.transform.scale(self.creeper_image_walk, (50, 50))
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
            func_type=DistFunc.Polar,
        )
        # Initialize creepers
        self.create_creepers()

        # UI elements
        self.create_ui_elements()

    def create_ui_elements(self):
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
            value_range=(10, 100),
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
            value_range=(10, 100),
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

    def create_creepers(self):
        creepers_data = self.field.get_creepers()

        self.creepers = [
            CreeperDraw(
                pos_x=data.get_coord()[0] - self.center_x,
                pos_y=data.get_coord()[1] - self.center_y,
                explosion_frames=self.explosion_frames,
            )
            for data in creepers_data
        ]
        for crep in creepers_data:
            print(crep.get_coord())
            print(len(creepers_data))

    def update_targets(self):
        creepers_data = self.field.get_creepers()

        for creeper, data in zip(self.creepers, creepers_data):
            x, y = data.get_coord()
            state = data.get_state()

            creeper.set_target(x, y, self.center_x, self.center_y, steps=max(1, self.thao // 16))

            if state == CreeperState.Walk:
                creeper.state = State.WALK
            elif state == CreeperState.Born:
                creeper.state = State.BORN
            elif state == CreeperState.Sleep:
                creeper.state = State.SLEEP
            elif state == CreeperState.Hissing:
                creeper.state = State.HISS
            elif state == CreeperState.Explodes:
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
            if creeper.state == State.WALK:
                self.screen.blit(
                    self.creeper_image_walk, (int(creeper.pos_x + self.center_x), int(creeper.pos_y + self.center_y))
                )
            elif creeper.state == State.EXPLOSION:
                creeper.update_explosion()
                creeper.draw(self.screen, self.center_x, self.center_y)
            elif creeper.state == State.BORN:
                self.screen.blit(
                    self.creeper_image_born, (int(creeper.pos_x + self.center_x), int(creeper.pos_y + self.center_y))
                )
            elif creeper.state == State.SLEEP:
                self.screen.blit(
                    self.creeper_image_sleep, (int(creeper.pos_x + self.center_x), int(creeper.pos_y + self.center_y))
                )
            elif creeper.state == State.HISS:
                self.screen.blit(
                    self.creeper_image_hiss, (int(creeper.pos_x + self.center_x), int(creeper.pos_y + self.center_y))
                )

        return moving

    def run(self):
        running = True
        while running:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.creeper_slider:
                        self.creeper_count = int(event.value)
                        self.creeper_label.set_text(f"Creepers: {self.creeper_count}")
                    elif event.ui_element == self.thao_slider:
                        self.thao = int(event.value * 1000)
                        self.thao_label.set_text(f"Thao: {self.thao / 1000:.1f} s")
                    elif event.ui_element == self.radius_slider:
                        self.radius = int(event.value)
                        self.radius_label.set_text(f"Radius: {self.radius}")
                elif event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.start_button:
                    self.field = Field(
                        (width, height),
                        creepers_num=self.creeper_count,
                        explosion_radius=self.radius_explosion,
                        move_radius=self.radius,
                        func_type=DistFunc.Polar,
                    )
                    self.create_creepers()

            self.manager.process_events(event)
            self.manager.update(time_delta)

            if pygame.time.get_ticks() - self.last_update_time > self.thao:
                self.update_targets()
                self.last_update_time = pygame.time.get_ticks()

            moving = self.animate_creeper_positions()
            if not moving:
                self.update_targets()

            self.manager.draw_ui(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Simulation().run()
