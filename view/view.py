import pygame
import pygame_gui
from handler import update_config, new_states


class Creeper:
    def __init__(self, pos_x=0, pos_y=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.target_x = pos_x
        self.target_y = pos_y
        self.dx = 0
        self.dy = 0
        self.steps_left = 0

    def set_target(self, target_x, target_y, steps=10):
        self.target_x = target_x
        self.target_y = target_y
        self.dx = (target_x - self.pos_x) / steps
        self.dy = (target_y - self.pos_y) / steps
        self.steps_left = steps

    def update_position(self):
        if self.steps_left > 0:
            self.pos_x += self.dx
            self.pos_y += self.dy
            self.steps_left -= 1
        return self.steps_left > 0


class Simulation:
    def __init__(self, width=1920, height=1080, image_path="view/image/creeper_icon.png"):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Creepy Simulation")
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((width, height))

        # Default simulation parameters
        self.creeper_count = 1000
        self.thao = 2000  # Target update interval in milliseconds
        self.radius = 100
        self.last_update_time = pygame.time.get_ticks()
        self.creepers = []

        try:
            self.creeper_image = pygame.image.load(image_path).convert_alpha()
            self.creeper_image = pygame.transform.scale(self.creeper_image, (10, 10))  # Resize to 20x20 pixels
        except Exception as e:
            print(f"Error loading image: {e}")
            pygame.quit()
            exit()

        # Initialize creepers
        self.create_creepers()

        # UI elements
        self.create_ui_elements()

    def create_ui_elements(self):
        # Creeper count slider
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

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 160), (150, 40)),
            text="Start Simulation",
            manager=self.manager,
        )

    def create_creepers(self):
        initial_positions = new_states(self.creeper_count)
        self.creepers = [Creeper(pos_x=x, pos_y=y) for x, y in initial_positions]

    def update_targets(self):
        steps = max(1, self.thao // 16)
        for creeper in self.creepers:
            target_x, target_y = new_states(1)[0]
            creeper.set_target(target_x, target_y, steps)

    def animate_creeper_positions(self):
        self.screen.fill((255, 255, 255))  # White background

        moving = False
        for creeper in self.creepers:
            if creeper.update_position():
                moving = True
            # Draw PNG image
            self.screen.blit(self.creeper_image, (int(creeper.pos_x), int(creeper.pos_y)))

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
                        update_config(self.creeper_count, self.thao / 1000, self.radius)
                    elif event.ui_element == self.thao_slider:
                        self.thao = int(event.value * 1000)
                        self.thao_label.set_text(f"Thao: {self.thao / 1000:.1f} s")
                        update_config(self.creeper_count, self.thao / 1000, self.radius)
                    elif event.ui_element == self.radius_slider:
                        self.radius = int(event.value)
                        self.radius_label.set_text(f"Radius: {self.radius}")
                        update_config(self.creeper_count, self.thao / 1000, self.radius)
                elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
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
