import math
from abc import ABC, abstractmethod

import pygame
import pygame_gui

slider_size = (400, 40)
slider_text_size = (250, 40)


class UiElement(ABC):
    def __init__(self, app):
        self.label = None
        self.event = None
        self.app = app

    def add_label(self, label):
        self.label = label

    @abstractmethod
    def handel(self, event):
        pass


class CreeperSlider(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.lin_min = 0
        self.lin_max = 100
        self.log_min = 1
        self.log_max = 50000
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), slider_size),
            start_value=self.log_to_linear(self.app.creepers_params.creeper_count),
            value_range=(self.lin_min, self.lin_max),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 10), slider_text_size),
                text=f"Creepers: {self.app.creepers_params.creeper_count}",
                manager=app.manager,
            )
        )

    def linear_to_log(self, linear_value):
        linear_ratio = (linear_value - self.lin_min) / (self.lin_max - self.lin_min)
        log_value = self.log_min * (self.log_max / self.log_min) ** linear_ratio
        return int(log_value)

    def log_to_linear(self, log_value):
        log_ratio = math.log(log_value / self.log_min) / math.log(self.log_max / self.log_min)
        linear_value = self.lin_min + log_ratio * (self.lin_max - self.lin_min)
        return linear_value

    def handel(self, event):
        self.app.creepers_params.creeper_count = self.linear_to_log(int(event.value))
        self.label.set_text(f"Creepers: {self.app.creepers_params.creeper_count}")


class TaoSlider(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 60), slider_size),
            start_value=app.thao // 1000,
            value_range=(0.5, 5),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 60), slider_text_size),
                text=f"Thao: {app.thao / 1000:.1f} s",
                manager=app.manager,
            )
        )

    def handel(self, event):
        self.app.thao = int(event.value * 1000)
        self.label.set_text(f"Thao: {self.app.thao / 1000:.1f} s")


class CreeperWalkRadius(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 110), slider_size),
            start_value=self.app.creepers_params.radius,
            value_range=(1, 200),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 110), slider_text_size),
                text=f"Creeper walk radius: {self.app.creepers_params.radius}",
                manager=app.manager,
            )
        )

    def handel(self, event):
        self.app.creepers_params.radius = int(event.value)
        self.label.set_text(f"Creeper walk radius: {self.app.creepers_params.radius}")


class CreeperRadiusExplosionSlider(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 160), slider_size),
            start_value=self.app.creepers_params.radius_explosion,
            value_range=(1, 100),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 160), slider_text_size),
                text=f"Creeper radius explosion: {self.app.creepers_params.radius_explosion}",
                manager=app.manager,
            )
        )

    def handel(self, event):
        self.app.creepers_params.radius_explosion = int(event.value)
        self.label.set_text(f"Creeper radius explosion: {self.app.creepers_params.radius_explosion}")


class SteveCount(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 210), slider_size),
            start_value=self.app.steve_params.count,
            value_range=(0, 200),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 210), slider_text_size),
                text=f"Steve count: {self.app.steve_params.count}",
                manager=app.manager,
            )
        )

    def handel(self, event):
        self.app.steve_params.count = int(event.value)
        self.label.set_text(f"Steve count: {self.app.steve_params.count}")


class SteveRadius(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 260), slider_size),
            start_value=self.app.steve_params.radius,
            value_range=(1, 100),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 260), slider_text_size),
                text=f"Steve walk radius: {self.app.steve_params.radius}",
                manager=app.manager,
            )
        )

    def handel(self, event):
        self.app.steve_params.radius = int(event.value)
        self.label.set_text(f"Steve walk radius: {self.app.steve_params.radius}")


class StartButton(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 310), (150, 40)),
            text="Start Simulation",
            manager=app.manager,
        )

    def handel(self, event):
        self.app.start_game()


class UiManager:
    def __init__(self, app):
        ui_classes = [
            CreeperSlider,
            TaoSlider,
            CreeperWalkRadius,
            CreeperRadiusExplosionSlider,
            SteveRadius,
            SteveCount,
            StartButton,
        ]
        self.ui_elems = [ui_elem(app) for ui_elem in ui_classes]

    def handle_event(self, event):
        for ui_elem in self.ui_elems:
            if event.ui_element == ui_elem.event:
                ui_elem.handel(event)
                return True
        return False
