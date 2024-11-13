from enum import Enum
from random import sample

import ttkbootstrap as ttk
from PIL import Image, ImageDraw, ImageTk
from handler import update_config, new_states


class States(Enum):
    CHILL = "Chill"
    MOVING = "Move"
    HISS = "Hiss"
    SLEEP = "Sleep"


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


class Window:
    def __init__(self, size: str = "1920x1080"):
        self.app = ttk.Window(title="Creepy", themename="minty")
        self.app.geometry(size)
        self.entries = {}
        self.canvas = None
        self.creepers = []
        self.active_creepers = []
        self.create_paned_window()
        self.creeper_image = None
        self.thao = 2000
        self.frames_per_second = 100
        self.animation_interval = 1000 // self.frames_per_second
        self.animation_job = None

    def create_paned_window(self):
        main_frame = ttk.Frame(self.app)
        main_frame.pack(fill="both", expand=True)

        top_frame = self.create_top_frame(main_frame)
        top_frame.pack(fill="x", padx=10, pady=10)

        bottom_frame = self.create_bottom_frame(main_frame)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def create_top_frame(self, parent):
        left_frame = ttk.Frame(parent, width=200)
        ttk.Label(left_frame, text="Введите данные", font=("Arial", 12, "bold")).pack(
            pady=10
        )

        self.create_scale_entry(left_frame, "Криперы:", 1, 50000, "nums")
        self.create_scale_entry(left_frame, "Частота:", 0.1, 5, "thao")
        self.create_scale_entry(left_frame, "Радиус:", 1, 100, "radius")

        submit_button = ttk.Button(
            left_frame,
            text="Запуск симуляции",
            bootstyle="danger-outline",
            command=self.submit,
        )
        submit_button.pack(pady=10)
        return left_frame

    def create_bottom_frame(self, parent):
        right_frame = ttk.Frame(parent)
        self.canvas = ttk.Canvas(right_frame, background="white")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        return right_frame

    def create_scale_entry(self, parent, label_text, from_, to, entry_key):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text=label_text, font=("Arial", 10, "bold")).pack(side="left")

        scale = ttk.Scale(
            frame,
            from_=from_,
            to=to,
            orient="horizontal",
            length=150,
            command=lambda v: self.update_scale_value(entry_key, v),
        )
        scale.pack(side="left", fill="x", expand=True, padx=5)
        self.entries[entry_key] = scale

        value_label = ttk.Label(frame, text=str(scale.get()))
        value_label.pack(side="right")
        self.entries[f"{entry_key}_value_label"] = value_label

    def update_scale_value(self, entry_key, value):
        self.entries[f"{entry_key}_value_label"].config(text=f"{float(value):.2f}")

    def submit(self):
        if self.animation_job is not None:
            self.app.after_cancel(self.animation_job)
            self.animation_job = None

        self.creepers.clear()
        self.canvas.delete("all")
        self.active_creepers.clear()

        nums = int(self.entries["nums"].get())
        self.thao = int(float(self.entries["thao"].get()) * 1000)
        radius = float(self.entries["radius"].get())

        update_config(nums, self.thao, radius)
        self.create_creepers(nums)
        self.update_targets()
        self.animate_creeper_positions()

    def create_creepers(self, nums):
        self.creepers = []
        for x, y in new_states(nums):
            creeper = Creeper(x, y)
            self.creepers.append(creeper)

    def update_targets(self):
        if not self.active_creepers:
            self.active_creepers = sample(self.creepers, min(len(self.creepers), 250))
            steps = max(1, self.thao // self.animation_interval)

            new_positions = new_states(len(self.active_creepers))
            for creeper, (new_x, new_y) in zip(self.active_creepers, new_positions):
                creeper.set_target(new_x, new_y, steps)

        self.app.after(self.thao, self.update_targets)

    def animate_creeper_positions(self):
        image = Image.new("RGB", (1920, 1080), "white")
        draw = ImageDraw.Draw(image)

        moving = False

        for creeper in self.creepers:
            if creeper.update_position():
                moving = True

            draw.ellipse(
                (
                    creeper.pos_x - 2,
                    creeper.pos_y - 2,
                    creeper.pos_x + 2,
                    creeper.pos_y + 2,
                ),
                fill="black",
            )

        self.creeper_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.creeper_image, anchor="nw")

        if moving:
            self.animation_job = self.app.after(
                self.animation_interval, self.animate_creeper_positions
            )
        else:
            self.active_creepers.clear()
            self.update_targets()
            self.animation_job = self.app.after(
                self.animation_interval, self.animate_creeper_positions
            )

    def run(self):
        self.app.mainloop()


app = Window()
app.run()
