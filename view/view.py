from enum import Enum

import ttkbootstrap as ttk
from handler import update_config, new_states


class States(Enum):
    CHILL = "Chill"
    MOVING = "Move"
    HISS = "Hiss"
    SLEEP = "Sleep"


class Creeper:
    def __init__(self, canvas, pos_x=0, pos_y=0):
        self.canvas = canvas
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.state = States.CHILL
        self.shape = self.canvas.create_oval(self.pos_x - 5, self.pos_y - 5, self.pos_x + 5, self.pos_y + 5,
                                             fill="black")

    def move_to(self, target_x, target_y, steps=10):
        dx = (target_x - self.pos_x) / steps
        dy = (target_y - self.pos_y) / steps
        self.animate(dx, dy, steps)

    def animate(self, dx, dy, steps_left):
        if steps_left > 0:
            self.pos_x += dx
            self.pos_y += dy
            self.canvas.coords(self.shape, self.pos_x - 5, self.pos_y - 5, self.pos_x + 5, self.pos_y + 5)
            self.canvas.after(30, self.animate, dx, dy, steps_left - 1)


class Window:
    def __init__(self, size: str = "1000x1000"):
        self.app = ttk.Window(title="Creepy", themename="minty")
        self.app.geometry(size)
        self.entries = {}
        self.canvas = None
        self.creepers = []
        self.create_paned_window()

    def create_paned_window(self):
        paned_window = ttk.PanedWindow(self.app, orient="horizontal")
        paned_window.pack(fill="both", expand=True)

        left_frame = self.create_left_frame(paned_window)
        right_frame = self.create_right_frame(paned_window)

        paned_window.add(left_frame, weight=1)
        paned_window.add(right_frame, weight=3)

    def create_left_frame(self, parent):
        left_frame = ttk.Frame(parent, width=200)

        ttk.Label(left_frame, text="Введите данные", font=("Arial", 12, "bold")).pack(pady=10)

        self.create_placeholder_entry(left_frame, "Криперы:", "Количество", "nums")
        self.create_placeholder_entry(left_frame, "Частота:", "𝛕", "thao")
        self.create_placeholder_entry(left_frame, "Радиус:", "r", "radius")

        submit_button = ttk.Button(left_frame, text="Запуск симуляции", bootstyle="danger-outline", command=self.submit)
        submit_button.pack(pady=10)

        return left_frame

    def create_right_frame(self, parent):
        right_frame = ttk.Frame(parent)
        self.canvas = ttk.Canvas(right_frame, background="white")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        return right_frame

    def create_placeholder_entry(self, parent, label_text, placeholder_text, entry_key):
        frame = ttk.Frame(parent)
        frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame, text=label_text, font=("Arial", 10, "bold")).pack(side="left")

        entry = ttk.Entry(frame, bootstyle="info")
        entry.pack(side="left", fill="x", expand=True, padx=5)
        self.entries[entry_key] = entry

        placeholder = ttk.Label(frame, text=placeholder_text, foreground="grey")
        placeholder.place(in_=entry, relx=0.02, rely=0.5, anchor="w")

        entry.bind("<FocusIn>", lambda event: placeholder.place_forget())
        entry.bind("<FocusOut>", lambda event: self.show_placeholder_if_empty(entry, placeholder))

    @staticmethod
    def show_placeholder_if_empty(entry, placeholder):
        if not entry.get():
            placeholder.place(in_=entry, relx=0.02, rely=0.5, anchor="w")

    def submit(self):
        nums = int(self.entries["nums"].get())
        thao = float(self.entries["thao"].get())
        radius = float(self.entries["radius"].get())

        result = update_config(nums, thao, radius)
        print("Конфигурация обновлена:", result)
        self.create_creepers()
        self.update_creeper_positions()

    def create_creepers(self):
        if not self.creepers:
            nums = int(self.entries["nums"].get())
            for x, y in new_states(nums):
                self.creepers.append(Creeper(self.canvas, x, y))

    def update_creeper_positions(self):
        nums = int(self.entries["nums"].get())
        new_positions = new_states(nums)
        for creeper, (new_x, new_y) in zip(self.creepers, new_positions):
            creeper.move_to(new_x, new_y)

        self.app.after(2000, self.update_creeper_positions)

    def run(self):
        self.app.mainloop()


app = Window()
app.run()
