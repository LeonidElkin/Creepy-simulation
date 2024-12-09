from abc import ABC, abstractmethod

import pygame
import pygame_gui


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
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 10), (400, 40)),
            start_value=app.creeper_count,
            value_range=(1, 50000),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 10), (200, 40)),
                text=f"Creepers: {app.creeper_count}",
                manager=app.manager,
            )
        )

    def handel(self, event):
        self.app.creeper_count = int(event.value)
        self.label.set_text(f"Creepers: {self.app.creeper_count}")

    # def handel(self, event):
    #     value = int(event.value)
    #     self.app.parameters["creeper_count"] = value
    #     self.label.set_text(f"Creepers: {value}")


class TaoSlider(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 60), (400, 40)),
            start_value=app.thao // 1000,
            value_range=(0.5, 5),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 60), (200, 40)),
                text=f"Thao: {app.thao / 1000:.1f} s",
                manager=app.manager,
            )
        )

    def handel(self, event):
        self.app.thao = int(event.value * 1000)
        self.label.set_text(f"Thao: {self.app.thao / 1000:.1f} s")

    # def handel(self, event):
    #     value = int(event.value * 1000)  # Преобразуем в миллисекунды
    #     self.app.parameters["thao"] = value
    #     self.label.set_text(f"Thao: {value / 1000:.1f} s")


class RadiusSlider(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 110), (400, 40)),
            start_value=app.radius,
            value_range=(20, 200),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 110), (200, 40)),
                text=f"Walk radius: {app.radius}",
                manager=app.manager,
            )
        )

    def handel(self, event):
        self.app.radius = int(event.value)
        self.label.set_text(f"Walk radius: {self.app.radius}")

    # def handel(self, event):
    #     value = int(event.value)
    #     self.app.parameters["radius"] = value
    #     self.label.set_text(f"Walk radius: {value}")


class RadiusExplosionSlider(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((10, 160), (400, 40)),
            start_value=app.radius_explosion,
            value_range=(1, 100),
            manager=app.manager,
        )
        self.add_label(
            pygame_gui.elements.UILabel(
                relative_rect=pygame.Rect((420, 160), (200, 40)),
                text=f"Radius explosion: {app.radius_explosion}",
                manager=app.manager,
            )
        )

    def handel(self, event):
        self.app.radius_explosion = int(event.value)
        self.label.set_text(f"Radius explosion: {self.app.radius_explosion}")

    # def handel(self, event):
    #     value = int(event.value)
    #     self.app.parameters["radius_explosion"] = value
    #     self.label.set_text(f"Radius explosion: {value}")


class StartButton(UiElement):
    def __init__(self, app):
        super().__init__(app)
        self.event = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 210), (150, 40)),
            text="Start Simulation",
            manager=app.manager,
        )

    def handel(self, event):
        self.app.start_game()


class UiManager:
    def __init__(self, app):
        ui_classes = [CreeperSlider, TaoSlider, RadiusSlider, RadiusExplosionSlider, StartButton]
        self.ui_elems = [ui_elem(app) for ui_elem in ui_classes]

    def handle_event(self, event):
        for ui_elem in self.ui_elems:
            if event.ui_element == ui_elem.event:
                ui_elem.handel(event)
                return True
        return False
